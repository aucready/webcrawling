import requests
from bs4 import BeautifulSoup
import json
import pprint
keyword = '서울시 마포구'

url = 'https://apis.zigbang.com/search?q={}'.format(keyword)

r = requests.get(url)
result = json.loads(r.text)
# print(result)
# pprint.pprint(result)

if result['success']:
    lat = result['items'][0]['lat']
    lng = result['items'][0]['lng']
print(lat, lng)

