#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  2 19:50:03 2020

@author: nishant.gupta
"""

from selenium_driver import selenium_driver
from utils import string_util

class balance_sheet_data_getter:
    def __init__(self, url):
        self.url = url
        self.total_current_assets = []
        self.total_current_liabilities = []
        self.total_liabilities = []
        self.total_stockholders_equity = []
        self.short_term_debt = []
        self.long_term_debt = []
        self.common_stock = []
        
    def get_data(self):
        current_liab_dd = '//*[@id="label_gg5"]/div[1]/a'
        current_liab = '//*[@id="data_ttgg5"]'
        # TODO: Ideally click for dd of current assets should be needed for current assets
        # But somehow that is not working and dd of current liabilities is needed
        # Similar is the case of total liabilities dd
        # current_assets_dd = '//*[@id="label_g1"]/div[1]/a'
        current_assets_dd = '//*[@id="label_gg5"]/div[1]/a'
        current_assets = '//*[@id="data_ttg1"]'
        # liab_dd = '//*[@id="label_g5"]/div[1]/a'
        liab_dd = '//*[@id="label_gg5"]/div[1]/a'
        liab = '//*[@id="data_ttg5"]'
        stock_holders_equity_dd = '//*[@id="label_g8"]/div[1]/a'
        stock_holders_equity = '//*[@id="data_ttg8"]'
        short_term_debt_string = "//div[contains(text(),'Short-term debt')]"
        short_term_debt = '//*[@id="data_i41"]'
        long_term_dd = '//*[@id="label_gg6"]/div[1]/a'
        long_term_debt_string = "//div[contains(text(),'Long-term debt')]"
        long_term_debt = '//*[@id="data_i50"]'
        common_stk = '//*[@id="data_i82"]'
        
        # Now get the data from the url
        driver = selenium_driver(url = self.url, num_retries = 5)
        long_term_debt_present = driver.find_xpath(element_xpath = long_term_debt_string, \
                                          click_xpath = long_term_dd)
        if (long_term_debt_present == ""):
            print("No long term debt on the company")
        else:
            long_term_debt = driver.find_xpath(element_xpath = long_term_debt,\
                                               click_xpath = long_term_dd)
            print("Long term debt: ", long_term_debt)
            self.long_term_debt = string_util.get_processed_data(long_term_debt)

        short_term_debt_present = driver.find_xpath(element_xpath = short_term_debt_string, \
                                          click_xpath = current_liab_dd)
        if (short_term_debt_present == ""):
            print("No short term debt on the company")
        else:
            short_term_debt = driver.find_xpath(element_xpath = short_term_debt,\
                                                click_xpath = current_liab_dd)
            print("Short term debt: ", short_term_debt)
            self.short_term_debt = string_util.get_processed_data(short_term_debt)

        self.total_current_liabilities = string_util.get_processed_data(driver.find_xpath(element_xpath = current_liab,\
                                                           click_xpath = current_liab_dd))
        print("Total current liab: ", self.total_current_liabilities)
        self.total_current_assets = string_util.get_processed_data(driver.find_xpath(element_xpath = current_assets,\
                                                      click_xpath = current_assets_dd))
        print("Total current assets: ", self.total_current_assets)
        self.total_stockholders_equity = string_util.get_processed_data(driver.find_xpath(element_xpath = stock_holders_equity,
                                                           click_xpath = stock_holders_equity_dd))
        print("Total stock holder's equity: ", self.total_stockholders_equity)
        self.total_liabilities = string_util.get_processed_data(driver.find_xpath(element_xpath = liab,\
                                                   click_xpath = liab_dd))
        print("Total liabilites: ", self.total_liabilities)
        
        self.common_stock = string_util.get_processed_data(driver.find_xpath(element_xpath = common_stk))
        print("Common stock: ", self.common_stock)

#balance_sheet_url = 'http://financials.morningstar.com/balance-sheet/bs.html?t=' + '532523' + \
#                                '&region=ind&culture=en-US&platform=sal'
#balance_sheet = balance_sheet_data_getter(balance_sheet_url)
#balance_sheet.get_data()