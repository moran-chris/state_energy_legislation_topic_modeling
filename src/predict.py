import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import xgboost as xgb
from sklearn.metrics import recall_score
from sklearn.metrics import precision_score
from sklearn import metrics
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report
import pickle 
def merge_data(df1,df2):

    df1['key'] = df1['state'] + df1['year'].astype(str)
    df2['key'] = df2['state']+df2['year'].astype(str)
    df = df1.merge(df2,how ='left',left_on = 'key', right_on = 'key')
    #Removed NE because no data on party affiliation for house members
    df.drop(df.loc[df['state_x'] == 'NE'].index, inplace = True)
    #Removed other, only 70 out of over 12000 records 
    df.drop(df.loc[df['new_status'] == 'other'].index, inplace = True)
    columns = ['unique_id','state_x','primary_dem','primary_rep','additional_dem','additional_rep',
                'sen_dem_per','sen_rep_per','house_dem_per','house_rep_per','clusters_2',
                'legis_control_dem','legis_control_rep','gov_party_dem','gov_party_rep',
                'state_control_dem','state_control_rep','proposed_by','new_status','bi','has_associated',
                'passed']
    return df[columns]




def get_pca(X, n=2):
    scaler = StandardScaler(copy=True, with_mean=True, with_std=True)
    X = scaler.fit_transform(X)
    pca = PCA(n_components = n)
    return pca.fit_transform(X)

def get_model(model,X,y, n_splits = 2, threshold = .65):


    f1_scores = []
    recall = []
    precision = []
    skf = StratifiedKFold(n_splits = n_splits)

    for train_index, test_index in skf.split(X,y):
        model.fit(X[train_index], y[train_index])
        preds = model.predict_proba(X[test_index])[:,1]
        y_hat = (preds > threshold).astype(int)
        f1_scores.append(f1_score(y[test_index],y_hat,average = 'weighted'))
        recall.append(recall_score(y[test_index],y_hat))
        precision.append(precision_score(y[test_index], y_hat))
    f1_scores = np.array(f1_scores).mean()
    recall = np.array(recall).mean()
    precision = np.array(precision).mean()
    print(classification_report(y[test_index],y_hat))
    print(f' F1: {np.array(f1_scores).mean()}')
    print(f' recall {np.array(recall).mean()}')
    print(f' precision: {np.array(precision).mean()}')
    
    return model,f1_scores

def add_predict_probas(model, df):
    X = df.drop(['unique_id','passed'], axis = 1).values
    df['probas'] = model.predict_proba(X)[:,1]
    df['three'] = (df['probas'] > .3).astype(int)
    df['four'] = (df['probas'] > .4).astype(int)
    df['six'] = (df['probas'] > .6).astype(int)
    df['likelihood'] = df['six'] + df['four'] + df['three']
    df.drop(['six','four','three'], axis = 1, inplace = True)
    return df 





if __name__ == '__main__':

    bill_df = pd.read_pickle('../data/pkl/data_13_clusters.pkl')
    bill_df = add_proposed_by(bill_df)
    makeup_df = pd.read_pickle('../data/pkl/makeup.pkl')
    df = merge_data(bill_df,makeup_df)
    df = pd.get_dummies(df, columns = ['state_x', 'proposed_by','clusters_2'])
    with open('xgb_model', 'rb') as file:
        model = pickle.load(file)

    
    df['probas'] = predict_probas(model, df)
    df['cluster'] = df.merge(bill_df[['unique_id','clusters_2']], how = 'left', on = 'unique_id')


    ## Used When training 
    #df.drop(df.loc[df['new_status'] == 'pending'].index, inplace = True)
    #df.drop('new_status', axis = 1, inplace = True)




    #y_all = df['passed'].values
    #X_all = df.drop(['passed','unique_id'], axis = 1).values
    
    #For Training Purposes
    #X,X_holdout,y,y_holdout = train_test_split(
                                    #        X_all, y_all, test_size=0.2,stratify = y_all)
    
    # Used when building model 
    #model = xgb.XGBClassifier(max_depth = 2)
    # threshold = .65
    # get_model(model, X, y,n_splits = 3, threshold = threshold)

    # preds = model.predict_proba(X_holdout)[:,1]
    # y_hat = (preds > threshold).astype(int)   
    # print('F1')
    # print(f1_score(y_holdout,y_hat,average = 'weighted'))
    # print('Precision')
    # print(precision_score(y_holdout,y_hat))
    # print(classification_report(y_holdout, y_hat))

    # df = add_predict_probas(model,df)
    # # models = []
    # for i in range(1,10):
    #     model = xgb.XGBClassifier(max_depth = i)
    #     for n in np.linspace(.1,.5,20):
    #         threshold = n 
    #         for w in np.linspace(20,70,30):
    #             X_pca = get_pca(X,int(w))
    #             models.append(get_model(model,X_pca,y,threshold = threshold))


    

    # plt.plot(fpr,tpr)

    # print(f' F1: {np.array(f1_scores).mean()}')
    # print(f' recall {np.array(recall).mean()}')
    # print(f' precision: {np.array(precision).mean()}')