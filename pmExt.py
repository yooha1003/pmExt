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
import logging
import pytextrank
import spacy
# modules for pdf generation
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph
from reportlab.platypus import SimpleDocTemplate
#


class pmExt:
    def __init__(self):
        pass

    def ext_article(self, keywords, itemN):
        # make directory
        self.create_dir(root_dir, keywords)
        title_list = []
        doi_list = []
        abstract_list = []
        abstract_summary_list = []
        abstract_keyword_list = []
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
            try:
                d_path = '//*[@id="full-view-identifiers"]/li[2]/span/a'
                doi_link = browser.find_element_by_xpath(d_path)
                doi_list_tmp = doi_link.get_attribute('href')
                doi_list.append(doi_list_tmp)
            except:
                doi_list_tmp = "No DOI!!"
                doi_list.append(doi_list_tmp)

            ## abstract_list
            a_path = '//*[@id="enc-abstract"]/p'
            abstract_link = browser.find_element_by_xpath(a_path)
            abstract_list_tmp = abstract_link.text
            abstract_list.append(abstract_list_tmp)

            # abstract_summary
            # load a spaCy model and set the environment
            nlp = spacy.load("en_core_web_sm")
            # logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
            # logger = logging.getLogger("PyTR")
            tr = pytextrank.TextRank(logger=None)
            nlp.add_pipe(tr.PipelineComponent, name="textrank", last=True)
            doc = nlp(abstract_list_tmp)
            # temporary abstract_summary_list
            abstract_summary_list_tmp = [];
            for ab_summary in doc._.textrank.summary(limit_phrases=1, limit_sentences=2):
                abstract_summary_list_tmp.append(ab_summary)
            abstract_summary_list.append(str(abstract_summary_list_tmp))
            # temporary abstract_summary_list
            abstract_keyword_list_tmp = [];
            for phrase in doc._.phrases[:5]: ## top 5 keywords
                abstract_keyword_list_tmp.append(phrase)
            abstract_keyword_list.append(str(abstract_keyword_list_tmp))


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
        while i < itemN - 1:
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
            try:
                d_path = '//*[@id="full-view-identifiers"]/li[2]/span/a'
                doi_link = browser.find_element_by_xpath(d_path)
                doi_list_tmp = doi_link.get_attribute('href')
                doi_list.append(doi_list_tmp)
            except:
                doi_list_tmp = "No DOI!!"
                doi_list.append(doi_list_tmp)

            # abstract_list
            a_path = '//*[@id="enc-abstract"]/p'
            abstract_link = browser.find_element_by_xpath(a_path)
            abstract_list_tmp = abstract_link.text
            abstract_list.append(abstract_list_tmp)

            # load a spaCy model and set the environment
            nlp = spacy.load("en_core_web_sm")
            # logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
            # logger = logging.getLogger("PyTR")
            tr = pytextrank.TextRank(logger=None)
            nlp.add_pipe(tr.PipelineComponent, name="textrank", last=True)
            doc = nlp(abstract_list_tmp)
            # temporary abstract_summary_list
            abstract_summary_list_tmp = [];
            for ab_summary in doc._.textrank.summary(limit_phrases=1, limit_sentences=2):
                abstract_summary_list_tmp.append(ab_summary)
            abstract_summary_list.append(str(abstract_summary_list_tmp))
            # temporary abstract_summary_list
            abstract_keyword_list_tmp = [];
            for phrase in doc._.phrases[:5]: ## top 5 keywords
                abstract_keyword_list_tmp.append(phrase)
            abstract_keyword_list.append(str(abstract_keyword_list_tmp))

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
            try:
                next_article = browser.find_element_by_xpath('//*[@id="adjacent-navigation"]/div[3]/a/span[2]')
                browser.execute_script("arguments[0].click();", next_article)
                time.sleep(0.5)
                i += 1
            except:
                print("### End of the searching pages ###")
                break
        browser.quit()
        return title_list, citation_list, doi_list, abstract_list, abstract_summary_list, abstract_keyword_list, figure_list

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
    [Ver 0.21]       bug fixed for duplicated articles over limit
    [ver 0.20]       added an abstract summary as an output using TextRank algorithm
    [ver 0.10]       release of this script (2020.08.01)

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
title_list, citation_list, doi_list, abstract_list, abstract_summary_list, abstract_keyword_list, figure_list = response().ext_article(keyword, int(itemN))

# set path
path = root_dir + keyword

# link downloads
print("")
print(" +++++++++++++++++++++++++++++++++++++ NOW Processing IS STARTING +++++++++++++++++++++++++++++++++++++ ")
print("")
print(" [ Now downloading article information !! ] ")
# with open(os.path.join('./' + root_dir + '/', keyword + '.txt'), 'w', encoding="utf-8") as f:
#     pbar = enumerate(tqdm(title_list))
#     for item_ind, item in pbar:
#         f.write("%s\n" % "      ")
#         f.write("[ Article" + "-" + '%04d' %(item_ind + 1) + " ]: " + "%s\n" % item)
#         f.write("Citation" + ": " + "%s\n" % textwrap.fill(citation_list[item_ind], width=150))
#         f.write("doi" + ": " + "%s\n" % textwrap.fill(doi_list[item_ind], width=150))
#         f.write("%s\n" % textwrap.fill(abstract_list[item_ind], width=150))
#         f.write("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
#         f.write("%s\n" % "      ")
#         time.sleep(0.01)

