######################################
#   By Kumaran D
#   Normalised SSR NFT results extractor
#   Refer to the confluence page to understand what the script intends to do
######################################
import time
from selenium import webdriver
from collections import defaultdict
import datetime
############### ingest lists #################
conv_id_list = ["878242441"]
#                "21671508", "20560908", "12495484", "26771630", "4611458",
#                "16043234", "24438136", "1521522", "40133382", "9363592",
#                "34200310", "17647434", "40434478", "36938556", "21915840",
#                "4832344", "23101714", "32654108", "13936796", "20033990"]
code_id_list = [["CA Instantiation", "28673", "8705"], ["Offer Publish", "24578", "24577"]]
############### ingest lists #################

############### update lists #################
#conv_id_list = ["7218900", "31775500", "2503786", "15432404", "27534242",
#                "26412536", "10913496", "26118844", "5383942", "5467854",
#                "28158646", "33263704", "18212606", "32874994", "26042336",
#                "16167868", "26385388", "21292670", "33100816", "4539886",
#                "26308880", "23380598", "12426380", "9651114", "1229064"]
#code_id_list = [["Update Completed", "8215", "8705"]]
############### update lists #################

############### delete lists #################
#conv_id_list = ["34137376", "820610", "7914876", "27855082", "28528846",
#                "28752200", "25025520", "13376560", "33572204", "18950538",
#                "23006696", "15686608", "17556118", "37031106", "351690",
#                "15524954", "19392310", "21147058", "1517820", "13996028"]
#                "27762532", "19251634", "39945814", "31349770", "13622126"]
#code_id_list = [["Delete Completed", "24578", "24577"]]
#code_id_list = [["Delete Completed", "36866", "8705"]]
############### delete lists #################

#conv_id_list = ["429410653"]
#code_id_list = [["Update Completed", "8215", "8705"]]
CODE_ID_INDEX = 7
LOG = False
analytics = defaultdict(list)
HAMMER = "http://80.238.29.159/ham/Test1/NotificationReport.aspx"


def print_line(*argv):
    if LOG is True:
        for matter in argv:
            print(matter)


def insert_timing(time_list, matter):
    for i in range(0, len(time_list)):
        #print(time_list[i]["start_time"], matter["start_time"])
        if time_list[i]["start_time"] > matter["start_time"]:
            time_list.insert(i, matter)
            #print("date greater!!")
            return
    time_list.append(matter)


def get_log_for_conv_id(driver, conv_id):
    logs = []
    elem = driver.find_element_by_id("TextBoxFromDate")
    elem.clear()
    elem.send_keys('2019-06-04 12:59')

    elem = driver.find_element_by_id("TextBoxConversationId")
    elem.clear()
    elem.send_keys(conv_id)

    refresh = driver.find_element_by_id("ButtonApplyFilter")
    refresh.click()
    time.sleep(2)

    table_id = driver.find_element_by_id("GridView1")
    for tr in table_id.find_elements_by_tag_name("tr"):
        #print_line(tr.text)
        logs.append(tr.text)
    for code_id in code_id_list:
        timing_d = {}
        timing_d['conv_id'] = conv_id
        logtime1_found = False
        for line in logs:
            split_line = line.split(' ')
            #print_line(split_line)
            if (len(split_line) > CODE_ID_INDEX) and (code_id[1] in split_line[CODE_ID_INDEX]):
                logtime1 = datetime.datetime.strptime(split_line[0]+' '+split_line[1], '%d/%m/%Y %H:%M:%S')
                logtime1_found = True
                timing_d['end_time'] = logtime1
                #print_line("end_time", logtime1)
            if (len(split_line) > CODE_ID_INDEX) and (code_id[2] in split_line[CODE_ID_INDEX]) and logtime1_found is True:
                logtime2 = datetime.datetime.strptime(split_line[0]+' '+split_line[1], '%d/%m/%Y %H:%M:%S')
                #print_line("start_time", logtime2)
                timing_d['start_time'] = logtime2
                #print_line(code_id[0], " Delta: " + str((logtime1-logtime2).seconds))
                #print(logtime2.seconds)
                break;
        #print("timing_d", timing_d)
        insert_timing(analytics[code_id[0]], timing_d)


######main######
def main():
    driver = webdriver.Chrome()
    driver.get(HAMMER)
    assert "Notification Report" in driver.title
    driver.execute_script("javascript:hideShow()")
    time.sleep(1)

    for conv_id in conv_id_list:
        print_line("Conversation ID: " + conv_id)
        get_log_for_conv_id(driver, conv_id)
        #input("Press Enter to exit..")
    driver.close()
    for code_id in code_id_list:
        print("Normalised " + code_id[0] + " Timelines")
        for matter in analytics[code_id[0]]:
            print("Conversation ID:", matter["conv_id"])
            print("Start Time:", matter["start_time"])
            print("End Time:", matter["end_time"])
            print("Delta: " + str((matter["end_time"]-matter["start_time"]).seconds))
            #print((matter["end_time"]-matter["start_time"]).seconds)
        print("\n\n")


if __name__ == '__main__':
    main()