######################################
#   By Kumaran D
#   Confirm URID numbers for each SSR NFT file
#   Refer to the confluence page to understand what the script intends to do
######################################
import time
import os
import re
import datetime

LOG = True
URID_FILE = 'urid.txt'
ANALYTICS_DIR = 'C:\\Work\\G7\\SSR NFT\\ingest_nft\\ingest\\Stage\\R11\\'
FILE_COUNTER = []
def print_line(*argv):
    if LOG is True:
        for matter in argv:
            print(matter)


######main######
def main():
    urid_list = []
    urid_counter = {}
    f = open(ANALYTICS_DIR + URID_FILE, "r")
    for line in f:
        urid_list.append(line.strip('\n\r'))
    f.close()
    for filename in os.listdir(ANALYTICS_DIR):
        if bool(re.search('Xmlfile', filename)) is False:
            continue
        f = open(ANALYTICS_DIR + filename, "r")
        filetext = f.read()
        for urid in urid_list:
            #print_line("Urid ID: " + urid)
            if re.search(urid, filetext):
                #print(urid.strip('\n\r'), filename)
                if urid in urid_counter.keys():
                    urid_counter[urid] += 1
                else:
                    urid_counter[urid] = 1
        f.close()
    for urid in urid_counter.keys():
        print(urid,urid_counter[urid])
    print("\n\n")


if __name__ == '__main__':
    main()