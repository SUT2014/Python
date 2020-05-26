#! /usr/bin/python
# Description: PAM sending tool
# pam.py <start sub id>,<end sub id>,(<attribute names...>),(<attribute values...>)
# Kumaran D

import sys
import os
import pipes
import pprint
from time import strftime
import datetime
import shutil

g_profile_sql_string = "profilemanager/psswrd1234@aspcmdbt03:1525/ASPCM3T"

def write_footer(f):
    f.write("\nFILEEND")

def write_header(f,start,end):
    f.write("startSubId="+start+", endSubId="+end+"\n")

def print_usage():
    print 'pam.py - script to send PAM messages\n'
    print 'usage: pam.py <start sub id> <end sub id> <attribute names> <attribute values> \n'
    print 'examples:'
    print 'pam.py 2759000 2759000 TSA42 Max  ::: will set TSA42 to Max for subscriber id 2759000\n'
    print 'pam.py 2759000 2759005 TSA42 Max  ::: will set TSA42 to Max for subscribers 27590000 to ..05\n'
    print 'pam.py 2759000 2759005 TSA42,TSA43 Max,Min  ::: will set TSA42 to Max, TSA43 to Min for subscribers 27590000 to ..05\n'
    print 'pam.py 2759000 2759000  ::: to send blank PAM message\n'

def main():
    if (len(sys.argv) < 3 or len(sys.argv) == 4):
       print_usage()
       return
    #create a file based on current time, 4 ms resolution
    t = datetime.datetime.now();
    s = t.strftime('%Y%m%d%H%M%S%S%w')
    f = open(s+".sub","w")
    write_header(f,sys.argv[1],sys.argv[2])
    if (len(sys.argv) == 3):
       attrib_list=" "
       attrib_value=" " 
    else:
       attrib_list = ","+sys.argv[3]
       attrib_value = ","+sys.argv[4]
    f.write("SubId"+attrib_list+"\n")
    for i in range (int(sys.argv[1]),int(sys.argv[2])+1):
        f.write(str(i)+attrib_value+"\n")
        
    write_footer(f)
    #move the file to PMGR hot directory
    dest = '/apps/pmgr/release/data/'+f.name
    shutil.move(f.name,dest)
    f.close()

if __name__ == "__main__":
    main()
