import pandas as pd 
import numpy as np 
from sklearn.feature_extraction import stop_words
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.stop_words import ENGLISH_STOP_WORDS
from sklearn.decomposition import NMF
from sklearn.decomposition import SparsePCA
from sklearn.decomposition import TruncatedSVD
from sklearn.cluster import KMeans 
import nltk 
from sklearn.feature_extraction.text import TfidfVectorizer
import matplotlib.pyplot as plt  
import matplotlib
from get_stop_words import custom_stop_words,cluster_one_words,cluster_two_words
import get_stop_words


plt.style.use('ggplot')
font = {'family' : 'DejaVu Sans',
        'weight' : 'normal',
        'size'   : 16}
matplotlib.rc('font', **font)




def lemmatize_str(string):
    ''' Lemmatize a string and return it in its original format '''

    w_tokenizer = nltk.tokenize.WhitespaceTokenizer()
    lemmatizer = nltk.stem.WordNetLemmatizer()
    return " ".join([lemmatizer.lemmatize(w) for w in w_tokenizer.tokenize(string)])



def vectorize_tf(corpus):
    ''' tokenize text and returns a term frequency matrix 
        also removes stop words'''
    
    vectorizer = CountVectorizer(stop_words = custom_stop_words)
    X = vectorizer.fit_transform(corpus)
    features = np.array(vectorizer.get_feature_names())
    return X, features 

def vectorize_tf_idf(df, column, stop_words):
    ''' tokenize text and returns a tf_idf matrix 
        also removes stop words'''

    text = df[column].values
    vectorizer = TfidfVectorizer(stop_words = stop_words) 
    X = vectorizer.fit_transform(text)
    features = np.array(vectorizer.get_feature_names())
    return X, features 

def plot_pca(X,labels):
    ''' plots data points according to first two PCA values '''

    pca = TruncatedSVD(n_components = 2)
    X_pca = pca.fit_transform(X)
    fig, ax = plt.subplots(1, 1, figsize=(8, 6))

    for topic in set(labels):
        mask = labels == topic
        X_pca_masked = X_pca[mask]
        ax.scatter(X_pca_masked[:, 0], X_pca_masked[:, 1],alpha = .5, label = 'Topic '+str(topic),
            edgecolor='k', s=40)
          #cmap=plt.cm.Set1, #c = plt.cm.Set1.colors[topic/2],
    ax.legend()
    ax.set_title("First two PCA directions")
    ax.set_xlabel("1st eigenvector (PC1)")
    ax.set_ylabel("2nd eigenvector (PC2)")
    plt.show()

def get_nmf(X, n_components=7,alpha = .1):
    '''topic models corpus through NMF'''

    nmf = NMF(n_components=n_components, max_iter=100, random_state=12345, alpha=alpha)
    W = nmf.fit_transform(X)
    H = nmf.components_
    return W, H

def get_topic_words(H, features, n_features):
    ''' retrieve top words associated with each NMF topic '''

    top_word_indexes = H.argsort()[:, ::-1][:,:n_features]
    return features[top_word_indexes]

def document_topics(W):
    return W.argsort()[:,::-1][:,0]

def get_kmeans(X, k):
    ''' topic models corpus through kmeans '''

    kmeans = KMeans(n_clusters = k,random_state = 1234)
    labels = kmeans.fit_predict(X)
    return kmeans,labels

def kmeans_topics(X,kmeans_labels,features,n,n_words = 10):
    ''' retrieves top words associated with kmeans topics '''

    topics = []
    for idx in range(n):
        mask = kmeans_labels == idx
        cluster = X[mask]
        topic = get_topic_words(cluster.sum(axis = 0),features,n_words)
        topics.append(topic)
    return topics

def main(df,n = 7,cluster = None, model = 'NMF', alpha = .1,stop = []):
    ''' runs dataframe through topic modeling pipeline ''' 

    new_stop_words = list(custom_stop_words)
    new_stop_words.extend(stop)
    new_stop_words = set(new_stop_words)
    if cluster:
        df = df.loc[df['clusters_2'] == cluster]
    df['text'] = df['text'].apply(lambda x: lemmatize_str(x))
    corpus = df['text']
    X, features = vectorize_tf_idf(df,'text',new_stop_words)
    if model == 'NMF':
        W,H = get_nmf(X,n_components = n, alpha =alpha)
        return df,X,features,W,H
    else:
        kmeans,kmeans_labels = get_kmeans(X,n)
        return df,X,features,kmeans,kmeans_labels

def elbow_plot(input_data, num_iters):

    rss = []
    for n in range(1,num_iters+1):
        df,X,features,kmeans,kmeans_labels = main(input_data,n =n,model = 'Kmeans')    
        rss.append(-kmeans.score(X))
    fig, ax = plt.subplots(figsize = (15,10))    
    ax.plot(list(range(1,num_iters+1)),rss)
    ax.set_title('RSS vs K', fontsize = 35)
    ax.set_ylabel('RSS', fontsize = 30)
    ax.set_xlabel('K', fontsize = 30)
    plt.savefig('elbow.png')

    
if __name__ == '__main__':
    data = pd.read_pickle('../data/pkl/data_13_clusters.pkl')
    #data = pd.read_pickle('../data/pkl/energy_cleaned_v2.pkl')
    n = 4

    df,X,features,W,H= main(data, n, model = 'NMF',cluster = 3)
   # topics = kmeans_topics(X, kmeans_labels,features,n)
    topics = get_topic_words(H,features,10)