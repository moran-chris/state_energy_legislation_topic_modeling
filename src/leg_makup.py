import pandas as pd 
import numpy as np 
from string import punctuation


us_state_abbrev = {
    'Alabama': 'AL','Alaska': 'AK','American Samoa': 'AS','Arizona': 'AZ',
    'Arkansas': 'AR','California': 'CA','Colorado': 'CO','Connecticut': 'CT',
    'Delaware': 'DE','District of Columbia': 'DC','Florida': 'FL','Georgia': 'GA',
    'Guam': 'GU','Hawaii': 'HI','Idaho': 'ID','Illinois': 'IL','Indiana': 'IN',
    'Iowa': 'IA','Kansas': 'KS','Kentucky': 'KY','Louisiana': 'LA','Maine': 'ME',
    'Maryland': 'MD','Massachusetts': 'MA','Michigan': 'MI','Minnesota': 'MN',
    'Mississippi': 'MS','Missouri': 'MO','Montana': 'MT','Nebraska': 'NE',
    'Nevada': 'NV','New Hampshire': 'NH','New Jersey': 'NJ','New Mexico': 'NM',
    'New York': 'NY','North Carolina': 'NC','North Dakota': 'ND',
    'Northern Mariana Islands':'MP','Ohio': 'OH','Oklahoma': 'OK','Oregon': 'OR',
    'Pennsylvania': 'PA','Puerto Rico': 'PR','Rhode Island': 'RI','South Carolina': 'SC',
    'South Dakota': 'SD','Tennessee': 'TN','Texas': 'TX','Utah': 'UT','Vermont': 'VT',
    'Virgin Islands': 'VI','Virginia': 'VA','Washington': 'WA','West Virginia': 'WV',
    'Wisconsin': 'WI','Wyoming': 'WY'}

def remove_punctuation(string, punc=punctuation):
    ''' removes punctuation from a given string '''

    for character in punc:
        string = string.replace(character,'')
    return string

def main(file_paths):
    
    df = pd.DataFrame()
    year = 2015
    for path in file_paths:
        df2 = pd.read_csv('../data/'+path)
        df2['year'] = year 
        year += 1
        df = pd.concat([df,df2])
    df['STATE'] = df['STATE'].apply(lambda x: remove_punctuation(x))
    df['state'] = df['STATE'].apply(lambda x: us_state_abbrev[x])
    df.drop(df.loc[df['STATE'] == 'Nebraska'].index, inplace = True)
    df.drop('STATE',axis = 1, inplace = True)
    df['sen_dem_per'] = df['Senate_Dem']/df['Total_Senate']
    df['sen_rep_per'] = df['Senate_Rep']/df['Total_Senate']
    df['house_dem_per'] = df['House_Dem.']/df['Total_House']
    df['house_rep_per'] = df['House_Rep']/df['Total_House']
    df['legis_control_dem'] = df['Legis_Control'].apply(lambda x: 1 if 'Dem' in x else 0)
    df['legis_control_rep'] = df['Legis_Control'].apply(lambda x: 1 if 'Rep' in x else 0)
    df['gov_party_dem'] = df['Gov_Party'].apply(lambda x: 1 if x == 'Dem' else 0)
    df['gov_party_rep'] = df['Gov_Party'].apply(lambda x: 1 if x == 'Rep' else 0)
    df['state_control_dem'] = df['State_Control'].apply(lambda x: 1 if x == 'Dem' else 0)
    df['state_control_rep'] = df['State_Control'].apply(lambda x: 1 if x == 'Rep' else 0)
    return df 




if __name__ == '__main__':



    file_paths = ['2015.csv','2016.csv','2017.csv','2018.csv','2019.csv','2020.csv']
    df =main(file_paths)
    df.to_pickle('../data/makeup.pkl')
