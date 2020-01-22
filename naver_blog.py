import requests
from bs4 import BeautifulSoup



def get_search_naver_blog(query, start_page = 1, end_page=None):
    start = (start_page - 1)*10 +1

    url = 'https://search.naver.com/search.naver?where=post&sm=tab_jum&query={}&start={}'.format(query, start)


    r = requests.get(url)
    bs = BeautifulSoup(r.text, 'lxml')
    result = []
    if end_page is None:
        #41-50 / 6,670건
        tot_counts = bs.select('span.title_num')[0].text
        tot_counts.splte('/')[-1]

        tot_counts.replace('건', '').replace(',', '').strip()
        end_page = tot_counts / 10

        if end_page > 900:
            end_page = 900

    lis = bs.select('li.sh_blog_top')

    for li in lis:
        try:

            thumbnail = li.select('img')[0]['src']
            title = li.select('dl > dt > a')[0]
            sumury = li.select('dl > dd.sh_blog_passage')[0].text
            title_link = title['href']
            title_text = title.text

            result.append((thumbnail, title_text, title_link, sumury))

        except:
            continue

    if start_page < end_page:
        start_page += 1
        result.extend(get_search_naver_blog(query, start_page=start_page, end_page=end_page))


    return result



results = get_search_naver_blog('파이썬강좌', start_page=1, end_page=3)
j = 0

for result in results:
    j += 1
    print(result)
    print('-'*90 + '{}'.format(j))







