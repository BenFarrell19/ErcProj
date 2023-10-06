import requests
from selenium import webdriver
import json
import datetime
import os
import ast
from time import sleep
import pandas as pd


# need to get list of 5000 largest cap stocks and 5000 stocks with most daily trading volume
# then compare and create new list

# collecting ticker symbols
browser = webdriver.Chrome(
    executable_path=os.path.abspath("C:/Users/Ben Farrell/Downloads/chromedriver_win32 (1)/chromedriver.exe"))

# creating list of S&P 500 ticker symbols
browser.get("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
sleep(2)
ticker_lst = []
c = 0
for i in range(1, 505):
    c += 1
    elem = browser.find_element_by_xpath('//*[@id="constituents"]/tbody/tr[{}]/td[1]/a'.format(c))
    ticker_lst.append(elem.text)

# ticker list file creation
json.dump(ticker_lst, open('ticker list', 'w'))


def utc_dt(dt):
    """
    :param dt: iso 8602 timestamp object from estimize data
    :return: utc datetime object
    """
    fm = '%Y-%m-%dT%H:%M:%S%z'
    dt = datetime.datetime.strptime(dt, fm)
    dt = dt.timestamp()
    dt = datetime.datetime.utcfromtimestamp(dt)
    return dt


# function to call earnings releases endpoint from estimize api
headers = {"X-Estimize-Key": "29ae555ddfc3709251c82e23", "content-type": "application/json"}
lst = []


def get_company_financials(ticker):
    data = requests.get('https://api.estimize.com/companies/{}/releases'.format(ticker), headers=headers).json()
    data.append(ticker)
    lst.append(data)


# no data list:
no_data_lst = []
# calling api

for i in ticker_lst:
    sleep(1)
    try:
        get_company_financials(i)
    except Exception as e:
        print(e, i)
        no_data_lst.append(i)

# creation of uncleaned data file and companies with no data

json.dump(no_data_lst, open('no data companies', 'w'))
json.dump(lst, open('estimize_data', 'w'))

# cleaning data
# NEED TO GET NULL VALUES AS STRINGS AUTOMATICALLY

with open('estimize_data', 'r') as f:
    file = ast.literal_eval(f.read())

# makes key value pairs for each feature of estimize data and puts in another dictionary so each quarter has a ticker
main_lst = []
c = 0
for lst in file:
    for i in lst:
        if type(i) == dict:
            if 2020 > i["fiscal_year"] > 2010:
                c += 1
                main_dic = {lst[-1]: {'fiscal year': i["fiscal_year"],
                                      'fiscal quarter': i["fiscal_quarter"],
                                      'reported eps': i["eps"],
                                      'estimated eps': i["wallstreet_eps_estimate"],
                                      'reported revenue': i["revenue"],
                                      'estimated revenue': i["wallstreet_revenue_estimate"],
                                      'released': str(
                                          utc_dt(i["release_date"]))}}  # take original iso 8601 and turns to just utc and strong for json encoding
                main_lst.append(main_dic)

# storing cleaned data
json.dump(main_lst, open('clean quarterlies', 'w'))


