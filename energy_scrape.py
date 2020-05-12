import numpy as np 
import pandas as pd
from bs4 import BeautifulSoup
import codecs 
import requests 
from time import sleep


class Scraper():

    def __init__(self,bill_csv,bill_html):
        self.bill_csv = bill_csv 
        self.bill_html = bill_html 

    
    def get_data(self):

        doc = np.genfromtxt(self.bill_csv, dtype = str, delimiter = '\t')
        ########################TEST############################
        bill_text_lookup = np.where(doc == 'BILL TEXT LOOKUP')[0]
        state_seperator = bill_text_lookup - 1
        bad_cells = np.concatenate([bill_text_lookup,state_seperator])
        doc = np.delete(doc,bad_cells)
        ######################TEST############################3
        records = []
        row = []
        for cell in doc:
            if cell[:8] == "History:":
                records.append(row)
                row = []
            else:
                row.append(cell)
        self.records = records 

    @staticmethod 
    def _find_additional_authors(cell):
        idx = cell.find(':')
        if idx == -1:
            return None 
        else: 
            return cell[idx + 2:]

    @staticmethod 
    def _clean_authors(cell):
        idx = cell.find('Additional Authors')
        if idx == -1:
            return cell
        else:
            return cell[:idx -1]

    def to_dataframe(self):

        df = pd.DataFrame(columns = ['bill_id','title','year','status','author',
                                    'topics','summary','associated bills',
                                    'date of last action'])
        row_dict = {}
        for row in self.records:
            row_dict = {'bill_id':row.pop(0), 'year' : row.pop(0), 'title':row.pop(0)}
            for cell in row:
                idx = cell.find(':')
                if idx != -1:
                    row_dict[cell[:idx].lower().replace('"','')] = cell[idx + 2:]
            df = df.append([row_dict])
            row_dict = {}

        df['additional_authors'] = df['author'].apply(lambda x: Scraper._find_additional_authors(x))
        df['temp_author'] = df['author'].apply(lambda x: Scraper._clean_authors(x))

        df.drop('author', axis =1,inplace = True)

        df.rename(columns = {'associated bills':'associated_bills',
                            'date of last action' : 'date_of_last_action',
                            'temp_author' : 'author'}, inplace = True)
        self.data = df

    def get_bill_links(self):
        html = codecs.open(self.bill_html, "r", "utf-8")
        soup = BeautifulSoup(html.read(),'html.parser')
        links = [list(link.children)[0] for link in soup.find_all('a',href=True)]

        bill_links = [str(link) for link in links if 'custom.statenet.com' in link] 
        ########################### Remove the [:10]
        self.data['bill_links'] = bill_links
        self.bill_links = bill_links

    @staticmethod
    def _grab_one_bill_text(html_link):
        sleep(2)
        try:
            print(html_link)
            page = requests.get(html_link)
            print(page.status_code)
            soup = BeautifulSoup(page.content,'html.parser')
            text = soup.find_all(class_ = 'text')[0].text
            text_string = str(text)
        except:
            text_string = None
        return text_string
    
    def get_bill_text(self):
        self.data['text'] = self.data['bill_links'].apply(lambda x: Scraper._grab_one_bill_text(x))


if __name__ == '__main__':


    # bill_csv_path = 'data/Prescription Drug Bills All - Sheet1.tsv'
    # bill_html_path = 'data/view-source_https___www.ncsl.org_research_health_prescription-drug-statenet-database.aspx.html'
    bill_csv_path = 'data/energy_bills_2015 - Sheet1.tsv'
    bill_html_path = 'data/energy_2015.html'
    scrape = Scraper(bill_csv_path, bill_html_path)
    scrape.get_data()
    scrape.to_dataframe()
    scrape.get_bill_links()
    scrape.get_bill_text()
    scrape.data.to_pickle('energy_2015.pkl')
#doc = np.genfromtxt('Prescription Drug Bills - Sheet1.csv',dtype = str,delimiter = '\t')
#page = requests.get(bill_links[0])
#soup = BeautifulSoup(page.content,'html.parser')