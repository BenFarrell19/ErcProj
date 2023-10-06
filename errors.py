from selenium import webdriver
import json
import os
from time import sleep
from selenium import *
import pandas as pd

browser = webdriver.Chrome(
    executable_path=os.path.abspath("C:/Users/Ben Farrell/PycharmProjects/test/chromedriver.exe"))

error_urls = json.load(open('duberrors_file', 'r'))
errors = []
eps_dic = {}
main = []
c = -1
for i in error_urls:
    c += 1
    try:
        if i[1] == 0:
            i[0] = i[0] + '/earnings'
        browser.get(i[0])
        sleep(4)
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

            key = error_urls[c][0].split("/")
            key = key[5]
            eps_dic[key] = {'company': key,
                            'Date': date.text,
                            'est. eps': est_eps.text,
                            'rep. eps': rep_eps.text,
                            'est. rev.': est_rev.text,
                            'act. rev.': act_rev.text}
            main.append(eps_dic[key])

    except:
        try:
            browser.refresh()
            sleep(4)
            for e in range(2, 29):
                if e == 12:
                    continue
                sleep(2)
                date = browser.find_element_by_xpath(
                    '//*[@id="cphPrimaryContent_tabEarningsHistory"]/div[5]/div/table/tbody/tr[{}]/td[1]'.format(e))
                est_eps = browser.find_element_by_xpath(
                    '//*[@id="cphPrimaryContent_tabEarningsHistory"]/div[5]/div/table/tbody/tr[{}]/td[3]'.format(e))
                rep_eps = browser.find_element_by_xpath(
                    '//*[@id="cphPrimaryContent_tabEarningsHistory"]/div[5]/div/table/tbody/tr[{}]/td[4]'.format(e))
                est_rev = browser.find_element_by_xpath(
                    '//*[@id="cphPrimaryContent_tabEarningsHistory"]/div[5]/div/table/tbody/tr[{}]/td[6]'.format(e))
                act_rev = browser.find_element_by_xpath(
                    '//*[@id="cphPrimaryContent_tabEarningsHistory"]/div[5]/div/table/tbody/tr[{}]/td[7]'.format(e))
                key = error_urls[c][0].split("/")
                key = key[5]
                eps_dic[key] = {'company': key,
                                'Date': date.text,
                                'est. eps': est_eps.text,
                                'rep. eps': rep_eps.text,
                                'est. rev.': est_rev.text,
                                'act. rev.': act_rev.text}
                main.append(eps_dic[key])
        except Exception as e:
            errors.append(e)
            print(browser.current_url, "\n", e)
            continue
print(errors)
print(len(errors))
json.dump(main, open('scraped_data_2', 'w'))