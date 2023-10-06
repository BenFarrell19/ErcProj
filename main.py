import json
import datetime as dt
import yfinance as yf
import ta
from ta import momentum

# loading cleaned estimize data
lst = json.load(open('clean quarterlies', 'r'))


# function required to find dates
def closest_dates(dates, pivot, n):
    return sorted((d for d in dates if d < pivot), key=lambda t: abs(t - pivot))[:n - 1]


# calculates the average change in eps over last n number of quarters
def eps_change(ticker, start_quarter, n_quarters=6):
    """
    :param ticker: stock ticker symbol
    :param start_quarter: [yyyy, q] ex. [2020, 3]
    :param n_quarters: number of quarters to use in calc, default:6
    :return: returns the average percent change in eps over last n quarters
    """
    # start_quarter format: [2020, 3]
    eps_dates_lst = []
    eps_lst = []
    dates_lst = []
    # creates list of every quarterly release date for given company
    for dic in lst:
        for i in dic:
            if i == ticker:
                temp = dt.datetime.strptime(dic[ticker]['released'], '%Y-%m-%d %H:%M:%S')
                dates_lst.append(temp)
    # takes list of every quarterly release date and finds release date matching given year/quarter
    # then takes release date for given year/quarter and creates list of the n most recent quarters to given
    for dic in lst:
        for i in dic:
            if i == ticker:
                if dic[ticker]['fiscal year'] == start_quarter[0]:
                    if dic[ticker]['fiscal quarter'] == start_quarter[1]:
                        start_date = dic[ticker]['released']
                        start_date = dt.datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S')
                        eps_dates_lst = closest_dates(dates_lst, start_date, n_quarters)
                        eps_dates_lst.insert(0, start_date)
    # takes list of n most recent quarters prior to given and creates list of eps for each of those quarters
    for date in eps_dates_lst:
        for dic in lst:
            for i in dic:
                if i == ticker:
                    if dt.datetime.strptime(dic[ticker]['released'], '%Y-%m-%d %H:%M:%S') == date:
                        eps_lst.insert(0, dic[ticker]['reported eps'])
    # calculates average change between eps in list of eps for quarters prior to given
    temp = []
    for a, b in zip(eps_lst[::1], eps_lst[1::1]):
        temp.append(100 * (b - a) / a)
    avg_eps = sum(temp) / (len(temp))
    return round(avg_eps, 3)


# calculates average percent change in revenue over last n number of quarters for company
def revenue_change(ticker, start_quarter, n_quarters=6):
    """
    :param ticker: stock ticker symbol
    :param start_quarter: [yyyy, q] ex. [2020, 3]
    :param n_quarters: number of quarters to use in calc, default:6
    :return: returns the average percent change in revenue over last n quarters
    """
    # see comments on eps_change to understand this code as its identical just revenue from dictionary instead of eps
    # start_quarter format: [2020, 3]
    revenue_dates_lst = []
    revenue_lst = []
    dates_lst = []
    for dic in lst:
        for i in dic:
            if i == ticker:
                temp = dt.datetime.strptime(dic[ticker]['released'], '%Y-%m-%d %H:%M:%S')
                dates_lst.append(temp)
    for dic in lst:
        for i in dic:
            if i == ticker:
                if dic[ticker]['fiscal year'] == start_quarter[0]:
                    if dic[ticker]['fiscal quarter'] == start_quarter[1]:
                        start_date = dic[ticker]['released']
                        start_date = dt.datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S')
                        revenue_dates_lst = closest_dates(dates_lst, start_date, n_quarters)
                        revenue_dates_lst.insert(0, start_date)
    for date in revenue_dates_lst:
        for dic in lst:
            for i in dic:
                if i == ticker:
                    if dt.datetime.strptime(dic[ticker]['released'], '%Y-%m-%d %H:%M:%S') == date:
                        revenue_lst.insert(0, dic[ticker]['reported revenue'])
    temp = []
    for a, b in zip(revenue_lst[::1], revenue_lst[1::1]):
        temp.append(100 * (b - a) / a)
    avg_revenue = sum(temp) / (len(temp))
    return round(avg_revenue, 3)


def get_price_history(ticker_symbol, start, end, interval):
    ticker_data = yf.Ticker(ticker_symbol)
    df = ticker_data.history(interval=interval, start=start, end=end)
    return df


# yfinance and timedelta use different representation for intervals
intervals = {'1m': 'minutes', '1h': 'hours', '1d': 'days', '1w': 'weeks'}


# price change prior to and after earnings
def earnings_price_change(ticker, quarter, percentage='y', units_prior=5, units_after=5, interval='1d'):
    """
    :param ticker: ticker symbol for stock
    :param quarter: [yyyy, q] ex. [2019, 3]
    :param percentage: have price change in percentage (y/n)? default yes
    :param units_prior: change n days leading up to earnings, default 5
    :param units_after: change n days after earnings, default 5
    :param interval: interval for units, ('1m','1h','1d','1w'), default days
    :return: change in prices of stocks before and after earnings
    """
    # only problem with this functions is the fact that it uses a 24 hour clock while the markets are only open for a few of those hours
    for dic in lst:
        for i in dic:
            if i == ticker:
                if dic[ticker]['fiscal year'] == quarter[0]:
                    if dic[ticker]['fiscal quarter'] == quarter[1]:
                        # release has to be stored as string cause json is stupid and cant encode datetime objects
                        release = dt.datetime.strptime(dic[ticker]['released'], '%Y-%m-%d %H:%M:%S')
                        prior_time = release - dt.timedelta(**{intervals[interval]: units_prior + 1})
                        after_time = release + dt.timedelta(**{intervals[interval]: units_after + 1})
                        chg_prior = get_price_history(ticker, prior_time, release, interval)
                        chg_after = get_price_history(ticker, release, after_time, interval)
                        start_p = chg_after['Open'][0]
                        end_p = chg_after['Close'][-1]
                        percent_chg_after = round(((end_p - start_p) / start_p) * 100, 3)
                        start_a = chg_prior['Open'][0]
                        end_a = chg_prior['Close'][-1]
                        percent_chg_prior = round(((end_a - start_a) / start_a) * 100, 3)
                        if percentage == 'y':
                            result = {'percent change prior to earnings': percent_chg_prior,
                                      'percent change after earnings': percent_chg_after}
                            return result
                        elif percentage == 'n':
                            result = {'point change prior to earnings': end_p - start_p,
                                      'point change after earnings': end_a - start_a}
                            return result


# function to calculate rsi for any stock for any period of units
def Rsi(ticker, start_date, interval='1d', units_prior=30):
    """
    :param ticker: ticker symbol for stock
    :param start_date: date closest to now to have rsi calculation for
    :param interval: interval for units, ('1m','1h','1d','1w'), default days
    :param units_prior: number of units prior to the start to calculate rsi for
    :return: returns dataframe of dates and rsi values for given stock
    """
    # uses 250 days to properly calculate moving averages, closest to td values
    df = get_price_history(ticker, start_date - dt.timedelta(**{intervals[interval]: 250}), start_date, interval)
    rsi = ta.momentum.rsi(df['Close'], 14)
    rsi = rsi[len(rsi) - units_prior:len(rsi)]
    return rsi


# example runs:
'''
a = revenue_change('MMM', [2018, 2], n_quarters=4)
b = eps_change('MMM', [2018, 2], n_quarters=4)
c = earnings_price_change('MMM', [2019, 3], units_prior=24, units_after=9, interval='1h')
r = Rsi('AMD', dt.datetime(2020,7,13), units_prior=5)

print(a)
print(b)
print(c)
print(r)
'''