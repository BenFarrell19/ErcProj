import requests
import json
import pandas as pd
from time import sleep
import ast

'''
headers = {"X-Estimize-Key": "29ae555ddfc3709251c82e23", "content-type": "application/json"}

lst = []


def get_company_financials(ticker):
    data = requests.get('https://api.estimize.com/companies/{}/releases'.format(ticker), headers=headers).json()
    data.append(ticker)
    lst.append(data)


ticker_lst = json.load(open('ticker list', 'r'))

c = 0
for i in ticker_lst:
    c += 1
    if c < 3:
        sleep(1)
        get_company_financials(i)

json.dump(lst, open('estimize_data', 'w'))
'''

with open('estimize_data', 'r') as f:
    file = ast.literal_eval(f.read())


main_lst = []
c = 0
for lst in file:
    print(lst)
    for i in lst:
        if type(i) == dict:
            if 2020 > i["fiscal_year"] > 1999:
                c += 1
                main_dic = {lst[-1]: {'fiscal year': i["fiscal_year"],
                                      'fiscal quarter': i["fiscal_quarter"],
                                      'reported eps': i["eps"],
                                      'estimated eps': i["wallstreet_eps_estimate"],
                                      'reported revenue': i["revenue"],
                                      'estimated revenue': i["wallstreet_revenue_estimate"],
                                      'released': i["release_date"]}}
                print(c, main_dic)
                main_lst.append(main_dic)


print("\n\n\n")
print(main_lst)
json.dump(main_lst, open('clean quarterlies', 'w'))
