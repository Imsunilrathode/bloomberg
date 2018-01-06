"""
Readme
==========
Get [error] URL's from geturl.py log-files for maxiter iterations.
======================

This programe aims to fetch error urls from each logfiles and then
retry for maxiter number of iterations and if still it doesnt able to
download then it writes error status to output_logpath file.
And for success urls, it downloads to output_path.

This program has total 8 attributes to pass through cmdline.

login_path,dataoutpath,logout_path,batch_size,pause_time,from-year-month,to-year-month,maxiterations

from-year-month,to-year-month and maxiterations are options attributes.

Test-scenarios of this program:
===========================
--> If from-year-month and to-year-month are not passed then all login files will be processed.
    And if maxiterations is not mentioned then its default value is 1.

--> And if maxiteration value passed is 6 and all urls got success
    status at 3rd iteration then program breaks at 3rd iteration.

--> And if maxiteration value passed is 9 and on 9th iteration still few
    urls could not be processed, then program ends after 9th iteration
    and url status will be updated as "[error]".

COMMAND LINE EXECUTION EXAMPLE:
===============================
C:\Users>python fixerror.py <input_logpath> <output_datapath> <output_logpath> <batch_size> <pause_time> --from=<from-year-month> --to=<to-year-month> --max=<maxiter>
                                                                            (or)
C:\Users>python fixerror.py <input_logpath> <output_datapath> <output_logpath> <batch_size> <pause_time>

eg:
C:\Users\Sunil>python fixerror.py D:\login D:\dataout D:\logout 4 3 --from=2014-6 --to=2014-8 --max=2

output:
=========
Currently iteration is 1
Now processing logfile 2014-6.log
Now processing logfile 2014-7.log
Now processing logfile 2014-8.log
Downloading completed for all logfiles
No more error or retry left in logfiles
"""

import sys
import urllib
import os
from time import sleep
from datetime import datetime
import getopt

# Read all arguments from commandline.

error_logpath = sys.argv[1]
output_path = sys.argv[2]
output_errorlog = sys.argv[3]
batch = int(sys.argv[4])
pause_time = int(sys.argv[5])  # Sleep time in between each batch downloading

# from_date, to_date and maxiter are optional arguments
opts, args = getopt.getopt(sys.argv[6:], 'c:a:m:', ['from=', 'to=','max='])
from_date = ""
to_date = ""
maxiter =""

for opt, arg in opts:
    if opt in ('-c', '--from'):
        from_date = arg
    if opt in ('-a', '--to'):
        to_date = arg
    if opt in ('-m', '--max'):
        maxiter = arg


# If from_date and to_date not passed, all files will be processed
if from_date is not "":
    fd = datetime.strptime(from_date,'%Y-%m') # fd is from_date in datetime format
    td = datetime.strptime(to_date,'%Y-%m') # td is to_date in datetime format

# If maxiter is not passed, by default program runs for 1 iteration.
if maxiter is "":
    maxiter = 1
count = 0

# Open each logfile from main directory
for iter in range(0,int(maxiter)):

    print >> sys.stderr,"Current iteration is "+str(iter+1)

    error_count = 0
    if iter==0:
        openfile = error_logpath
    else:
        openfile = output_errorlog

    for filename in os.listdir(openfile):

        year = filename[:4]
        month = filename[5:-4]

        d = datetime.strptime(year+"-"+month,'%Y-%m')
        if from_date is "":
            fd = d
            td = d
        if(d >= fd and d <= td):
            error_file = openfile + "\\" + filename

            with open(error_file) as f:
                content = f.readlines()

            for i in range(0,len(content)):
                retry = "[retry"+str(iter)+"]"
                if iter==0:
                    lookfor ="[error] "
                else:
                    lookfor = retry
                if content[i][:8] == lookfor:

                    folder  = str(content[i].rsplit('/',2)[1])[:-3]
                    output_filePath = output_path +"\\"+ folder

                    # create folder for each output files in output_path
                    if not os.path.exists(output_filePath):
                        os.makedirs(output_filePath)
                    txt_filename = str(content[i][9:-1].rsplit('/', 1)[1])
                    txt_filePath = output_filePath +"\\" +txt_filename +'.html'
                    log_filepath = output_errorlog +"\\" +folder+'.txt'

                    if not os.path.exists(output_errorlog):
                        os.makedirs(output_errorlog)
                    sys.stdout = open(log_filepath, 'a')
                    if iter < int(maxiter)-1:
                        status = "[retry"+str(iter+1)+"]"
                    else:
                        status = "[error]"

                    # retrive each article_url and save directly to filepath.
                    try:
                        urllib.urlretrieve(content[i][9:-1], txt_filePath)
                        print >> sys.stdout, "[success]",str(content[i][9:-1])

                    # If url could not be fetched, then update its status to "[retry<iteration>]"
                    except:
                        print >>sys.stdout, status , content[i][9:-1]
                        error_count = error_count +1

                    count = count + 1
                    # Timeout for pause_time for every batch-size.
                    if count%batch == 0:
                        sleep(pause_time + pause_time*0.1)


            print >> sys.stdout, "-----------------------"

            print >> sys.stderr, "Processed logfile " + filename

            # Timeout at end of each file.
            sleep(pause_time + pause_time*0.1)

    # if no error files found while processing logfiles, break the loop and exit the program.
    if error_count==0:
        print >> sys.stderr,"Downloading completed for all logfiles"
        print >> sys.stderr,"No more error or retry left in logfiles."
        break

