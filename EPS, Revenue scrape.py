from selenium import webdriver
import json
import os
from time import sleep
from selenium import *
import pandas as pd

browser = webdriver.Chrome(executable_path=os.path.abspath("C:/Users/Ben Farrell/PycharmProjects/test/chromedriver.exe"))

# creating list of S&P 500 ticker symbols
browser.get("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
sleep(2)
ticker_lst = []
c = 0
# 505
for i in range(1, 505):
    c += 1
    elem = browser.find_element_by_xpath('//*[@id="constituents"]/tbody/tr[{}]/td[1]/a'.format(c))
    ticker_lst.append(elem.text)

print(ticker_lst)
print(len(ticker_lst))
base_url = "https://www.marketbeat.com/stocks/"
error_urls = {}
main = []
eps_dic = {}
json.dump(ticker_lst, open('ticker list', 'w'))
# 504
for i in range(504):
    try:
        browser.get(base_url + ticker_lst[i])
        sleep(1)
        button = browser.find_element_by_xpath('//*[@id="tabEarnings"]')
        button.click()
        sleep(2)
    except Exception as e:
        error_urls[ticker_lst[i]] = [browser.current_url, 0]
        print(browser.current_url, "clicking earnings error ", e)
        continue

    try:
        for e in range(2, 29):
            if e == 12:
                continue
            date = browser.find_element_by_xpath(
                '//*[@id="cphPrimaryContent_tabEarningsHistory"]/div[6]/div/table/tbody/tr[{}]/td[1]'.format(e))
            est_eps = browser.find_element_by_xpath(
                '//*[@id="cphPrimaryContent_tabEarningsHistory"]/div[6]/div/table/tbody/tr[{}]/td[3]'.format(e))
            rep_eps = browser.find_element_by_xpath(
                '//*[@id="cphPrimaryContent_tabEarningsHistory"]/div[6]/div/table/tbody/tr[{}]/td[4]'.format(e))
            est_rev = browser.find_element_by_xpath(
                '//*[@id="cphPrimaryContent_tabEarningsHistory"]/div[6]/div/table/tbody/tr[{}]/td[6]'.format(e))
            act_rev = browser.find_element_by_xpath(
                '//*[@id="cphPrimaryContent_tabEarningsHistory"]/div[6]/div/table/tbody/tr[{}]/td[7]'.format(e))

            eps_dic[ticker_lst[i]] = {'company': ticker_lst[i],
                                      'Date': date.text,
                                      'est. eps': est_eps.text,
                                      'rep. eps': rep_eps.text,
                                      'est. rev.': est_rev.text,
                                      'act. rev.': act_rev.text}
            main.append(eps_dic[ticker_lst[i]])
    except Exception as e:
        error_urls[ticker_lst[i]] = [browser.current_url, 1]
        print(browser.current_url, "scraping earnings tbody error", e)
        continue

if len(error_urls) > 0:
    val = error_urls.values()
    values = list(val)
    keys = list(error_urls)
    dub_errors = []

    for i in range(len(error_urls)):
        try:
            browser.get(values[i][0])
            sleep(2)
            if values[i][1] == 1:
                for e in range(2, 30):
                    date = browser.find_element_by_xpath(
                        '//*[@id="cphPrimaryContent_tabEarningsHistory"]/div[6]/div/table/tbody/tr[{}]/td[1]'.format(e))
                    est_eps = browser.find_element_by_xpath(
                        '//*[@id="cphPrimaryContent_tabEarningsHistory"]/div[6]/div/table/tbody/tr[{}]/td[3]'.format(e))
                    rep_eps = browser.find_element_by_xpath(
                        '//*[@id="cphPrimaryContent_tabEarningsHistory"]/div[6]/div/table/tbody/tr[{}]/td[4]'.format(e))
                    est_rev = browser.find_element_by_xpath(
                        '//*[@id="cphPrimaryContent_tabEarningsHistory"]/div[6]/div/table/tbody/tr[{}]/td[6]'.format(e))
                    act_rev = browser.find_element_by_xpath(
                        '//*[@id="cphPrimaryContent_tabEarningsHistory"]/div[6]/div/table/tbody/tr[{}]/td[7]'.format(e))

                    eps_dic[ticker_lst[i]] = {'company': ticker_lst[i],
                                              'Date': date.text,
                                              'est. eps': est_eps.text,
                                              'rep. eps': rep_eps.text,
                                              'est. rev.': est_rev.text,
                                              'act. rev.': act_rev.text}
                    main.append(eps_dic[ticker_lst[i]])
            else:
                button = browser.find_element_by_xpath('//*[@id="tabEarnings"]')
                button.click()
                sleep(2)
                for e in range(2, 29):
                    date = browser.find_element_by_xpath(
                        '//*[@id="cphPrimaryContent_tabEarningsHistory"]/div[6]/div/table/tbody/tr[{}]/td[1]'.format(e))
                    est_eps = browser.find_element_by_xpath(
                        '//*[@id="cphPrimaryContent_tabEarningsHistory"]/div[6]/div/table/tbody/tr[{}]/td[3]'.format(e))
                    rep_eps = browser.find_element_by_xpath(
                        '//*[@id="cphPrimaryContent_tabEarningsHistory"]/div[6]/div/table/tbody/tr[{}]/td[4]'.format(e))
                    est_rev = browser.find_element_by_xpath(
                        '//*[@id="cphPrimaryContent_tabEarningsHistory"]/div[6]/div/table/tbody/tr[{}]/td[6]'.format(e))
                    act_rev = browser.find_element_by_xpath(
                        '//*[@id="cphPrimaryContent_tabEarningsHistory"]/div[6]/div/table/tbody/tr[{}]/td[7]'.format(e))

                    eps_dic[ticker_lst[i]] = {'Date': date.text,
                                              'est. eps': est_eps.text,
                                              'rep. eps': rep_eps.text,
                                              'est. rev.': est_rev.text,
                                              'act. rev.': act_rev.text}
                    main.append(eps_dic[ticker_lst[i]])
        except:
            dub_errors.append(values[i])
            print(values[i], "DUB ERROR, see file")

    if len(dub_errors) > 0:
        json.dump(dub_errors, open('duberrors_file', 'w'))
        print(json.load(open('duberrors_file', 'r')))

json.dump(main, open('scraped_data', 'w'))
print(json.load(open('scraped_data', 'r')))

# ticker list file
json.dump(ticker_lst, open('ticker list', 'w'))