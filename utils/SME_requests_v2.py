import requests
import uuid
from datetime import datetime
import time

SPREAD_FILE = '.\\TestData\\Spread.txt'
SME_GUID = '.\\TestData\\SME_GUIDs_60K.txt'
#DELAY = 120
DELAY = 1

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

    def runner(self, guids, count):
        current_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        print("Starting Meter Firmware request at", current_time)
        uuid_string = str(uuid.uuid1())
        print("Posting: ", uuid_string, "with ", count, "GUID(s)....")
        body = self.BODY_PART.replace('UUID', uuid_string)
        body = body.replace('JSON_BODY', guids)
        #print(body)
        #self.post_it(body)
        current_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        print("Ending Meter Firmware request at", current_time)


class SpreadFiler:
    def __init__(self, spread_file, guids_file):
        self.sfp = open(spread_file, "r")
        self.gfp = open(guids_file, "r")

    def guids_count(self):
        return sum(1 for line in self.gfp)

    def get_spread(self):
        count = self.guids_count()
        self.gfp.seek(0)
        print(count)
        return [(count * int(bits) / 100) for bits in (self.sfp.readline().split(','))]

    def get_next_guids(self, count):
        guid_lines = ''
        for i in range(0, count):
            guid_lines += self.gfp.readline()
        # print(guid_lines)
        return guid_lines.rstrip(',\n')

    def __del__(self):
        self.sfp.close()
        self.gfp.close()


def main():
    pB = PosterBoy()
    sf = SpreadFiler(SPREAD_FILE, SME_GUID)
    for i in sf.get_spread():
        guids = sf.get_next_guids(int(i))
        # print(guids)
        pB.runner(guids, int(i))
        print("Sleeping for ", DELAY, "Seconds..")
        time.sleep(DELAY)


if __name__ == '__main__':
    main()
