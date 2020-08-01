#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
PubMed Article Search and Download Python Script (Ver 0.1)
"""

# import modules
import sys
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import argparse
from tqdm import tqdm
import requests
import time
import urllib.request
from urllib.parse import quote
from selenium.webdriver.common.action_chains import ActionChains
from PIL import Image
import textwrap

class pmExt:
    def __init__(self):
        pass

    def ext_article(self, keywords, itemN):
        # make directory
        self.create_dir(root_dir, keywords)
        title_list = []
        doi_list = []
        abstract_list = []
        citation_list = []
        figure_list = []
        # scrolling google browser
        try:
            # browser extraction part ####
            chrome_opt = webdriver.ChromeOptions()
            chrome_opt.add_argument('--disable-gpu')
            pathx = "/Users/uksu/Downloads/chromedriver"
            browser = webdriver.Chrome(executable_path=pathx,options=chrome_opt)
            ActionChains(browser).key_down(Keys.CONTROL).click().key_up(Keys.CONTROL).perform()
            url = 'https://pubmed.ncbi.nlm.nih.gov/?term=' + quote(keywords.encode('utf-8')) + '&size=20'
            browser.get(url)
            time.sleep(1)
            element = browser.find_element_by_tag_name("body")

            # Searching environment setting
            elementx = browser.find_element_by_xpath('//*[@id="static-filters-form"]/div/div[1]/div[1]/ul/li[1]/label')
            browser.execute_script("arguments[0].click();", elementx)
            time.sleep(1)
            elementx = browser.find_element_by_xpath('//*[@id="static-filters-form"]/div/div[1]/div[1]/ul/li[2]/label')
            browser.execute_script("arguments[0].click();", elementx)
            time.sleep(1)
            elementx = browser.find_element_by_xpath('//*[@id="static-filters-form"]/div/div[1]/div[1]/ul/li[3]/label')
            browser.execute_script("arguments[0].click();", elementx)
            time.sleep(1)

            # click first article
            elementx = browser.find_element_by_xpath('//*[@id="search-results"]/section/div[1]/div/article[1]/div[2]/div[1]/a')
            browser.execute_script("arguments[0].click();", elementx)
            first_article = browser.find_element_by_xpath('//*[@id="adjacent-navigation"]/div[2]/a/span[2]')
            browser.execute_script("arguments[0].click();", first_article)
            time.sleep(1)
            first_article = browser.find_element_by_xpath('//*[@id="adjacent-navigation"]/div[2]/a/span[2]')
            browser.execute_script("arguments[0].click();", first_article)
            time.sleep(1)
            ## extract first article
            # title_list
            t_path = '//*[@id="full-view-heading"]/h1'
            title_link = browser.find_element_by_xpath(t_path)
            title_list_tmp = title_link.text
            title_list.append(title_list_tmp)

            # citation list
            try:
                c_path = '//*[@id="citedby"]/h2/em[1]'
                citation_link = browser.find_element_by_xpath(c_path)
                citation_list_tmp = citation_link.text
                citation_list.append(citation_list_tmp)
            except:
                print("!! No citation of this paper !!")
                citation_list_tmp = '0'
                citation_list.append(citation_list_tmp)

            # doi_list
            d_path = '//*[@id="full-view-identifiers"]/li[2]/span/a'
            doi_link = browser.find_element_by_xpath(d_path)
            doi_list_tmp = doi_link.get_attribute('href')
            doi_list.append(doi_list_tmp)

            # abstract_list
            a_path = '//*[@id="enc-abstract"]/p'
            abstract_link = browser.find_element_by_xpath(a_path)
            abstract_list_tmp = abstract_link.text
            abstract_list.append(abstract_list_tmp)

            # figure_list
            j = 1
            while j < 10:
                try:
                    f_path = '//*[@id="slides-container"]/figure['+ str(j) + ']/a'
                    figure_link = browser.find_element_by_xpath(f_path)
                    figure_list_tmp = figure_link.get_attribute('href')
                    figure_list.append(figure_list_tmp)
                except:
                    print("!! No more figures in this paper !!")
                    figure_list.append('no_fig')
                    # figure_list.remove('no_fig')
                j += 1
            time.sleep(1)
            # go to next article
            next_article = browser.find_element_by_xpath('//*[@id="adjacent-navigation"]/div[2]/a/span[2]')
            browser.execute_script("arguments[0].click();", next_article)
            time.sleep(1)
        except Exception as e:
            print(e)
        ## main run
        i = 0
        while i < itemN:
            # title_list
            t_path = '//*[@id="full-view-heading"]/h1'
            title_link = browser.find_element_by_xpath(t_path)
            title_list_tmp = title_link.text
            title_list.append(title_list_tmp)

            # citation list
            try:
                c_path = '//*[@id="citedby"]/h2/em[1]'
                citation_link = browser.find_element_by_xpath(c_path)
                citation_list_tmp = citation_link.text
                citation_list.append(citation_list_tmp)
            except:
                print("!! No citation of this paper !!")
                citation_list_tmp = '0'
                citation_list.append(citation_list_tmp)

            # doi_list
            d_path = '//*[@id="full-view-identifiers"]/li[2]/span/a'
            doi_link = browser.find_element_by_xpath(d_path)
            doi_list_tmp = doi_link.get_attribute('href')
            doi_list.append(doi_list_tmp)

            # abstract_list
            a_path = '//*[@id="enc-abstract"]/p'
            abstract_link = browser.find_element_by_xpath(a_path)
            abstract_list_tmp = abstract_link.text
            abstract_list.append(abstract_list_tmp)

            # figure_list
            j = 1
            while j < 10:
                try:
                    f_path = '//*[@id="slides-container"]/figure['+ str(j) + ']/a'
                    figure_link = browser.find_element_by_xpath(f_path)
                    figure_list_tmp = figure_link.get_attribute('href')
                    figure_list.append(figure_list_tmp)
                except:
                    print("!! No more figures in this paper !!")
                    figure_list.append('no_fig')
                    # figure_list.remove('no_fig')

                j += 1
            # go to next article
            next_article = browser.find_element_by_xpath('//*[@id="adjacent-navigation"]/div[3]/a/span[2]')
            browser.execute_script("arguments[0].click();", next_article)
            time.sleep(0.5)
            i += 1

        return title_list, citation_list, doi_list, abstract_list, figure_list

    def create_dir(self, root_dir, name):
        try:
            if not os.path.exists(root_dir):
                os.makedirs(root_dir)
                time.sleep(0.2)
                path = (name)
                sub_directory = os.path.join(root_dir, path)
                if not os.path.exists(sub_directory):
                    os.makedirs(sub_directory)
            else:
                path = (name)
                sub_directory = os.path.join(root_dir, path)
                if not os.path.exists(sub_directory):
                    os.makedirs(sub_directory)

        except OSError as e:
            if e.errno != 17:
                raise
            pass
        return

# HELP Section
parser = argparse.ArgumentParser(description='## Search and Extract Papers using PubMed Engine ##', formatter_class=argparse.RawDescriptionHelpFormatter,
                                 epilog='''\
version history:
    [ver0.10]       release of this script (2020.08.01)

++ Copyright at uschoi@nict.go.jp / qtwing@naver.com ++
''')
# parser.add_argument("Keyword", help="Keywords without space",)
# parser.add_argument("Item_number", help="Searching item number")
# parser.add_argument("URL_output.txt", help="URL text files")
parser.add_argument('--version', action='version', version='Version 0.1')
parser.parse_args()

# assign input arguments
print("+++++++++++++++++++++++++++++++++++++++++++++")
keyword = input('## Enter the keywords:  ')
print("+++++++++++++++++++++++++++++++++++++++++++++")
itemN = input('## How many articles do you want ?:  ')
print("+++++++++++++++++++++++++++++++++++++++++++++")

# root directiory
root_dir = "PubMed_Reports/"

# MAIN RUN
response = pmExt
title_list, citation_list, doi_list, abstract_list, figure_list = response().ext_article(keyword, int(itemN))

# set path
path = root_dir + keyword

# link downloads
print("")
print(" +++++++++++++++++++++++++++++++++++++ NOW Processing IS STARTING +++++++++++++++++++++++++++++++++++++ ")
print("")
print(" [ Now downloading article information !! ] ")
print(" ")
with open(os.path.join('./' + root_dir + '/', keyword + '.txt'), 'w', encoding="utf-8") as f:
    pbar = enumerate(tqdm(title_list))
    for item_ind, item in pbar:
        f.write("%s\n" % "      ")
        f.write("[Article" + "-" + '%04d' %(item_ind + 1) + "]: " + "%s\n" % textwrap.fill(item, width=150))
        f.write("Citation" + ": " + "%s\n" % textwrap.fill(citation_list[item_ind], width=150))
        f.write("doi" + ": " + "%s\n" % textwrap.fill(doi_list[item_ind], width=150))
        f.write("%s\n" % textwrap.fill(abstract_list[item_ind], width=150))
        f.write("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        f.write("%s\n" % "      ")
        time.sleep(0.01)

# print(figure_list)
# save figure
print(" ")
print(" [ Now downloading article figures !! ] ")
print(" ")
pbar2 = enumerate(tqdm(figure_list))
indN = len(title_list) + 1

n_tmp = 0
ind2_tmp = 1
fig_mark = 0
nofig_mark = 0
for item_ind2, item2 in pbar2:
    if 'no_fig' not in item2:
        filename = "Article" + "_" + '%04d' % (n_tmp + 1) + "_Fig" + '%02d' % (ind2_tmp) + ".jpg"
        urllib.request.urlretrieve(item2, os.path.join(path, filename))
        fig_mark += 1
    else:
        nofig_mark += 1
        ind2_tmp = 0
    mark_diff = item_ind2 - (nofig_mark+fig_mark)
    ind2_tmp = ind2_tmp + 1
    n_tmp = round((item_ind2 - ind2_tmp + 1 - mark_diff)/9)

print("")
print(" +++++++++++++++++++++++++++++++++++++ NOW EXTRACTION FINISHED ++++++++++++++++++++++++++++++++++++++++ ")
print("")























#
