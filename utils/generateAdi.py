#! /usr/bin/python

import csv
import random
import os
import datetime
import sys
from shutil import copyfile

input_filename = "ADI_TEMPLATE.xml"
options_filename = "options.csv"

if len(sys.argv) == 3:
    input_filename = sys.argv[1]
    options_filename = sys.argv[2]

print ("using arguments...Input file:" + input_filename+ ", Options file:"+ options_filename)
# creating new output directory
output_dir = "output/" + datetime.datetime.now().strftime("%Y%m%d%H%M%S")
try:
    os.makedirs(output_dir)
except OSError:
    print ("Cannot create Output Directory - " + output_dir + "!!!, Exiting..")
    exit(-1)

options_file = open(options_filename, "r")
# read csv file, parse
options = csv.DictReader(options_file)

# outer loop, every option entry
for option in options:
    random_number = random.randint(1000000000000000, 9999999999999999)
    output_filename = output_dir +"/"+ str(random_number) + ".xml"
    output_file = open(output_filename, "w")
    input_file = open(input_filename, "r")
    for line in input_file:
        if "%%" in line:
            for token in (line.split("%%")):
                # print("Token="+token)
                if "RANDOM" in token:
                    line = line.replace("%%RANDOM%%", str(random_number))
                    line = line.replace("%%RANDOM1%%", str(random_number+1))
                    line = line.replace("%%RANDOM2%%", str(random_number+2))
                    line = line.replace("%%RANDOM3%%", str(random_number+3))
                elif token in option.keys():
                    line = line.replace("%%" + token + "%%", str(option.get(token)))
                miniToken = token.split(":")
                if (len(miniToken) > 1):
                    if "PART" in miniToken[1]:
                        line = line.replace("%%" + token + "%%", str(option.get(miniToken[0])).split("/")[-1])
                    elif "FULL" in miniToken[1]:
                        line = line.replace("%%" + token + "%%", str(option.get(miniToken[0])))
        # print(line)
        output_file.write(line)
    output_file.close()
    input_file.close()

options_file.close()
#copyfile(input_filename, output_dir+'/'+input_filename.rsplit('/',1)[1])
copyfile(options_filename, output_dir+'/'+options_filename.rsplit('/',1)[1])
print("Output XMLs in:"+output_dir)
