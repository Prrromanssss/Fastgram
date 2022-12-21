import json

import requests

url = 'https://www.cdek.ru/ru/cabinet/api/483/cost'
my_json_data = json.load(open('request.json'))
headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8',
           'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
           'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0'
           'YaBrowser/22.11.0.2500 Yowser/2.5 Safari/537.37}'}
response = requests.post('https://www.cdek.ru/ru/cabinet/api/483/cost',
                         headers=headers, json=my_json_data)
print(response)
print(response.text)
