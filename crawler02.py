import requests
from bs4 import BeautifulSoup
from requests_html import HTMLSession
# session = HTMLSession()
# response = session.get('https://www.naver.com')
# print(response.html.links)
#





response = requests.get("https://www.naver.com")
bs = BeautifulSoup(response.text, "html.parser")
for img in bs.select("img"):
    print(img)
for a in bs.select('a'):
    print(a)






# print(response.status_code)
# print(response.headers)

# print(response.text)



