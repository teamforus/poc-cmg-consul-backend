import requests

BASE_URL = 'https://test.platform.forus.io/'
TOKEN_ACTIVE = 'active'


def get_auth_header(auth_token):
    return {'Authorization': 'Bearer ' + auth_token}


class ForusApi:

    @staticmethod
    def check_token(auth_token):
        payload = {'access_token': auth_token}
        r = requests.get(BASE_URL + 'api/v1/identity/proxy/check-token', params=payload)
        return r.json()['message'] == TOKEN_ACTIVE

    @staticmethod
    def get_records(auth_token):
        r = requests.get(BASE_URL + 'api/v1/identity/records', headers=get_auth_header(auth_token))
        return r.json()
