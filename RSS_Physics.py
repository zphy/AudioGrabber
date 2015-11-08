# -*- coding: utf-8 -*-
"""
Created on Sat Aug 30 21:05:33 2014

@author: hyzhou
Github: zphy

This file reads RSS information from APS's online journal Physics and converts the text to .mp3 audio to listen during one's free time. As I've been pretty busy lately I haven't had the time to implement this for non-Mac platforms, and the results might be affected by APS website changes, but I might update this code soon.

A directory should be created on the upper level to store these audio files, with the corresponding folder names.

This file requires the installation of the following packages:
    BeautifulSoup4
    feedparser
"""

#import urllib
from bs4 import BeautifulSoup # to process html files
import urllib2 # imports html
import os  # to use say and other command line or system operations
import re
import os.path
import feedparser
#import time

journal_url = "http://feeds.aps.org/rss/recent/physics.xml"
journal="physics"
lastcheck=20150628              # update each time this code is run
#"http://feeds.nature.com/nphys/rss/current"
#http://feeds.nature.com/nphoton/rss/current
#http://feeds.nature.com/nnano/rss/current
#http://feeds.nature.com/nmat/rss/current


# class for feed items
class FItem:
    
    def __init__(self,item,journal):
        self.link=item["link"]
        self.title=str(item["title"].encode('utf8'))
        print(self.title.split())
        temp=self.title
        temp=temp.replace("'","")
        temp=temp.replace(":","")
        temp=temp.replace("(","")
        temp=temp.replace(")","")
        temp=temp.replace("-","")
        temp=temp.replace("/","")
        self.title=temp
        self.title=''.join(self.title.split())
        self.title.replace("'","")
        print(self.title)
        self.journal=journal
        self.dir='../'+self.journal
        
       
        
    def ExtrTxt(self):
        os.chdir(self.dir)  # go to a separate directory for each journal
        page=urllib2.urlopen(self.link) # extract text
        html=page.read()
        soup=BeautifulSoup(html)
        texts=soup.findAll(text=True)
        def visible(element):       # only retain visible elements
            if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
                return False
            #elif re.match('<!--.*-->', str(element)):  # has been giving me a ascii non-matching warning lately, temporarily commenting out
            #    return False
            return True 
        visible_texts = filter(visible, texts)
        i=0     # keeping track of line number
        flagend=0
        for line in visible_texts:
            visible_texts[i]=line.encode('utf8')
            visible_texts[i]=visible_texts[i].replace('\n', '')
            visible_texts[i]=visible_texts[i].replace('\t', '')
            visible_texts[i]=visible_texts[i].replace('\r', '')
            visible_texts[i]=visible_texts[i].replace('\xe2\x80\x94',' dash ')    #EM-Dash
            visible_texts[i]=visible_texts[i].replace('\xe2\x80\xa2','')
            visible_texts[i]=visible_texts[i].replace('\xe2\x80\x9c','"')
            visible_texts[i]=visible_texts[i].replace('\xe2\x80\x9d','"')
            visible_texts[i]=visible_texts[i].replace('.',',')      # this is mainly because somehow mac doesn't
            # know to stop at periods.
            #if visible_texts[i]=='APS Journals':
            #    print('1')
            #    flagstart=i
            if visible_texts[i]==' APS News':
                print('1')
                flagstart=i
            if visible_texts[i]=='Show more':
                print('1')
                flagstart=i+1
            if visible_texts[i]=='Previous Synopsis':
                print('2')
                flagend=i
                break
            if visible_texts[i]=='Previous synopsis':
                print('2')
                flagend=i
                break
            if visible_texts[i]=='Previous Viewpoint':
                print('2')
                flagend=i
                break
            if visible_texts[i]=='Previous Focus':
                print('2')
                flagend=i
                break
            if visible_texts[i]=='Previous Editorial':
                print('2')
                flagend=i
                break
            if visible_texts[i]=='References':
                print('2')
                flagend=i
                break
            if visible_texts[i]=='Subject Areas':
                print('2')
                flagend=i
                break
            if visible_texts[i]=='Recent Articles':
                print('2')
                flagend=i
                break
            if visible_texts[i]=='Announcements':
                print('2')
                flagend=i
                break
            visible_texts[i]=visible_texts[i].replace('Article metrics','')
            i=i+1
        if flagend==0:
            print('No reference found!')
            f=open(self.title+'.txt','w')
            f.close()
            return 0
        visible_texts = visible_texts[flagstart:flagend]    # only interested in main text of article
        visible_texts = ''.join(visible_texts)
        s=str(visible_texts)
        journaltxt=self.journal+'.txt'
        f=open(journaltxt,'w+')
        f.write(s)
        f.close()
        aiffmake='say -v Samantha -r 150 -o '+self.title+'.aiff -f'+self.journal+'.txt'
        mp3make='lame -h '+self.title+'.aiff '+self.title+'.mp3'
        os.system(aiffmake)
        os.system(mp3make)
        os.remove(self.title+'.aiff')
        f=self.title+'.mp3'
        fullpath = os.path.join(self.dir, f)
        if os.path.getsize(fullpath) < 52 * 1024:
            os.remove(fullpath)
            print('.mp3 too small, removed!')
        print('.mp3 generate success!')
        
def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return 1
        else:
            return 0
        
feed = feedparser.parse(journal_url)
items = feed["items"]
for item in items:
    print([item["title"]])
    date=item["date"].encode('ascii')
    date=int(date[0:4]+date[5:7]+date[8:10])
    if date<lastcheck:
        continue
    #month=int(date[5:7])
    #day=int(date[8:10])
    fitem=FItem(item,journal)
    if find(fitem.title+'.mp3','../'+journal)==0:
        fitem.ExtrTxt()
for root, _, files in os.walk('../'+journal):
    for f in files:
        fullpath = os.path.join(root, f)
        if os.path.getsize(fullpath) < 20 * 1024:
            os.remove(fullpath)
