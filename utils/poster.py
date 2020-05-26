import requests
import uuid
from datetime import datetime

GUID = '{"commsHubId":"AD-00-00-00-00-07-B4-A4","businessTargetId":"AD-00-00-FD-00-07-B4-A4"} \n'


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

    def __init__(self, guids):
        self.guids = guids

    def post_it(self):
        try:
            # print(self.BODY_PART)
            r = requests.post(self.URL, data=self.BODY_PART, headers=self.HEADERS)
            r.raise_for_status()
            print(r.content)
        except requests.exceptions.HTTPError as e:
            print(e.response.text)

    def runner(self):
        current_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        print("Starting Meter Firmware request at", current_time)
        uuid_string = str(uuid.uuid1())
        print("Posting: ", uuid_string, "with ", self.guids.count('\n'), "GUID(s)....")
        self.BODY_PART = self.BODY_PART.replace('UUID', uuid_string)
        self.BODY_PART = self.BODY_PART.replace('JSON_BODY', self.guids)
        self.post_it()
        current_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        print("Ending Meter Firmware request at", current_time)


def main():
    pB = PosterBoy(GUID)
    pB.runner()


if __name__ == '__main__':
    main()
