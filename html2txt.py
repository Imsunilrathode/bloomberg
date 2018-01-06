"""
Readme
==========
Get title, publish and update timestamp, and body content from article html path.

It also provide output in json format is file format i.e. -f=j is passed as argument in cmd.

Steps involved
==============


 1. Import required libraries.Install beautiful soup library if not present.

             pip install beautifulsoup4
 2. Because of console character encoding issue,update it to UTF-8.
            chcp 65001

COMMAND LINE EXECUTION EXAMPLE:
===============================
C:\Users>python <FILE_NAME> <html_path>
                or
C:\Users>python <FILE_NAME> <html_path> --n=<count of words> -f=j<json format>


C:\Users\Sunil>python html2txt.py D:\data\1991-7\theres-still-life-in-this-rust-belt-relic.html >output.txt
                                            or
C:\Users\Sunil>python html2txt.py D:\data\1991-7\theres-still-life-in-this-rust-belt-relic.html --n=100 -f=j
 output will be json format
C:\Users\Sunil>type output.txt
"""

from bs4 import BeautifulSoup
import codecs
import math
import sys
import getopt
import time
import itertools
from calendar import timegm

opts, args = getopt.getopt(sys.argv[2:], 'n:f:c:', ['n=','f=','c='])
n = "" # count of words to be printed
f = "" # json file format if -f=j
c = "" # id value for json file

for opt, arg in opts:
    if opt in ('-n', '--n'):
        n = arg
    if opt in ('-f', '--f'):
        f = arg
    if opt in ('-c', '--c'):
        c = arg

# Read local html file path
path = sys.argv[1]

# id value will be 1 if program is run on single html file.
if c is "":
    id = 1
else:
    id = c
path1 = r'%s' % path
page=codecs.open(path1, 'r')

soup = BeautifulSoup(page,"lxml")

# Fetch title of article
title = soup.find('title').text
date_list = []

# Json format in begining of file


# Fetch publish date and update date of article
for i in soup.findAll('time'):
    if i.has_attr('datetime'):
        date_list.append(i['datetime'])
if f is "":
    print "Title of the article : " + title.encode("utf-8")+"\n"
else:
    if int(id) is 1:
    # Json format
        print '{"doc":[' + "\n" \

    print '{"id":'+ str(id) +',\n' \
           '"title":"' + title.encode("utf-8") + '",'+ "\n"



if len(date_list) == 1:
    utc_time = time.strptime(date_list[0], "%Y-%m-%dT%H:%M:%S.%fZ")
    pub_epoch_time = timegm(utc_time)
    if f is "":
        print "Publish Timestamp: " + str(date_list[0]) + "\n"
        print "Publish epoch seconds: " + str(pub_epoch_time) + "\n"
    else:
        # Json format
        print '"publish-timestamp": "'+ str(date_list[0]) +'",'+ "\n"
        print '"publish-epoch-seconds":'+ str(pub_epoch_time) +","+ "\n"

if len(date_list) == 2:
    utc_time1 = time.strptime(date_list[0], "%Y-%m-%dT%H:%M:%S.%fZ")
    pub_epoch_time = timegm(utc_time1)
    utc_time2 = time.strptime(date_list[1], "%Y-%m-%dT%H:%M:%S.%fZ")
    update_epoch_time = timegm(utc_time2)
    if f is "":
        print "Publish Timestamp: " + str(date_list[0])+"     Update Timestamp: " + str(date_list[1]) +"\n"
        print "Publish epoch seconds: " + str(pub_epoch_time) + "             Update epoch seconds :" + str(update_epoch_time) + "\n"
    else:
        # Json format
        print '"publish-timestamp": "'+ str(date_list[0]) +'",'+ "\n"
        print '"publish-epoch-seconds":'+ str(pub_epoch_time) +","+ "\n"
        print '"update-timestamp": "'+ str(date_list[1]) +'",'+ "\n"
        print '"update-epoch-seconds":'+ str(update_epoch_time) +","+ "\n"


#Fetch article body content
body1 = []
bodylist = []
body = soup.find('div' , {'class' : 'article-body__content'}) or soup.find('div' , {'class' : 'body-copy'})
if body == soup.find('div' , {'class' : 'body-copy'}):
    body.find('aside', class_="inline-newsletter").decompose()
try:
    body1 = body.find_all({'p','h2','h3','pre'})

except:
    print "Content not found"
    exit()

for i in range(0,len(body1)):
    if body1[i].has_attr('h2' or 'h3'):
        print "\n"
        bodylist.append(body1[i].find('h2' or 'h3').text.encode("utf-8"))

    else:
        t = body1[i].text.encode("utf-8")
        t = ' '.join(t.split())
        bodylist.append(t)

# Format body content in paragraphs.
subbodylist = []

for x in range(0,len(bodylist)):
    subbodylist.append(list(bodylist[x].split(' ')))

# If n(count of words) value is not mentioned. Then display full article
# Each line restricted to 15 words
if f is "":
    print  "Article body:\n"

# Full article body in text format
if n is "" and f is "":
    for y in range(0,len(bodylist)):
        if len(subbodylist[y]) > 15:
            n=int(math.ceil(float(len(subbodylist[y]))/15))
            line = []
            for z in range(0,n):
                line = subbodylist[y][15*z:15*(z+1)]
                print ' '.join(line)
            print "\n"
        else:
            print ' '.join(subbodylist[y])

# Full article body in json format
elif f is not "" and n is "":
    para = list(itertools.chain.from_iterable(subbodylist))
    print '"article-body":"'+' '.join(para).replace('"', '\\"').replace('\n', '\\n')+'"'
    print '}'

    if c is "":
        print ']}'

# Article body limited to first n words in json format
elif f is not "" and n is not "":
    para = list(itertools.chain.from_iterable(subbodylist))[:int(n)]
    print '"article-body":"'+' '.join(para)+'"'
    print '}]}'

# Article body limited to first n words in txt format
elif f is "" and n is not "":
    para = list(itertools.chain.from_iterable(subbodylist))[:int(n)]

    if len(para) > 15:
        n=int(math.ceil(float(len(para))/15))
        line = []
        for k in range(0,n):
            line = para[15*k:15*(k+1)]
            print ' '.join(line)
        print "\n"
    else:
        print ' '.join(para)
