import requests
import json
from common.crmtoolconf import CrmTools


class CrmRequest:

    def __init__(self, url):
        self.url = url

    def get(self, parms=None):
        if parms:
            get_url = self.url + str(parms)
        else:
            get_url = self.url
        req = json.loads(requests.request('GET', url=get_url, headers=CrmTools.bbp_header).text)
        return req

    def post(self, data=None):
        if data:
            json_data = json.dumps(data)
        else:
            json_data = None
        req = json.loads(requests.request('POST', url=self.url, data=json_data, headers=CrmTools.bbp_header).text)
        return req
