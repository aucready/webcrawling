import requests
from bs4 import BeautifulSoup



def hot_deal(keyword):
    url = 'https://slickdeals.net/newsearch.php?src=SearchBarV2&q={}&pp=20'.format(keyword)
    r = requests.get(url)
    bs = BeautifulSoup(r.text, 'lxml')

    rows = bs.select('div.resultRow')

    result = []

    for r in rows:
        link =r.select('a.dealTitle')[0]
        href = link.get('href')
        if href is None:
            continue
        href = 'https://slickdeals.net' + href
        title = link.text

        price = r.select('span.price')[0].text.replace('$', '').replace('from', '').replace(',','').strip()
        if price.find('/') >= 0 or price.find('to') > 0 or price == '':
            continue
        price = float(price)

        hot = len(r.select('span.icon-fire'))
        result.append((title, href, price, hot))

    return result


collect_data = hot_deal('macbook')

for coll in collect_data:
    print(coll)








#
# for p in hot_deal(keyword):
#     print(p)



#
# for p in hot_deal('ipad'):
#
#     print(p)










