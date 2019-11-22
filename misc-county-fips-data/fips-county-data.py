# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 09:27:21 2019

@author: Omar
"""

from bs4 import BeautifulSoup
import requests

link = 'https://en.wikipedia.org/wiki/User:Michael_J/County_table'

page = requests.get(link)
soup = BeautifulSoup(page.text,'html.parser')


tab = soup.find('table',{'class':'wikitable sortable'})
#manually do header for first row then grab data
header = ['i','state','fips','county','county seats','popultion',
          'land area (sq km)','land area(sq mi)','water area (sq km)',
          'water area (sq mi)','total area (sq km)','total area (sq mi)','latitude','longitude']

tableData = []
for item in tab.find_all_next('tr')[1:]:
    toAdd = []
    for tag in item.find_all('td'):
        txt = tag.text
        #handling footnootes
        if '[' in txt:
            ind1 = txt.index('[')
            ind2 = txt.index(']')
            txt = txt[:ind1]+txt[ind2+1:]
        toAdd.append(txt)
    #take care of char at end of lat and lon
    toAdd[-2] = toAdd[-2][:-1]
    toAdd[-1] = toAdd[-1][:-2]
    #removing possible footnotes in county name
    if '[' in toAdd[3]:
        entry = toAdd[3]
        ind1 =entry.index('[')
        ind2 = entry.index(']')
        toAdd[3] = entry[:ind1]+entry[ind2+1:]
    tableData.append(toAdd)
    
#write to file 
with open('county-data.txt','w',encoding = 'utf8') as fptr:
    fptr.write('\t'.join(header)+'\n')
    for datum in tableData:
        fptr.write('\t'.join(datum)+'\n')