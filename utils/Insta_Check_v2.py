######################################
#   By Kumaran D
#   CA Instantiation script.
#   Given a file with conversation ids, check each of them for CA Instantiation.
#   Refer to the confluence page to understand what the script intends to do
######################################
import time
from selenium import webdriver
from collections import defaultdict
import datetime

code_id_list = [["CA Instantiation", "28673"]]

CODE_ID_INDEX = 7
LOG = False
analytics = defaultdict(list)
HAMMER = "http://80.238.29.159/ham/test1/NotificationReport.aspx"


def print_line(*argv):
    if LOG is True:
        for matter in argv:
            print(matter)


def get_log_for_conv_id(driver, conv_id):
    logs = []
    elem = driver.find_element_by_id("TextBoxFromDate")
    elem.clear()
    elem.send_keys('2019-06-07 12:59')

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
        insta_check = {}
        insta_check['conv_id'] = conv_id
        insta_check['result'] = False
        for line in logs:
            split_line = line.split(' ')
            #print_line(split_line)
            if (len(split_line) > CODE_ID_INDEX) and (code_id[1] in split_line[CODE_ID_INDEX]):
                insta_check['result'] = True
                break
        analytics[code_id[0]].append(insta_check)


######main######
def main():

    driver = webdriver.Chrome()
    driver.get(HAMMER)
    assert "Notification Report" in driver.title
    driver.execute_script("javascript:hideShow()")
    time.sleep(1)

    for conv_id in range(559207622, 559207622+434):
        print_line("Conversation ID: " + str(conv_id))
        get_log_for_conv_id(driver, conv_id)
        #input("Press Enter to exit..")
    driver.close()
    for code_id in code_id_list:
        print("Activity: " + code_id[0])
        for matter in analytics[code_id[0]]:
            print("Conversation ID: ", matter["conv_id"], "Status: ", matter['result'])
        print("\n\n")


if __name__ == '__main__':
    main()