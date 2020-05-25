######################################
#   By Kumaran D
#   Normalised SGW NFT results extractor
#   Refer to the confluence page to understand what the script intends to do
######################################

import time
import re
from collections import defaultdict
import datetime

CODE_ID_INDEX = 6
TIME_INDEX = 1
analytics = defaultdict(list)

def add_log_to_analytics(line):
    split_line = (line.split(' '))
    #print(split_line[CODE_ID_INDEX])
    key = (re.findall("\[([^[\]]*)\]", split_line[CODE_ID_INDEX]))[0]
    analytics[key].append(datetime.datetime.strptime(split_line[0]+' '+split_line[1], '%Y/%m/%d %H:%M:%S.%f'))


######main######
def main():
    f = open('C:\Work\G7\SGW NFT\\1kin1seconds_new.txt', "r")
    for line in f:
        add_log_to_analytics(line)
    for matter in analytics:
        if len(analytics[matter]) > 1:
            print(float(float((analytics[matter][1] - analytics[matter][0]).microseconds))/1000)
            #print(matter, float(float((analytics[matter][1] - analytics[matter][0]).microseconds))/1000)

if __name__ == '__main__':
    main()