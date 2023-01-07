import requests
from bs4 import BeautifulSoup
from functools import lru_cache

br_flag = False
ced_flag = False
am_flag = False
idiom_flag = False
ex_flag = False


@lru_cache()
def get_soup(word):
    word = word.replace(' ', '-')
    headers = {"Accept": "*/*",
               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0"}
    url = 'https://www.collinsdictionary.com/dictionary/english/' + word
    req = requests.get(url, headers=headers)
    src = req.text
    with open('index.html', 'w', encoding="utf-8") as file:
        file.write(src)
    soup = BeautifulSoup(src, 'lxml')
    if soup.find('div', class_='suggest_new_word_wrapper'):
        return None
    else:
        return soup


def get_word_contents(soup):
    word_contents = []
    global br_flag, ced_flag, am_flag
    br_flag = ced_flag = am_flag = False
    if soup.find('div', class_='cB cB-def cobuild br') is not None:
        word_contents_br = soup.find_all('div', class_='cB cB-def cobuild br')
        word = get_word(word_contents_br)
        for word_content in word_contents_br:
            if word in word_content.find('span', class_='orth').text:
                br_flag = True
                word_contents.append(word_content)
    elif soup.find('div', class_='cB cB-def ced') is not None:
        word_contents_ced = soup.find_all('div', class_='cB cB-def ced')
        word = get_word(word_contents_ced)
        for word_content in word_contents_ced:
            if word in word_content.find('span', class_='orth').text:
                ced_flag = True
                word_contents.append(word_content)
    elif soup.find('div', class_='cB cB-def american') is not None:
        word_contents_am = soup.find_all('div', class_='cB cB-def american')
        word = get_word(word_contents_am)
        for word_content in word_contents_am:
            if word in word_content.find('span', class_='orth').text:
                am_flag = True
                word_contents.append(word_content)
    return word_contents


def get_word(word_contents):
    word = word_contents[0].find('span', class_='orth')
    return word.text


def get_hom_tags(word_contents):
    for word_content in word_contents:
        if br_flag:
            definition_content = word_content.find('div', class_='content definitions cobuild br')
        if ced_flag:
            definition_content = word_content.find('div', class_='content definitions ced')
        if am_flag:
            definition_content = word_content.find('div', class_='content definitions american')
        hom_tags = definition_content.find_all(lambda tag: tag.name == 'div' and
                                                           tag.get('class') == ['hom'])
        for hom in hom_tags:
            if hom.find('span', 'gramGrp pos') is not None or hom.find('span', 'pos') is not None or \
                    hom.find('span', 'gramGrp'):
                yield hom


# присвой ворд контент нон в гет ворд контент файнд алл
# thrift store (take word plaing in consider while fixing this), raining cats and dogs
# когда будешь обрабатывать homs учти что иногда в одном hom лежит много значений например baton (american)
# hospitalit и finance

