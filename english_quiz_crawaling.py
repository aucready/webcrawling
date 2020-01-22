import requests
from bs4 import BeautifulSoup
import re
import json
import random




def get_news():
    url = 'https://www.usatoday.com'
    r = requests.get(url)
    bs = BeautifulSoup(r.text, 'lxml')
    lists = bs.select('div.gnt_m_th > a.gnt_m_th_a' )
    for li in lists:
        href =url + li['href']
        r = requests.get(href)
        bs = BeautifulSoup(r.text, 'lxml')
        texts = bs.select('div.gnt_ar_b > p.gnt_ar_b_p')
        contents = []
        for p in texts:
            contents.append(p.text)
        contents = ''.join(contents)
        print(contents)
        return contents.lower()
    return None

def naver_translate(word):
    try:
        url = 'https://ac.dict.naver.com/enkodict/ac?st=11001&r_lt=11001&q={}&'.format(word)
        r = requests.get(url)
        j = json.loads(r.text)
        return (j['items'][0][0][1][0])
    except:
        return None




# print(news)

def make_quiz(news):
    match_patern = re.findall(r'\b[a-z]{4,15}\b', news)
    frequency = {}
    quiz_list = []
    for word in match_patern:
        count = frequency.get(word, 0)
        frequency[word] = count + 1

    for word, count in frequency.items():
        # print(word, count)
        if count > 1:
            kor = naver_translate(word)
            if kor is not None:
                quiz_list.append({kor: word})

    return quiz_list


def quize():

    quiz_list = make_quiz(get_news())
    random.shuffle(quiz_list)

    chance = 5
    count = 0
    for q in quiz_list:
        count += 1
        kor = list(q.keys())[0]
        english = q.get(kor)
        print('*' * 90)
        print('문제:{}'.format(kor))
        print('*' * 90)

        for j in range(chance):
            user_input = input('위의 뜻을 가지는 영어단어는 무었인가요?')
            usr_input = str(user_input.lower().strip())

            if usr_input == english:
                print('정답!!!!!!!입니다.{}문제 남았습니다.'.format(len(quiz_list) - count))
                break

            else:
                n = chance - (j+1)

                if j == 0:
                    hint = ' _ ' * int(len(english) - 1)
                    print('{}는 정답이 아닙니다. 기회가 {}번 남았습니다.힌트 {} {}'.format(usr_input, n, english[0], hint))

                elif j == 1:
                    hint = ' _ ' * int(len(english) - 2)
                    print('{}는 정답이 아닙니다. 기회가 {}번 남았습니다.힌트 {} {} {}'.format(usr_input, n, english[0], english[1], hint))

                elif j == 2:
                    hint = ' _ ' * int(len(english) - 3)
                    print('{}는 정답이 아닙니다. 기회가 {}번 남았습니다.힌트 {} {} {} {}'.format(usr_input, n, english[0], english[1], english[2], hint))

                elif j == 3:
                    hint = ' _ ' * int(len(english) - 4)
                    print('{}는 정답이 아닙니다. 기회가 {}번 남았습니다.힌트 {} {} {} {} {}'.format(usr_input, n, english[0],english[1], english[2], english[3], hint))
                else:
                    print('틀렷습니다.정답은{} 입니다.'.format(english))

    print('더이상 문제가 없습니다.')



quize()
