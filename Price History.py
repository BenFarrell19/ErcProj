import pandas as pd
import datetime
import json
import re
import requests
from time import strftime
from time import sleep
import datetime

ticker_lst = json.load(open('ticker list', 'r'))
data = json.load(open('clean quarterlies', 'r'))

key = 'KGR73YMFH3JOB6JADI79CWKA0FPQPIDL'


def get_price_history(**kwargs):
    url = 'https://api.tdameritrade.com/v1/marketdata/{}/pricehistory'.format(kwargs.get('symbol'))

    params = {}
    params.update({'apikey': key})

    for arg in kwargs:
        parameter = {arg: kwargs.get(arg)}
        params.update(parameter)

    return requests.get(url, params=params).json()


epoch = datetime.datetime.utcfromtimestamp(0)


def unix_time_millis(dt):
    return (dt - epoch).total_seconds() * 1000.0


# one week prior earnings
week_prior_dic = {}
c = 0
for ticker in ticker_lst:
    c += 1
    if c < 3:
        for i in data:
            try:
                dt = i[ticker]["released"]
                dt_mils = unix_time_millis(dt)
                week_prior = dt - datetime.timedelta(days=7)
                week_prior_mils = unix_time_millis(week_prior)
                prices = get_price_history(symbol=i, period=1, periodType='day', frequnecyType='min', startDate=week_prior_mils, endDate=dt_mils)
                week_prior_dic[i[ticker]["released"]] = prices
            except Exception as e:
                print(e)
                continue
print("\n\n\n")
print(week_prior_dic)
# one week after earnings
