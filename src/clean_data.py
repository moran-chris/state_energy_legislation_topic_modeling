import pandas as pd 
import numpy as np 
import matplotlib.pyplot as pld 
from string import punctuation


def combine_data(file_path_list):
    ''' combines dataframe for each year''' 

    dfs = []
    for path in file_path_list:
        df = pd.read_pickle(path)
        dfs.append(df)
    return pd.concat(dfs)

def clean_df(df):
    ''' cleans and extracts fields from dataframe '''

    df = df[~df['text'].isna()]
    df['state'] = df['bill_id'].apply(lambda x: x[:2])
    df.drop_duplicates(subset = ['text','state'],keep = 'first',inplace = True)
    df.drop_duplicates(subset = ['bill_id','author'],keep = 'first',inplace = True)
    df['text'] = df['text'].apply(lambda x: x.lower())
    df['text'] = df['text'].apply(lambda x: remove_punctuation(x))
    df['text'] = df['text'].apply(lambda x: x.replace("\n",' '))
    df['primary_dem'] = df['author'].apply(lambda x: count_party(x))
    df['primary_rep'] = df['author'].apply(lambda x: count_party(x, '(R)'))
    df['additional_dem'] = df['additional_authors'].apply(lambda x: count_party(x))
    df['additional_rep'] = df['additional_authors'].apply(lambda x: count_party(x, '(R)'))
    df['new_status'] = df['status'].apply(lambda x: get_status(x))
    df['passed'] = df['new_status'].apply(lambda x: 1 if x == 'passed' else 0)
    df['bi'] = (((df['primary_dem'] + df['additional_dem']) != 0) & (
                (df['primary_rep'] + df['additional_rep'] != 0)))
    df['has_associated'] = df['associated_bills'].isnull()
    df['proposed_by'] = df['bill_id'].apply(lambda x: x.split(' ')[1])
    df['proposed_by'] = df['proposed_by'].apply(lambda x: get_proposed_by(x))
    df['unique_id'] = np.arange(df.shape[0])
    return df

def count_party(string,party = '(D)'):
    ''' counts the nuber of authors of a given party ''' 

    try:    
        party = [idx for idx in range(len(string)) if string.startswith(party,idx)] 
        return len(party)
    except:
        return 0

def remove_punctuation(string, punc=punctuation):
    ''' removes punctuation from a given string '''

    for character in punc:
        string = string.replace(character,'')
    return string

def get_status(cell):
    status =  cell[:(cell.find('-') - 1)]
    if status in ['Pending','Override Pending','To Governor']:
        return 'pending'
    elif status in ['Adopted', 'Enacted']:
        return 'passed'
    elif status in ['Failed', 'Vetoed']:
        return 'failed'
    else:
        return 'other'

def get_proposed_by(row):
        if row[0] == 'S':
            return 'S'
        elif row[0] == 'H':
            return 'H'
        elif row[0] == 'A':
            return 'A'
        else:
            return 'O'   


if __name__ == '__main__':
    

    file_paths = ['../data/pkl/energy_2020.pkl','../data/pkl/energy_2019.pkl','../data/pkl/energy_2018.pkl',
                '../data/pkl/energy_2017.pkl','../data/pkl/energy_2016.pkl','../data/pkl/energy_2015.pkl']
    df = combine_data(file_paths)
    df = clean_df(df)
    #df.to_pickle('../data/energy_cleaned_v2.pkl')
