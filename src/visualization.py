import pandas as pd 
import matplotlib.pyplot as plt 
import matplotlib
import numpy as np 




plt.style.use('ggplot')
font = {'family' : 'DejaVu Sans',
        'weight' : 'normal',
        'size'   : 16}
matplotlib.rc('font', **font)


def plot_topic_counts(df):
    fig,ax = plt.subplots()
    data = df[['clusters','unique_id']].groupby('clusters',as_index = False).count().sort_values(by = 'unique_id',ascending = False).values
    ax.bar([str(label) for label in list(data[:,0])],data[:,1])
    ax.set_xlabel('Topics')
    ax.set_ylabel('Bills')
    ax.set_title('Number of Bills by Topic')
    plt.show()

def plot_top_states(df,topics,labels):

    fig, ax = plt.subplots(len(topics))
    axes = ax.flatten()
    for idx,topic in enumerate(topics):
        data = df.loc[df['clusters'] == topic]
        grouped_data = data[['state','unique_id']].groupby('state',as_index = False).count().sort_values(by = 'unique_id',ascending = False).values
        axes[idx].bar(grouped_data[:5,0],grouped_data[:5,1])
        axes[idx].set_ylabel('Bills')
        axes[idx].set_title("Number of " + labels[idx] + " Bills by State" )
    axes[idx].set_xlabel('States')
    plt.show()

def bills_by_party(df):
    df['dem'] = df['primary_dem'].apply(lambda x: 1 if x != 0 else 0)
    df['rep'] = df['primary_rep'].apply(lambda x: 1 if x != 0 else 0)
    grouped = df[['clusters','rep','dem']].groupby('clusters',as_index =False).sum().values
    fig, ax = plt.subplots() 
    n = 7 
    ind = np.arange(n)
    width = .35
    print(grouped)
    ax.bar(ind,grouped[:,1],width,label = 'Republicans')
    ax.bar(ind + width,grouped[:,2],width,label = 'Democrats')
    ax.set_xticks(ind + width/2)
    ax.legend()
    ax.set_xticklabels(('1','2','3','4','5','6','7'))
    ax.set_xlabel('Topics')
    ax.set_ylabel('Bills')
    ax.set_title('Bills by Party')
    plt.show()

def bills_by_party_and_state(df):
    #df['dem'] = df['primary_dem'].apply(lambda x: 1 if x != 0 else 0)
    #df['rep'] = df['primary_rep'].apply(lambda x: 1 if x != 0 else 0)
    #grouped = df[['state','rep','dem']].groupby('state',as_index = False,).sum().sort_values(by = 'rep')
    grouped = df
    print(grouped.shape)
    fig,ax = plt.subplots()
    ind = np.arange(len(df))
    width = .35
    ax.barh(ind,grouped['rep'],width, label = 'Republicans')
    ax.barh(ind + width,grouped['dem'],width, label = 'Democrats')
    ax.set_yticks(ind + width/2)
    ax.set_yticklabels(grouped.state)
    ax.legend()
    ax.set_xlabel('Bills')
    ax.set_ylabel('State')
    ax.set_title('Bills by Party and State')
    plt.show()


def get_status(df):
    status_dict = {'Pending': 'pending','Adopted':'passed','Enacted':'passed',
                    'Failed':'failed','Vetoed':'failed','To Governor': 'pending',
                    'Override Pending': 'pending','':'other'}
    df['new_status'] = df['status'].apply(lambda x: x[:x.find('-') -1])
    df['new_status'] = df['new_status'].apply(lambda x: status_dict[x])
    return df
if __name__ == '__main__':
    df = pd.read_pickle('../data/clustered_data.pkl')
    df_ff = pd.read_pickle('../data/fossil_fuels_data.pkl')
    df_ff['subtopic_1'].astype(float)
    df_frak = df_ff.loc[df_ff['subtopic_1'] > .014]
    df_frak.reset_index(inplace =True)
    df_frak.drop('index',axis = 1,inplace = True)
    df_frak.index = np.arange(df_frak.shape[0])
    df_frak['dem'] = df_frak['primary_dem'].apply(lambda x: 1 if x != 0 else 0)
    df_frak['rep'] = df_frak['primary_rep'].apply(lambda x: 1 if x != 0 else 0)
    grouped = df_frak[['state','rep','dem']].groupby('state',as_index = False,).sum().sort_values(by = 'rep')    #plot_topic_counts(df)
    bills_by_party_and_state(grouped)
    #plot_top_states(df,[1,3,7],['Climate','Vehicles/Transportation','Fossil Fuels'])
    #bills_by_party(df)