"""
Readme
==========
Get sitemap URL for each month of the year from bloomberg main sitemap.
This program fetch each month sitemap url and pass required arguments
to another python program to download news articles
======================

This programe aims to parse the data fetched from XML webpage and connect with another python
program  to download  each sitemap article urls all URL's mentioned in webpage to local drive.
XML page URL, Count of URL's to be parsed and downloaded, destination path,log file path
batch size and time interval between batch downloading process and from and to year, month
are to be passed through arguments in command line.

Steps involved
==============


 1. Import required libraries.Install beautiful soup library if not present.

             pip install beautifulsoup4

 2. Read each argument passed through commandline into variables.

 3. Request XML page URL and fetch data to variable.

 4. Use beautiful soup library to parse the data within XML page.

 5. Store each tagged element into variables and group by tag ID.

 6. Now print the parsed elements from URL row wise.

 7. Pass each url to another program i.e geturl.py through command prompt.

 8. Repeat the above process till it reaches to_date mentioned in command line.

 9. Group the rows based on batch size and pause the process for random time
    interval so to eliminate the server hitting continously till EOF.

 10. Print "Downloading Completed" upon successfully exection.

COMMAND LINE EXECUTION EXAMPLE:
===============================
C:\Users>python <FILE_NAME> <URL> <COUNT> <BATCH_SIZE> <PAUSE_TIME> <From_date> <To_date>

Expected output with sample size 10:
-------------------------------------
C:\Users\Sunil>python sitemap.py http://www.bloomberg.com/feeds/bbiz/sitemap_index.xml D://data/ D://logdata/ 30 7 10 2014-04 2014-07.

Please wait, downloading will start soon
http://www.bloomberg.com/feeds/bbiz/sitemap_2014_7.xml || 2016-09-19 || 7:34:02-04:00
http://www.bloomberg.com/feeds/bbiz/sitemap_2014_6.xml || 2016-09-19 || 7:34:02-04:00
http://www.bloomberg.com/feeds/bbiz/sitemap_2014_5.xml || 2016-09-19 || 7:34:02-04:00
http://www.bloomberg.com/feeds/bbiz/sitemap_2014_4.xml || 2016-09-19 || 7:34:02-04:00
Downloading Completed
-----------------------------------------
Saving Stdout print statements in D://logdata/folder_names

"""

import os
import sys
import re
import urllib2
from bs4 import BeautifulSoup
from datetime import datetime
from dateutil.parser import parse
import random
from time import sleep

url = sys.argv[1]  # URL which needed to be parsed stored in variable url.
output_path = sys.argv[2]  # Destination path to store downloaded html pages.
log_path = sys.argv[3]      # Log file path to store print statements
count = int(sys.argv[4])  # Number of news articles to be downloaded.
batch = int(sys.argv[5])  # Batch size of urls to be downloaded in each interval
pause_time = int(sys.argv[6])  # Sleep time in between each batch downloading
from_date = sys.argv[7]    # Year and month from where sitemap to be downloaded
to_date = sys.argv[8]      # Year  and month till where sitemap to be downloaded


# Read from_date and to_date as string and convert into datetime format
fd = datetime.strptime(from_date,'%Y-%m') # fd is from_date in datetime format
td = datetime.strptime(to_date,'%Y-%m') # td is to_date in datetime format

# conditions for input arguments

if count < 0:
    print "Count of downloading articles should be greater then 0"
    exit()
if batch > count:
    print "Batch size exceeds article count"
    exit()
if fd < td:
    print "Please wait, downloading will start soon"
else:
    print "Wrong format... from_date should be lower than to_date"
    exit()


# Request page url and read the data.
req_url = urllib2.Request(url)
open_url = urllib2.urlopen(req_url)
fchData = open_url.read()
soup = BeautifulSoup(fchData, "lxml")

# Find all <loc> tags to fetch sitemap urls.
sitemap_url = str(soup.find_all("loc"))
sitemap_url = sitemap_url[1:-1]
sitemap_url = re.sub('<[A-Za-z\/][^>]*>', '', sitemap_url).replace(',', '')
sitemap_url = list(sitemap_url.split(' '))

# Find all <lastmod> tags to fetch sitemap Date.
sitemap_date = str(soup.find_all("lastmod"))
sitemap_date = sitemap_date[1:]
sitemap_date = re.sub('<[A-Za-z\/][^>]*>', '', sitemap_date).replace(',', '')
sitemap_date = list(sitemap_date.split(' '))

for x in range(0,len(sitemap_url)):

    # filter out video URLs for now
    p = re.compile('.*sitemap_video.*')
    if ( p.match(sitemap_url[x]) ):
        continue
    
    # split the year and month strings from sitemap_url seperatly into y = year and m = month variables
    y = sitemap_url[x].rsplit('_', 2)[1]
    m = sitemap_url[x].rsplit('_', 1)[1][:-4]
    # define folder name for each year-month of sitemap

    folder_name = y+"-"+m
    try:
        d = datetime.strptime(y+"-"+m,'%Y-%m')

        if(d >= fd and d <= td):
            print >> sys.stderr, str(sitemap_url[x]) + " || " + str(sitemap_date[x][:10]) + " || " + str(sitemap_date[x][12:])
            
            # Filepath to define its article file name and destination path.
            filePath = output_path + str(folder_name)
            # create folder for each sitemap in filePath
            if not os.path.exists(filePath):
                os.makedirs(filePath)
            # create log folder for each sitemap in log_path
            log_filePath = log_path + str(folder_name) + '.log'
            #if not os.path.exists(log_filePath):
            #    os.makedirs(log_filePath)

            geturl = "python2 geturl.py " + sitemap_url[x] + " " + filePath+"/"" " + str(count) + " " + str(batch) + " " + str(pause_time)
            # Pass the arguments to connect geturl.py program through cmd and save log files in output.txt
            os.system(geturl +" > " +log_filePath + ' -u')

            p_time = 20 + random.randint(-5, 5)
            print >> sys.stderr, "sleeping for", p_time, "seconds"
            sleep(p_time)

    except:
        continue


    
print >> sys.stderr, "Downloading Completed"
