import pandas as pd 
import numpy as np 
from sklearn.feature_extraction import stop_words
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.stop_words import ENGLISH_STOP_WORDS
from sklearn.decomposition import NMF
from sklearn.decomposition import PCA
import nltk 
from sklearn.feature_extraction.text import TfidfVectorizer
import matplotlib.pyplot as plt  
import matplotlib

plt.style.use('ggplot')
font = {'family' : 'DejaVu Sans',
        'weight' : 'normal',
        'size'   : 16}
matplotlib.rc('font', **font)




def lemmatize_str(string):
    # Lemmatize a string and return it in its original format
    w_tokenizer = nltk.tokenize.WhitespaceTokenizer()
    lemmatizer = nltk.stem.WordNetLemmatizer()
    return " ".join([lemmatizer.lemmatize(w) for w in w_tokenizer.tokenize(string)])

def get_stop_words(new_stop_words=None):
    # Retrieve stop words and append any additional stop words
    stop_words = list(ENGLISH_STOP_WORDS)
    if new_stop_words:
        stop_words.extend(new_stop_words)
    return set(stop_words)

def vectorize_tf(corpus):
    vectorizer = CountVectorizer(stop_words = custom_stop_words)
    X = vectorizer.fit_transform(corpus)
    features = np.array(vectorizer.get_feature_names())
    return X, features 

def vectorize_tf_idf(df, column, stop_words):
    # Vectorize a text column of a pandas DataFrame
    text = df[column].values
    vectorizer = TfidfVectorizer(stop_words = stop_words) 
    X = vectorizer.fit_transform(text)
    features = np.array(vectorizer.get_feature_names())
    return X, features 

def get_top_words(X, features, n_features = 10):
    # Retrieve feature names given H matrix, feature names, and number of features
    top_word_indexes = X.argsort()[:, ::-1][:,:n_features]
    return features[top_word_indexes]

def plot_pca(X):
    pca = PCA(n_components = 2)
    X_pca = pca.fit_transform(X)
    fig, ax = plt.subplots(1, 1, figsize=(8, 6))
    ax.scatter(X_pca[:, 0], X_pca[:, 1], 
           cmap=plt.cm.Set1, edgecolor='k', s=40)
    ax.set_title("First two PCA directions")
    ax.set_xlabel("1st eigenvector (PC1)")
    ax.set_ylabel("2nd eigenvector (PC2)")
    plt.show()

def get_nmf(X, n_components=7,alpha = .1):
    # Create NMF matrixes based on a TF-IDF matrix
    nmf = NMF(n_components=n_components, max_iter=100, random_state=12345, alpha=alpha)
    W = nmf.fit_transform(X)
    H = nmf.components_
    return W, H

def get_topic_words(H, features, n_features):
    # Retrieve feature names given H matrix, feature names, and number of features
    top_word_indexes = H.argsort()[:, ::-1][:,:n_features]
    return features[top_word_indexes]

if __name__ == '__main__':
    df = pd.read_pickle('data/energy_cleaned.pkl')
    #df = df.sample(n = 500, random_state = 37)
    df['text'] = df['text'].apply(lambda x: lemmatize_str(x))
    corpus = df['text']
    states = ['alabama','alaska','arizona','arkansas','california','colorado',
            'connecticut','delaware','florida','georgia','hawaii','idaho','illinois',
            'indiana','iowa','kansas','kentucky','louisiana','maine','maryland',
            'massachusetts','michigan','minnesota','mississippi','missouri',
            'montana','nebraska','nevada','hampshire','jersey',
            'mexico','york','carolina','dakota','ohio',
            'oklahoma','oregon','pennsylvania','rhode','carolina',
            'dakota','tennessee','texas','utah','vermont',
            'virginia','washington','virginia','wisconsin','wyoming']

    new_stop_words = states + ['section', 'shall', 'state','law','including','chapter','cost',
                    'service','pursuant','act','provided','amended','public','plan',
                    'board','project','department','year','purpose','person','authority',
                    'agency','subdivision','program','commissioner','new','paragraph',
                    'provision','commission','mean','county','use','subsection','following',
                    'required','effective','authorized','article','date','read','federal',
                    'provide','requirement','day','prior','include','general','minnesota',
                    'office','available','code','district','director','york','subject',
                    'statute','sec','approved','follows','hawaii','customer','change','ha',
                    'senate','local','legislature','member','standard','effect','enacted',
                    'order','unit','necessary','ii','thousand','defined','limited','committee'
                    'period','jersey','council','2020','january','account','title',
                    'division','annual','municipality','eligible','adding','california',
                    'resolved','revised','city','proposed','governor','action','et','10',
                    'july','accordance','secretary','le','2019','line','thereof','cent',
                    'establish','related','adopted','adaptation','imposed','applicable',
                    'adopt','30','issued','determined','make','vermont','said',
                    'reccomendation','appointed','notwithstanding','regional','unless',
                    'ensure','virginia']
    custom_lematize_dict = {'electrical': 'electric'}
    custom_stop_words = get_stop_words(new_stop_words)
    #X, features = vectorize_tf(corpus)
    X, features = vectorize_tf_idf(df,'text',custom_stop_words)
    top_words = get_top_words(X.sum(axis = 0),features,200)
    n = 15
    W, H = get_nmf(X,n)
    topics = get_topic_words(H,features,n)

    #plot_pca(X.toarray())