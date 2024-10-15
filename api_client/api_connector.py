import json
import requests
import time
import threading
import os

class APIConnector(object):
    '''
        Data Handler
    '''
    _instance = None
    _app_info = {}
    app_token = {}
    _url_info = {}

    def __new__(cls, *args, **kwargs):
        '''
            Singleton implementation to allow only one instance of APIConnector.
        '''
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        '''
            Loading API and URL information from JSON files.
        '''        
        account_info = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'auth_info.json')
        url_info =  os.path.join(os.path.dirname(os.path.abspath(__file__)), 'api_info.json')

        with open(account_info, 'r')as f:
            self._api_info = json.load(f)

        with open(url_info, 'r')as f:
            self._url_info = json.load(f)
        self._start()

    def _start(self):
        '''
            Starting the token refresh job for all specified apps.
        '''
        # auth token first (app = app name, info = username, password)
        for app, info in self._api_info.items():
            self.app_token[app] = self._auth_token(
                info['username'], info['password'])

        t1 = threading.Thread(
            target=self._create_refresh_job, args=self._api_info.keys())
        t1.start()

    def _create_refresh_job(self, *args):
        '''
            Background job to continuously refresh tokens.
        '''
        while(True):
            for app in args:
                self._refresh_token(app)
            time.sleep(880)

    def _refresh_token(self, app):
        '''
            Method to refresh tokens.
        '''
        request_header = {"Content-Type": "application/json"}
        request_body = {"refresh": self.app_token[app]['refresh']}
        response = requests.post(self._url_info['refresh_token_url'],
                                 data=json.dumps(request_body), headers=request_header)
        if response.status_code != 200:
            self.app_token[app] = self._auth_token(
                self._app_info[app]['username'], self._app_info[app]['password'])

        self.app_token[app] = response.json()

    def _auth_token(self, username, password):
        '''
            Authentication method to get API tokens based on username and password
        '''
        response = requests.post(self._url_info['get_token_url'], data={
            "username": username,
            "password": password
        })
        api_token = response.json()
        return api_token

    def send_request_to_apigw(self, api_url, token=None, request_body=None):
        '''
            Sending requests to the API gateway with the provided token.
        '''
        request_header = {
            "Authorization": f"Bearer {token['access']}",
            "Content-Type": "application/json"
        }

        response = requests.post(api_url, data=json.dumps(
            request_body), headers=request_header)
        if (response.status_code == 401):
            token = self._refresh_token(token['refresh'])
            request_header["Authorization"] = f"Bearer {token['access']}"
            response = requests.post(api_url, data=json.dumps(
                request_body), headers=request_header)

        return response

    def get_quotes(self, dataname=None):
        '''
            Method to get quotes data from the API.
        '''
        url = self._url_info['get_quotes']
        request_body = {
            "dataname": dataname,
        }
        response = self.send_request_to_apigw(
            url, self.app_token['technical_analysis'], request_body)
        if response.status_code == 200:
            res = response.json()['detail']         
            return res
        
        elif response.status_code == 404:
            return None
        else:
            print("Something wrong , status code:",
                  response.status_code)
            print(response.json())
            return None
        
    def get_signal(self):
        '''
            Method to get quotes data from the API.
        '''
        url = self._url_info['test']
        request_body = {
        }
        response = self.send_request_to_apigw(
            url, self.app_token['technical_analysis'], request_body)
        
        if response.status_code == 200:
            res = response.json()['msg']         
            return res
        
        elif response.status_code == 404:
            return None
        else:
            print("Something wrong , status code:",
                  response.status_code)
            print(response.json())
            return None