from bs4 import BeautifulSoup
import requests
import pandas as pd


URL_INFO = {
    'URL': 'https://www.slickcharts.com/',
    'HEADER': {'User-Agent': 'Mozilla/5.0'},
    'PARSER': 'lxml',
    'TAG': 'table',
    'ATTRS': 'table table-hover table-borderless table-sm'
            }

INDEXES = {'SP500': 'sp500',
           'NASDAQ': 'nasdaq100',
           'DOWJONES': 'dowjones'}

COLUMNS = ['#', 'Company', 'Symbol', 'Weight', 'Price']


def extract_web_data(index):
    response = requests.get(URL_INFO['URL'] + index, headers=URL_INFO['HEADER'])

    soup = BeautifulSoup(response.text, URL_INFO['PARSER'])
    index_info = soup.find(URL_INFO['TAG'], class_=URL_INFO['ATTRS'])

    df = pd.read_html(str(index_info))[0]
    return df[COLUMNS]

