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

COLUMNS = ['#', 'Company', 'Symbol', 'Weight', 'Price']


def url_parse(index_name):
    response = requests.get(URL_INFO['URL'] + index_name, headers=URL_INFO['HEADER'])

    soup = BeautifulSoup(response.text, URL_INFO['PARSER'])
    stats = soup.find(URL_INFO['TAG'], class_=URL_INFO['ATTRS'])
    return stats


def stats_load(stats):
    df = pd.read_html(str(stats))[0]
    return df[COLUMNS]
