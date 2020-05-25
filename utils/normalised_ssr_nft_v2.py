######################################
#   By Kumaran D
#   Normalised SSR NFT results extractor v2
#   Refer to the confluence page to understand what the script intends to do
######################################
import time
import os
import re
import datetime

LOG = True
####################SSR Asset Add analytics##########
#ID_FILE = 'urid.txt'
#ANALYTICS_DIR = 'C:\\Work\\G7\\SSR NFT\\ingest_nft\\ingest\\Stage\\R18\\'
#start_catch = ['SSR', 'Stored Procedure', 'SQL']
#end_catch = ['succeeded', 'RQT']
####################SSR Asset Add analytics##########

####################SSR Classif Add analytics##########
ID_FILE = 'classif_ids.txt'
ANALYTICS_DIR = 'C:\\Work\\G7\\SSR NFT\\classification nft\\Stage\\add\\R18\\'
start_catch = ['CREATE_CLASSIF_TERM', 'create_classif_attribute']
end_catch = ['succeeded', 'RQT']
####################SSR Classif Add analytics##########

####################SSR Classif delete analytics##########
#ID_FILE = 'classif_ids.txt'
#ANALYTICS_DIR = 'C:\\Work\\G7\\SSR NFT\\classification nft\\Stage\\delete\\R11\\'
#start_catch = ['delete_si_classif_term']
#end_catch = ['succeeded', 'RQT']
####################SSR Classif Add analytics##########

def print_line(*argv):
    if LOG is True:
        for matter in argv:
            print(matter)


######main######
def main():
    urid_list = []

    total_time = 0

    f = open(ANALYTICS_DIR + ID_FILE, "r")
    for line in f:
        urid_list.append(line.strip('\n\r'))
    f.close()
    delta = 0
    for filename in os.listdir(ANALYTICS_DIR):
        if bool(re.search('Xmlfile', filename)) is False:
            continue
        f = open(ANALYTICS_DIR + filename, "r")
        filetext = f.read()
        if any(x in filetext for x in start_catch):
            for urid in urid_list:
                #print_line("Urid ID: " + urid)
                    if re.search(urid, filetext):
                        #print(urid.strip('\n\r'), filename)
                        f.seek(0)
                        start_found = False
                        for line in f.readlines():
                            if any(x in line for x in start_catch) and start_found is False:
                                split_line = line.split(' ')
                                start_time = datetime.datetime.strptime(split_line[0]+' '+split_line[1], '%Y/%m/%d %H:%M:%S.%f')
                                start_found = True
                                continue

                            if any(x in line for x in end_catch) and start_found is True:
                                split_line = line.split(' ')
                                end_time = datetime.datetime.strptime(split_line[0]+' '+split_line[1], '%Y/%m/%d %H:%M:%S.%f')
                                delta = float(float((end_time - start_time).microseconds)) / 1000
                                break;
                    if delta != 0:
                        print(filename, start_time, end_time, delta, "ms")
                        #print(filename)
                        #print(delta)
                        total_time += delta
                        delta = 0
        f.close()
    print("Total time: ", total_time, "ms")
    print("\n\n")


if __name__ == '__main__':
    main()