# set the template for pdf output
report = SimpleDocTemplate(os.path.join('./' + root_dir + '/' + "pmExt_ArticleReport-" + keyword + '.pdf'), pagesize=A4)
report_style = getSampleStyleSheet()
# report_style.list()
report_style.add(ParagraphStyle(name='Paragraph', spaceAfter=10))
report_style.add(ParagraphStyle(name='content_title',
                          fontFamily='Helvetica',
                          fontSize=12,
                          leading=15,
                          textColor=colors.HexColor("#2E2D30")))
report_style.add(ParagraphStyle(name='content_citation',
                          fontFamily='Helvetica',
                          fontSize=10,
                          textColor=colors.HexColor("#D65720")))
report_style.add(ParagraphStyle(name='content_doi',
                          fontFamily='Times-Roman',
                          fontSize=11,
                          leading=15,
                          textColor=colors.HexColor("#285DC9")))
report_style.add(ParagraphStyle(name='content_line',
                          fontFamily='Times-Roman',
                          fontSize=11,
                          leading=15,
                          textColor=colors.HexColor("#050000")))
report_style.add(ParagraphStyle(name='content_summary',
                          fontFamily='Times-Roman',
                          fontSize=11,
                          leading=15,
                          textColor=colors.HexColor("#1A6304")))
report_style.add(ParagraphStyle(name='content_keyword',
                          fontFamily='Times-Roman',
                          fontSize=11,
                          leading=15,
                          textColor=colors.HexColor("#A10613")))
# title
report_title = Paragraph("pmExt Reports <ver 0.22>", report_style['Heading1'])

# main run
pbar = enumerate(tqdm(title_list))
contents = []
contents.append(report_title)

# run loop
for item_ind, item in pbar:
    # article number
    paragraph_1 = Paragraph(
        ("[ Article" + "-" + '%04d' %(item_ind + 1) + " ]"),
        report_style['Heading2']
    )
    # title
    paragraph_2= Paragraph(
        item,
        report_style['content_title']
    )
    # citation number
    paragraph_3 = Paragraph(
        ("Citation:  " + "%s\n" % citation_list[item_ind]),
        report_style['content_citation']
    )
    # doi link
    paragraph_4 = Paragraph(
        ("DOI:  " + "%s\n" % doi_list[item_ind]),
        report_style['content_doi']
    )
    # abstract
    paragraph_5 = Paragraph(
        abstract_list[item_ind],
        report_style['BodyText']
    )
    contents.append(paragraph_1)
    contents.append(paragraph_2)
    contents.append(paragraph_3)
    contents.append(paragraph_4)
    contents.append(paragraph_5)
report.build(contents)
print(" ")

print(" [ Now downloading abstract summary !! ] ")
# with open(os.path.join('./' + root_dir + '/', keyword + '_abstract_summary' + '.txt'), 'w', encoding="utf-8") as f:
#     pbar = enumerate(tqdm(title_list))
#     for item_ind, item in pbar:
#         f.write("%s\n" % "      ")
#         f.write("[ Article" + "-" + '%04d' %(item_ind + 1) + " ]: " + "%s\n" % item)
#         f.write("Citation" + ": " + "%s\n" % textwrap.fill(citation_list[item_ind], width=150))
#         f.write("doi" + ": " + "%s\n" % textwrap.fill(doi_list[item_ind], width=150))
#         f.write("%s\n" % "      ")
#         f.write("%s\n" % textwrap.fill(abstract_summary_list[item_ind], width=150))
#         f.write("%s\n" % "      ")
#         f.write('# Keywords  ' + "%s\n" % textwrap.fill(abstract_keyword_list[item_ind]))
#         f.write("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
#         f.write("%s\n" % "      ")
#         time.sleep(0.01)
#
# set the template for pdf output
summary = SimpleDocTemplate(os.path.join('./' + root_dir + '/' + "pmExt_AbstractSummary-" + keyword + '.pdf'), pagesize=A4)
# title
summary_title = Paragraph("pmExt Reports (Abstract Summary)", report_style['Heading1'])

# main run
pbar = enumerate(tqdm(title_list))
contents_sum = []
contents_sum.append(summary_title)

# run loop
for item_ind, item in pbar:
    # article number
    paragraph_1 = Paragraph(
        ("[ Article" + "-" + '%04d' %(item_ind + 1) + " ]"),
        report_style['Heading2']
    )
    # title
    paragraph_2= Paragraph(
        item,
        report_style['content_title']
    )
    # citation number
    paragraph_3 = Paragraph(
        ("Citation:  " + "%s\n" % citation_list[item_ind]),
        report_style['content_citation']
    )
    # doi link
    paragraph_4 = Paragraph(
        ("DOI:  " + "%s\n" % doi_list[item_ind]),
        report_style['content_doi']
    )
    # abstract summary
    paragraph_5 = Paragraph(
        "+++++++++++++++++++++++++++ Auto-Summary ++++++++++++++++++++++++++++",
        report_style['content_line']
    )
    # abstract summary
    paragraph_6 = Paragraph(
        abstract_summary_list[item_ind],
        report_style['content_summary']
    )
    # abstract summary
    paragraph_7 = Paragraph(
        "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++",
        report_style['content_line']
    )
    # abstract keywords
    paragraph_8 = Paragraph(
        abstract_keyword_list[item_ind],
        report_style['content_keyword']
    )
    contents_sum.append(paragraph_1)
    contents_sum.append(paragraph_2)
    contents_sum.append(paragraph_3)
    contents_sum.append(paragraph_4)
    contents_sum.append(paragraph_5)
    contents_sum.append(paragraph_6)
    contents_sum.append(paragraph_7)
    contents_sum.append(paragraph_8)
summary.build(contents_sum)


# save figures
print(" ")
print(" [ Now downloading article figures !! ] ")
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
