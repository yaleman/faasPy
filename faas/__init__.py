import time
import json

import base64
import requests

class FaaSAPI(object):
    def __init__(self, apikey, apipassword, proxy):
        authbytes = "{}:{}".format(apikey, apipassword).encode('utf-8')
        self.authtoken = base64.encodebytes(authbytes).decode('utf-8').replace("\n", "")
        self.proxy = proxy
        
        self.access_token = 0
        self.access_token_expiry = time.time() - 120
    

    def accesstoken(self):
        if time.time() > self.access_token_expiry:
            
            url = "https://api.services.fireeye.com/token"
            payload = "grant_type=client_credentials"
            headers = {
                'Authorization': "Basic {}".format(str(self.authtoken)),
                'Cache-Control': "no-cache",
                'Content-Type': "application/x-www-form-urlencoded",
                }

            response = requests.post(url, data=payload, headers=headers, proxies=self.proxy)
            token = response.json()

            self.access_token = token['access_token']
            self.access_token_expiry = time.time() + token['expires_in'] - 60

        return self.access_token
    
    def get_investigations(self):
        headers = { 'Authorization' : "Bearer {}".format(self.accesstoken())}
        try:
            req = requests.get("https://api.services.fireeye.com/investigations", headers=headers, proxies=self.proxy)
        except Error as e:
            sys.exit("Error doing get_investigations: {}".format(e))
        if 'data' in req.json().keys():
            if 'objects' in req.json()['data'].keys():
                return req.json()['data']['objects']
        return False

    def get_investigation(self, investigationId):
        headers = { 'Authorization' : "Bearer {}".format(self.accesstoken())}
        try:
            req = requests.get("https://api.services.fireeye.com/investigations/{}".format(investigationId), headers=headers, proxies=self.proxy)
        except Error as e:
            sys.exit("Error doing get_investigation: {}".format(e))
        if req.status_code == 200:
            return req.json()['data']
        else: 
            return False
