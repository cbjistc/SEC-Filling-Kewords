#This Part is used to get related filling
#Import Package
import pandas as pd
import requests
import os 
from bs4 import BeautifulSoup
import urllib.request 
from pathlib import Path
import pathlib

#Please set your saving position in here. 
position = ''

#Reading releated companies' filling documents. (Please use the CIK words.)                                                                                              
df = pd.read_csv(f'{position}/Company/firm_list_example.txt', sep=" ", header=None)
ciks = list(df[0])
#Setting your header to avoid block.
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36',
}

base_url_sec = 'https://www.sec.gov'
result = []
for cik in ciks:
    link = f'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={cik}&type=10-k&dateb=20070101&owner=exclude&start=&output=&count=100'
    response = requests.get(link,headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    doc_table = soup.find_all('table', class_='tableFile2')
    for row in doc_table[0].find_all('tr'):  
        filing = []
        cols = row.find_all('td')
        if len(cols) != 0:
            filing_type = cols[0].text.strip()                 
            filing_date = cols[3].text.strip()
            filing_numb = cols[4].text.strip()
            filing_doc = cols[1].find('a',{'href':True})

            if filing_doc != None:
                filing_doc_link = base_url_sec + filing_doc['href'] 
            else:
                filing_doc_link = 'no link'
            
            if filing_doc_link != 'no link':
                response = requests.get(filing_doc_link,headers=headers)
                soup = BeautifulSoup(response.content, 'html.parser')

                date = soup.find_all('div',{'class':'info'})
                fiscal_date = date[3].text.strip()

                file_table = soup.find_all('table', class_='tableFile')

                filing_link = base_url_sec + file_table[0].find_all('tr')[-1].find_all('td')[2].find('a',{'href':True})['href']
                f10_K = requests.get(filing_link, headers=headers)
                pathlib.Path(f"{position}/10K/{cik}").mkdir(parents=True, exist_ok=True) 
                with open(f"{position}/10K/{cik}/{fiscal_date}.txt", "w") as f:
                    f.write(f10_K.text)

            filing.append(cik)
            filing.append(filing_date)
            filing.append(fiscal_date)
            filing.append(filing_type)
            filing.append(filing_doc_link)
            filing.append(filing_link)

        result.append(filing)

df = pd.DataFrame(result,columns=['CIK', 'Filing Date', 'Fiscal Date','Filing Type','All Filing Link','10K Link'])
writer = pd.ExcelWriter(f'{position}/CIK_SEC_Sample.xlsx', engine='xlsxwriter')
df.to_excel(writer, sheet_name='CIK', index=False)
writer.save()
