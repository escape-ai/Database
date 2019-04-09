# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 22:26:44 2019

@author: gaoyu
"""


from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import re
from openpyxl import Workbook
import pandas as pd
import time
from selenium import webdriver
sum_url="https://smmry.com/"
web='https://www.straitstimes.com/indonesia-elections-2019'


def get_article_sum(page):
    word=""
    for link in page.find_all('div',{'id':'sm_container_output'}):  
        word+=link.text
    return word
       
def summary(url):
    
    browser=webdriver.Chrome("C:\selenium\chromedriver.exe")
    browser.get(sum_url)
    
    
    url_element=browser.find_element_by_id('sm_force_url')
    url_element.send_keys(url)
    
    sub_element=browser.find_element_by_id('sm_submit')
    sub_element.submit()
    time.sleep(10)        
    page=soup(browser.page_source,'html.parser')
    article_summary=get_article_sum(page)
    return article_summary


def get_urls(web):
    links=[]
    titles=[]
    uClient=uReq(web)
    '''download the web'''
    page_html=uClient.read()
    uClient.close()
    '''page parse'''
    page_soup=soup(page_html,'html.parser')
    main=page_soup.find_all('span',{"class":"story-headline"})    #
   
    for link in main:
        a=link.find('a')
        titles.append(a.text)
        
        url="www.straitstimes.com"+a.get('href')
        #if 'the-latest-fact-checks-from-the-international-fact-checking-network-ifcn-'in url:
        links.append(url)
    #print(links)
    return links,titles

def domain(url):
    domain=""
    count=0
    for i in url:
        if count==3:
            break
        else:
            if i=="/":
                count+=1
            else:
                if count==2:
                    domain+=i
    return domain
def trans(file):
    df=pd.read_excel(file)
    df=df.transpose()
    df.to_excel("truedata2.xlsx")
def savetoEXCEL(ls1,ls2,ls3):
     
    wb=Workbook()
    ws=wb.active
    ws.append(ls1)
    ws.append(ls2)
    ws.append(ls3)
   
    wb.save('todeletedata.xlsx')
    trans('todeletedata.xlsx')


    

a=get_urls(web)
urls=a[0]
titles=a[1]
summarys=[]
for url in urls:
    summarys.append(summary(url))
    
savetoEXCEL(titles,urls,summarys)    



#file="data.xlsx"
#trans(file)