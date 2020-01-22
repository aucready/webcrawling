import requests
from bs4 import BeautifulSoup


query = '파이썬강좌'
def get_search_naver_blog(query, start_page=1, end_page=None):
    #11 = (2-1)*10 + 1
    #21 = (3-1)*10 +1

    start = (start_page - 1)* 10 + 1



    url = 'https://search.naver.com/search.naver?where=post&sm=tab_jum&query={}&start={}'.format(query, start)
    print(url)
    r = requests.get(url)
    bs = BeautifulSoup(r.text, 'lxml')
    result = []


    if end_page is None:
        #1-10 / 7,495건
        tot_count = bs.select('span.title_num')[0].text
        tot_count = tot_count.split('/')[-1]
        tot_count = int(tot_count.replace(',', '').replace('건', '').strip())

        end_page = tot_count / 10

        if end_page > 900:
            end_page = 900


        # print(tot_count)


    lis = bs.select('li.sh_blog_top')
    for li in lis:
        try:
            thumbnail = li.select('img')[0]['src']
            title = li.select('dl > dt > a')[0]
            sumury = li.select('dl > dd.sh_blog_passage')[0].text

            title_link = title['href']
            title_text = title.text
            result.append((thumbnail, title_link, title_text, sumury))

        except:
            continue

    if start_page < end_page:
        start_page += 1
        result.extend(get_search_naver_blog(query, start_page = start_page, end_page = end_page))

    return result





results = get_search_naver_blog('안경', start_page=1,end_page=10)

j=0
for i in results:
    j += 1
    print(i)
    print('-'*90, '{}'.format(j))

