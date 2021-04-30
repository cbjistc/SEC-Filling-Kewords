#This part is used to get keyword information. 
import pandas as pd
import requests
import os 
from bs4 import BeautifulSoup
import urllib.request 
from pathlib import Path
import pathlib

file_dir = f"{position}/10K"
i =1
for root, dirs, files in os.walk(file_dir):  
    i +=1
    for file in files:
        position = root + '/' + file
        if '.DS_Store' not in position:
            key_paragraph =''
            with open(position) as f:
                contents = f.read()
            result = contents.split("\n\n")
            for paragraph in result:
                if '$' in paragraph:
                    if 'credit agreement' in paragraph:
                        key_paragraph = 'credit agreement \n\n' + key_paragraph + paragraph + "\n\n"
                    elif 'credit facilities' in paragraph:
                        key_paragraph = 'credit facilities \n\n' + key_paragraph + paragraph + "\n\n"
                    elif 'credit facility' in paragraph:
                        key_paragraph =  'credit facility \n\n' + key_paragraph + paragraph + "\n\n"
                    elif 'revolving credit' in paragraph:
                        key_paragraph = 'revolving credit \n\n' + key_paragraph + paragraph + "\n\n"
                    elif 'borrowings outstanding' in paragraph:
                        key_paragraph = 'borrowings outstanding \n\n' + key_paragraph + paragraph + "\n\n"
                    elif 'borrowing capacity' in paragraph:
                        key_paragraph = 'borrowing capacity \n\n' + key_paragraph + paragraph + "\n\n"
                    elif 'liquidity' in paragraph:
                        key_paragraph = 'liquidity \n\n' + key_paragraph + paragraph + "\n\n"
                    elif 'capital resources' in paragraph: 
                        key_paragraph = 'capital resources \n\n' + key_paragraph + paragraph + "\n\n"                        
            f.close()
            
            cik = root.split('/')[-1]
            pathlib.Path(f"{position}/keywords/{cik}").mkdir(parents=True, exist_ok=True) 
            fiscal_date = file[:-4]
            with open(f"{position}/keywords/{cik}/{fiscal_date}.txt", "w") as f:
                f.write(key_paragraph)
            f.close()