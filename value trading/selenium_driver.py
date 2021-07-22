#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  2 18:23:23 2020

@author: nishant.gupta
"""

import time 
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

class selenium_driver:
    def __init__(self, url, num_retries):
        self.url = url
        self.num_retries = num_retries
    
    def get_driver(self):
        driver = webdriver.Chrome(ChromeDriverManager().install())
        return driver
    
    def get_driver_old():
        driver = webdriver.Chrome('/Users/nishant.gupta/Downloads/chromedriver')
        return driver
    
    def find_xpath(self, element_xpath, click_xpath = ""):
        result = ""
        try:
            driver = self.get_driver()
            driver.implicitly_wait(20)
            driver.get(self.url)
            
            if (click_xpath != ""):
                print("Searching for click xpath: " + click_xpath)
                driver.find_element_by_xpath(click_xpath).click()
                # if click_xpath is given we click that element and wait for the required tag to be visible 
                ctr = 0
                # We are using thread.sleep temporarily because of the issue mentioned here:
                # https://stackoverflow.com/questions/45347675/make-selenium-wait-10-seconds
                while (ctr < self.num_retries):
                    print("Searching for element: " + element_xpath + " retry num: " + str(ctr))
                    web_element = driver.find_element_by_xpath(element_xpath)
                    if (web_element.text == "") :
                        ctr += 1
                        print("Will retry after 2 sec")
                        time.sleep(2)
                    else:
                        print("Found web element for xpath: " + element_xpath)
                        result = web_element.text
                        break
            else:
                # no click tag given so we simply seach for the element_xpath
                # Note that we don't have any retries here as we already have an implicit wait in the driver
                print("Searching for element: " + element_xpath)
                
                # TODO: We can think of removing the click_xpath we have above by having a sleep for some seconds
                # Click was most probably needed because we are trying to read an xpath element before page has
                # loaded completely and hence putting a sleep might help
                time.sleep(5)
                web_element = driver.find_element_by_xpath(element_xpath)
                result = web_element.text
            
            driver.quit()
            return result
        except Exception as e:
            print("Encountered exception: ", e)
            print("Got some error while finding " + element_xpath + " on url: " + self.url + \
                  " with click_xpath " + click_xpath)
            return result
    
    def get_content_by_searching(self, search_box_xpath, element_key, search_box_click_xpath):
        # Once we get the page content through selenium we use beautiful soup on the content
        # This is done presently for beta as we are not able to get corresponding web element through
        # selenium find_element_by_xpath api
        content = ""
        ctr = 0
        while (ctr < self.num_retries):
            driver = self.get_driver()
            driver.implicitly_wait(10)
            driver.get(self.url)
            try:
                # Enter the element_key in the search box and click search
                driver.find_element_by_xpath(search_box_xpath).send_keys(element_key)
                driver.find_element_by_xpath(search_box_click_xpath).click()
                time.sleep(10)
                content = driver.execute_script("return document.documentElement.outerHTML")
                driver.quit()
                return content
            except:
                print("Encountered some error in get_content_by_searching.. retry num: ", str(ctr))
            ctr += 1
            driver.quit()

        return content
    
    def get_element_by_searching(self, search_box_xpath, element_key, search_box_click_xpath, element_xpath):
        result = ""
        ctr = 0
        while (ctr < self.num_retries):
            driver = self.get_driver()
            driver.implicitly_wait(10)
            driver.get(self.url)
            try:
                # Enter the element_key in the search box and click search
                driver.find_element_by_xpath(search_box_xpath).send_keys(element_key)
                driver.find_element_by_xpath(search_box_click_xpath).click()
                time.sleep(10)
                result = driver.find_element_by_xpath(element_xpath).text
                driver.quit()
                return result
            except:
                print("Encountered some error in get_content_by_searching.. retry num: ", str(ctr))
            ctr += 1
            driver.quit()

        return result
            
            