"""
Readme
==========
Get URL's from webpage
======================

This programe aims to parse the data fetched from XML webpage and download all
URL's mentioned in webpage to local drive.XML page URL, Count of URL's to be
parsed and downloaded, destination path, batch size and time interval between
 batch downloading process are to be passed through arguments in command line.

Steps involved
==============


 1. Import required libraries.Install beautiful soup library if not present.

             pip install beautifulsoup4

 2. Read each argument passed through commandline into variables.

 3. Request XML page URL and fetch data to variable.

 4. Use beautiful soup library to parse the data within XML page.

 5. Store each tagged element into variables and group by tag ID.

 6. Now print the parsed elements from URL row wise , save and download.

 7. Repeat the above process till it reaches count mentioned in command line.

 8. Group the rows based on batch size and pause the process for random time
    interval so to eliminate the server hitting continously till EOF.

 9. Print "Downloading Completed" upon successfully exection of 6,7,8 steps.

COMMAND LINE EXECUTION EXAMPLE:
===============================
C:\Users>python <FILE_NAME> <URL> <DEST_PATH> <COUNT> <BATCH_SIZE> <PAUSE_TIME>

Expected output with sample size 10:
-------------------------------------
C:\Users\Sunil>python geturls.py http://www.bloomberg.com/feeds/bbiz/sitemap_2006_10.xml F://HTML/ 10 2 15

http://www.bloomberg.com/news/articles/2006-10-19/audis-adrenal-rs-4 || 2006-10-20 || yearly || 0.1
http://www.bloomberg.com/news/articles/2006-10-30/vaporstream-erases-your-e-mail-past || 2006-10-31 || yearly || 0.1

http://www.bloomberg.com/news/articles/2006-10-30/mazdas-unconventional-rx-8 || 2006-10-31 || yearly || 0.1
http://www.bloomberg.com/news/articles/2006-10-24/themoneyblogs-lacking-the-goods || 2006-10-25 || yearly || 0.1

http://www.bloomberg.com/news/articles/2006-10-21/more-car-for-less-money || 2006-10-22 || yearly || 0.1
http://www.bloomberg.com/news/articles/2006-10-19/symbols-clunky-clever-mc70 || 2006-10-20 || yearly || 0.1

http://www.bloomberg.com/news/articles/2006-10-01/the-future-on-four-wheels || 2006-10-02 || yearly || 0.1
http://www.bloomberg.com/news/articles/2006-10-01/the-ever-evolving-automobile || 2006-10-02 || yearly || 0.1

http://www.bloomberg.com/news/articles/2006-10-03/pentaxs-potent-k100d || 2006-10-04 || yearly || 0.1
http://www.bloomberg.com/news/articles/2006-10-03/big-tv-battle-lcd-vs-dot-plasma || 2006-10-04 || yearly || 0.1

Downloading Completed
-----------------------------------------
Saving Stdout print statements
C:\Users\Sunil>python geturls.py http://www.bloomberg.com/feeds/bbiz/sitemap_2006_10.xml F://HTML/ 10 2 15 >output.txt
C:\Users\Sunil>type output.txt
"""

import sys
import re
from time import sleep
import urllib
import urllib2
import random
from bs4 import BeautifulSoup

url = sys.argv[1]  # URL which needed to be parsed stored in variable url.
output_path = sys.argv[2]  # Destination path to store downloaded html pages.
count = int(sys.argv[3])  # Number of news articles to be downloaded.
batch = int(sys.argv[4])  # Batch size of urls to be downloaded in each interval
pause_time = int(sys.argv[5])  # Sleep time in between each batch downloading

# Request page url and read the data.
req_url = urllib2.Request(url)
open_url = urllib2.urlopen(req_url)
fchData = open_url.read()
soup = BeautifulSoup(fchData, "lxml")


# Find all <loc> tags to fetch article urls.
article_url = str(soup.find_all("loc"))
article_url = article_url[1:]
article_url = re.sub('<[A-Za-z\/][^>]*>', '', article_url).replace(',', '')
article_url = list(article_url.split(' '))

# Find all <lastmod> tags to fetch Date.
date = str(soup.find_all("lastmod"))
date = date[1:-1]
date = re.sub('<[A-Za-z\/][^>]*>', '', date).replace(',', '')
date = list(date.split(' '))
if len(date) < len(article_url):
    date = None
# Find all <changefreq> tags to fetch frequency parameter for each article.
frequency = str(soup.find_all("changefreq"))
frequency = frequency[1:-1]
frequency = re.sub('<[A-Za-z\/][^>]*>', '', frequency).replace(',', '')
frequency = list(frequency.split(' '))

# Find all <priority> tags to fetch priority tag value.
priority = str(soup.find_all("priority"))
priority = priority[1:-1]
priority = re.sub('<[A-Za-z\/][^>]*>', '', priority).replace(',', '')
priority = list(priority.split(' '))
for i in range(min(len(article_url),count)):
    # Print the parsed url,date,freq and priority variables for each article
    if date is None:
        print >> sys.stdout, str(article_url[i])
    else:
        print >> sys.stdout, str(article_url[i]) + " || " + str(date[i][:10])+" || " + str(frequency[i]) + " || "+str(priority[i])

    # Filepath to define its arctile file name and destination path.
    filePath = output_path + str(article_url[i].rsplit('/', 1)[1]) + '.html'
    # retrive each article_url and save directly to filepath.
    urllib.urlretrieve(article_url[i], filePath)

    # Group URL's in batch size and pause for pause_time +- 10 secs.
    if (i+1) % batch == 0:
        pause_time = pause_time + random.randint(-1, 1)
        sleep(pause_time)

print >> sys.stdout, "Downloading Completed"
