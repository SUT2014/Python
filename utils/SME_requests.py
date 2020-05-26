import requests
import uuid
from datetime import datetime

SPREAD_FILE = 'C:\\Work\\DMM Test\\Spread.txt'
SME_GUID = 'C:\\Work\\DMM Test\\SME_GUIDs.txt'


class PosterBoy:
    URL = 'http://172.20.209.72:8080/dsp-stub/ref2/firmwareUpgrade'
    HEADERS = {'Content-Type': 'application/json'}
    BODY_PART = """{
                    "firmwareUpgrade":{
                    "requestId":"UUID",
                    "approvedFirmwareVersionId":"OTAFile_A114_GSME_ZAZ1_Signature",
                    "firmwareImageHash":"4UdytM5H2K11h/xTCJM0g3yDgjvHhAKc1Bn8rfygWIM=",
                    "totalParts":1,
                    "partNumber":1,
                    "deliveryPoint":[ JSON_BODY ]
                    }
                }"""

    def post_it(self, body):
        try:
            r = requests.post(self.URL, data=body, headers=self.HEADERS)
            r.raise_for_status()
            print(r.content)
        except requests.exceptions.HTTPError as e:
            print(e.response.text)

    def runner(self, guids):
        current_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        print("Starting Meter Firmware request at", current_time)
        uuid_string = str(uuid.uuid1())
        print("Posting: ", uuid_string, "with ", guids.count('\n'), "GUID(s)....")
        body = self.BODY_PART.replace('UUID', uuid_string)
        body = body.replace('JSON_BODY', guids)
        #print(body)
        self.post_it(body)
        current_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        print("Ending Meter Firmware request at", current_time)


def file_length(file_name):
    fP = open(file_name, "r")
    lines = sum(1 for line in fP)
    fP.close()
    return lines


def main():
    spread_file = open(SPREAD_FILE, "r")
    spread_bits = spread_file.readline().split(',')
    spread_file.close()
    no_of_GUIDs = file_length(SME_GUID)
    guid_file = open(SME_GUID, "r")
    pB = PosterBoy()
    for bits in spread_bits:
        portion = int((no_of_GUIDs * int(bits)) / 100)
        # print(portion)
        guids = ''
        for i in range(0, portion):
            guids += guid_file.readline()
        # print(guids)
        guids = guids.rstrip(',\n')
        pB.runner(guids)
    guid_file.close()


if __name__ == '__main__':
    main()
