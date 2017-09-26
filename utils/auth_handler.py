import requests
import json

class AuthHandler(object):

    def __init__(self, config=None):
        self.userName=config.USER_NAME
        self.password=config.PASSWORD
        self.url=config.AUTH_URL

    def authenticate(self):
        headers = {'content-type': 'application/json'}
        r = requests.post(url=self.url, data="{\"userName\":\""+ self.userName+"\", \"password\":\""+ self.password+"\"}",
                          headers=headers)
        retval=r.json()
        self.token=retval['id_token']

    def get_token(self):
        return self.token



