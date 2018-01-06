"""
Readme
==========
This program aims to take html files as input and returns text files.
It passes each article html file from source folder to another python program i.e.html2txt.py
and scrap html file to text file with same name.

This program also writes a json file for each directory having all the articles of a directory in it in json format.

Steps involved
==============

 1. Read each html file from source folder.

 2. Pass the html file to another python program i.e. html2txt.py.

 3. html2txt.py returns text such as title, publish and updated time of article and article body.

 4. The returned text is written to text file with name same as html file.

 5. The output files are stored in destination folder in the same hierarchy they are retrived.

 6. The output json file also stored in destination folder.

COMMAND LINE EXECUTION EXAMPLE:
===============================
C:\Users>python <Source_path> <Output_path>

C:\Users\Sunil>python text2files.py D:\data D:\output1\

"""
import sys
import os


# source file path
path = sys.argv[1]
# output file path
output_path = sys.argv[2]
# Read each folder inside file path
for filename in os.listdir(path):
    folder_path = path + "\\" + filename
    files_count = str(len(os.listdir(folder_path)))
    id_value = 0

    # Read files from each file folder
    for htmlfiles in os.listdir(folder_path):
        id_value = str(int(id_value) + 1)
        file_path = folder_path + "\\" + htmlfiles
        output_filePath = output_path + "\\" +str(filename)
        # create folder for each output text files in output_path
        if not os.path.exists(output_filePath):
            os.makedirs(output_filePath)
        txt_filename = htmlfiles[:-5]
        txt_filePath = output_filePath +"\\" +txt_filename +'.log'
        json_filePath = output_filePath +"\\" +str(filename) +'.json'

        # txt format
        get_txt = "python html2txt.py " + file_path
        # One json file for each directory
        get_json = "python html2txt.py " + file_path+" -f=j --c="+id_value

        #Pass the arguments to connect html2txt.py program through cmd and save txt files in output_path
        os.system(get_txt+" > " +txt_filePath)

        # Json formatting
        os.system(get_json+" >> " + json_filePath)
        with open(json_filePath, "a") as json_file:
            if id_value == files_count:
                json_file.write("]}")
            else:
                json_file.write(",")


print "Downloading html to text files is completed"