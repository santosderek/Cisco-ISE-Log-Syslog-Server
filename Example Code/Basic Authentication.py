import requests
import json
from pprint import pprint
from requests.auth import HTTPBasicAuth
base_url = 'https://10.122.109.116:9060'


def main():

    with open('../app/static/config.json') as config_file:
        json_result = json.load(config_file)
        username = json_result['username']
        password = json_result['password']
    req = requests.get(base_url + '/ers/config/adminuser',
                       auth=HTTPBasicAuth(username, password),
                       headers={'Accept': 'application/json'},
                       verify=False)
    print(req.text)


if __name__ == '__main__':
    main()
