import requests
from bs4 import BeautifulSoup
import time
import json

kakao_torken = 'pQ4tOD8xKAl4TjHIaL2PJ0LMMYlicUFhbdLIcwo9dZoAAAFv0GCLjQ'


# kakao_torken = 'xFCVqnTy4VvQ3cYKFUjWls9YeJGsW0e-Z5mK3YwopcFEAAAFvzjrHVg'


def send_kakako(text):
    header = {'Authorization': 'Bearer ' + kakao_torken}
    url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
    post = {
        "object_type": "text",
        "text": text,
        "link": {
            "web_url": "https://developers.kakao.com",
            "mobile_web_url": "https://developers.kakao.com"
        },
        "button_title": "바로 확인"
    }

    data = {'template_object': json.dumps(post)}

    r = requests.post(url, headers=header, data=data)

    print(r.text)


def hot_deal(keyword):
    url = 'https://slickdeals.net/newsearch.php?src=SearchBarV2&q={}&pp=20'.format(
        keyword)
    r = requests.get(url)
    bs = BeautifulSoup(r.text, 'lxml')

    rows = bs.select('div.resultRow')

    result = []

    for r in rows:
        link = r.select('a.dealTitle')[0]
        href = link.get('href')
        if href is None:
            continue
        href = 'https://slickdeals.net' + href
        title = link.text

        price = r.select('span.price')[0].text.replace(
            '$', '').replace('From', '').replace('from', '').replace(',', '').strip()
        if price.find('/') >= 0 or price.find('to') > 0 or price == '' or price.find(
                'Each') > 0 or price.find('From') > 0:
            continue

        price = float(price)

        hot = len(r.select('span.icon-fire'))
        result.append((title, href, price, hot))

    return result


send_list = []


def main():
    usr_input = input()
    keyword = usr_input.replace(' ', '+')

    max_price = 2000.0
    min_price = 90.0

    while True:
        result = hot_deal(keyword)
        if result is not None:
            for r in result:
                title, href, price, hot = r

                if min_price < price < max_price:
                    if hot == 1:
                        if title not in send_list:
                            msg = '{}-hot. {} {} {} '.format(
                                hot, price, title, href)
                            send_kakako(msg)
                            send_list.append(title)

        time.sleep(60 * 5)


main()


