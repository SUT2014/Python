import time
from selenium import webdriver
import datetime

############### update lists #################
#conv_id_list = ["7218900", "31775500", "2503786", "15432404", "27534242",
#                "26412536", "10913496", "26118844", "5383942", "5467854",
#                "28158646", "33263704", "18212606", "32874994", "26042336",
#                "16167868", "26385388", "21292670", "33100816", "4539886",
#                "26308880", "23380598", "12426380", "9651114", "1229064"]
#code_id_list = [["Update Completed", "8215", "8705"]]
############### update lists #################

############### ingest lists #################
#conv_id_list = ["10508744", "8028404", "39009208", "28000694", "13206268",
#                "21671508", "20560908", "12495484", "26771630", "4611458",
#                "16043234", "24438136", "1521522", "40133382", "9363592",
#                "34200310", "17647434", "40434478", "36938556", "21915840",
#                "4832344", "23101714", "32654108", "13936796", "20033990"]
#code_id_list = [["CA Instantiation", "28673", "8705"], ["Offer Publish", "24578", "24577"]]
############### ingest lists #################

############### delete lists #################
conv_id_list = ["27762532", "19251634", "39945814", "31349770", "13622126"] #,
#                "28752200", "25025520", "13376560", "33572204", "18950538",
#                "23006696", "15686608", "17556118", "37031106", "351690",
#                "15524954", "19392310", "21147058", "1517820", "13996028",
#                "26459428", "19920462", "12072222", "11652662", "21559214"]
code_id_list = [["Delete Completed", "36866", "8705"]]
############### delete lists #################

#conv_id_list = ["429410653"]
CODE_ID_INDEX = 7
LOG = False

def print_line(*argv):
    if LOG is True:
        for matter in argv:
            print(matter)

def get_log_for_conv_id(driver, conv_id):
    logs = []
    elem = driver.find_element_by_id("TextBoxFromDate")
    elem.clear()
    elem.send_keys('2019-05-07 12:59')

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
        logtime1_found=False
        for line in logs:
            split_line = line.split(' ')
            #print_line(split_line)
            if (len(split_line) > CODE_ID_INDEX) and (code_id[1] in split_line[CODE_ID_INDEX]):
                logtime1 = datetime.datetime.strptime(split_line[0]+' '+split_line[1], '%d/%m/%Y %H:%M:%S')
                logtime1_found = True
                print_line(logtime1)
            if (len(split_line) > CODE_ID_INDEX) and (code_id[2] in split_line[CODE_ID_INDEX]) and logtime1_found is True:
                logtime2 = datetime.datetime.strptime(split_line[0]+' '+split_line[1], '%d/%m/%Y %H:%M:%S')
                print_line(logtime2)
                print_line(code_id[0], " Delta: " + str((logtime1-logtime2).seconds))
                print((logtime1-logtime2).seconds)
                break;



######main######
def main():
    driver = webdriver.Chrome()
    driver.get("http://80.238.29.159/ham/Test2/NotificationReport.aspx")
    assert "Notification Report" in driver.title
    driver.execute_script("javascript:hideShow()")
    time.sleep(1)

    for conv_id in conv_id_list:
        print_line("Conversation ID: " + conv_id)
        get_log_for_conv_id(driver, conv_id)
        #input("Press Enter to exit..")
    driver.close()

if __name__ == '__main__':
    main()