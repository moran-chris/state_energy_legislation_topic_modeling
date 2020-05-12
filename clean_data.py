import pandas as pd 
import numpy as np 
import matplotlib.pyplot as pld 
from string import punctuation


def combine_data(file_path_list):
    dfs = []
    for path in file_path_list:
        df = pd.read_pickle(path)
        dfs.append(df)
    return pd.concat(dfs)

def clean_df(df):
    df = df[~df['text'].isna()]
    df['state'] = df['bill_id'].apply(lambda x: x[:2])
    df = df[~df.duplicated(subset = ['text','state'])]
    df = df[~df.duplicated(subset = ['bill_id','author'])]
    df['text'] = df['text'].apply(lambda x: x.lower())
    df['text'] = df['text'].apply(lambda x: remove_punctuation(x))
    df['text'] = df['text'].apply(lambda x: x.replace("\n",' '))
    df['primary_dem'] = df['author'].apply(lambda x: count_party(x))
    df['primary_rep'] = df['author'].apply(lambda x: count_party(x, '(R)'))
    df['additional_dem'] = df['additional_authors'].apply(lambda x: count_party(x))
    df['additional_rep'] = df['additional_authors'].apply(lambda x: count_party(x, '(R)'))
    return df

def count_party(string,party = '(D)'):
    try:    
        party = [idx for idx in range(len(string)) if string.startswith(party,idx)] 
        return len(party)
    except:
        return 0
def remove_punctuation(string, punc=punctuation):
    # remove given punctuation marks from a string
    for character in punc:
        string = string.replace(character,'')
    return string

if __name__ == '__main__':
    

    file_paths = ['data/pkl/energy_2020.pkl','data/pkl/energy_2019.pkl','data/pkl/energy_2018.pkl',
                'data/pkl/energy_2017.pkl','data/pkl/energy_2016.pkl','data/pkl/energy_2015.pkl']
    #df = pd.read_pickle(path)
    df = combine_data(file_paths)
    df = clean_df(df)
    df.to_pickle('data/energy_cleaned.pkl')
