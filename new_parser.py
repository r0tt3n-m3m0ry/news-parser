# -*- coding: utf-8 -*-

try:
    from vk_api.longpoll import VkLongPoll, VkEventType
    from bs4 import BeautifulSoup as bs
    import requests
    import vk_api
except ImportError:
    print('Необходимо установить пакеты из файла requirements.txt')

from datetime import datetime
from ftplib import FTP
import sqlite3
import random
import time
import os

delay = 900

# 'РИА': 'ria', 'Известия': 'iz', 'RussiaToday': 'rt', 'BBC': 'bbc', 'Вести': 'vesti', 'ТВЭЛ': 'tvel', 'РБК': 'rbk', 'Коммерсант': 'komm', 
#  'Новости Новоуральска': 'novouralsknews', 'Администрация Новоуральского городского округа': 'admngo', 'Новоуральская вещательная компания': 'novouralsktv', 'Газета "Нейва"': 'neyvanews', 'Новоуральская газета': 'nugazeta'

site_names = {'Телерадиокомпания Зеленогорск': 'trkzelenogorsk', 'Сегодняшняя газета': 'sgzt', 'ПО "Электрохимический завод"': 'ecp', 'Афонтово': 'afontovo', 'Красное знамя': 'krznamya', 'Glazov Life': 'glazovlife', 'ЧМЗ': 'chmz'}

keywords = ['ядерный', 'атомный', 'твэл', 'росатом', 'атомная станция', 'атомное топливо', 'нейтрино', 'атомный реактор', 'атомный ледокол', 'атомная энергетика', 'ядерная установка', 'ядерные исследования', 'атомные источники тока', 'термоядерный синтез', 'вниинм', 'чмз', 'чепецкий механический завод', 'аэхк', 'ангарский электролизный химический комбинат', 'энергетика']

keywords_new = ['ТВЭЛ', 'Росатом', 'наука', 'энергия','Филимонов', 'цирконий', 'уран', 'кальций', 'сверхпроводниковая продукция', 'титан', 'Анищук', 'Россия', 'лето', 'карнавал']

parsed, new_news = [], []

# Полина = редиска, бросила меня(

vk_admin_id = 221003515
vk_public_id = -193536475

ftp_login = 'xtagfnap_python'
ftp_password = '45xyz625'

vk_token_bot = '5e0ec624a9904b970aadde6f3d40dc22b83e270b2e7709c457eb5706c9b11a52a111a846086ec2eb1c2d0'
vk_token_posting = '7b9f75ed8adabebe1a5ffadd54fb5090d31b9c5ae5bd08e3a2e7589cff42dfb56fddb1b5fbfbe9666143b'

vk_bot = vk_api.VkApi(token=vk_token_bot)
longpoll = VkLongPoll(vk_bot)
vk = vk_bot.get_api()

vk_posting = vk_api.VkApi(token=vk_token_posting)

def post_parsed_news_vk(post):
    vk_posting.method('wall.post', {'owner_id': vk_public_id, 'from_group': 1, 'message': f'{post[0]}. Источник: {post[-1]}. Подробнее: {post[1]}. '})

def post_parsed_news_fb():
    return 1

def send_message(message):
    vk.messages.send(user_id=vk_admin_id, random_id=random.randint(-999999999999, 999999999999), message=message)
    
def send_message_to_developer(message):
    vk.messages.send(user_id=565312948, random_id=random.randint(-999999999999, 999999999999), message=message)

def send_message_with_keyboard(message):
    vk.messages.send(user_id=vk_admin_id, random_id=random.randint(-999999999999, 999999999999), message=message, keyboard=open('keyboard.json').read())

def send_parsed_news(element):
    try:
        send_message_with_keyboard(f'Найдена новость: {element[0]}. Ссылка: {element[1]}. Источник: {element[2]}.')
        print(f'\n[{datetime.now().strftime("%H:%M:%S")}] [INFO] Отправлена на модерацию новость:\n\n{element[0]}\n{element[1]}\n\nИсточник: {element[2]}')
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
                if event.text:
                    if event.from_user:
                        if event.text == 'Дубликат':
                            print(f'\n\n=====ДУБЛИКАТ=====\n\n{element}\n\n=====КОНЕЦ ДУБЛИКАТА=====')
                            send_message('Новость не будет опубликована. Разработчик уведомлен.')
                            send_message_to_developer(f'\n\n=====ДУБЛИКАТ=====\n\n{element}\n\n=====КОНЕЦ ДУБЛИКАТА=====')
                            
                            return 0
                        if event.text == 'Не опубликовывать':
                            print(f'\n[{datetime.now().strftime("%H:%M:%S")}] [ОТВЕТ] {event.text}')
                            send_message('Новость не будет опубликована')
                            return 0
                        elif event.text == 'Опубликовать сейчас':
                            print(f'\n[{datetime.now().strftime("%H:%M:%S")}] [ОТВЕТ] {event.text}')
                            try:
                                post_parsed_news_vk(element)
                                send_message('Новость опубликована в вк!')
                                print(f'[{datetime.now().strftime("%H:%M:%S")}] [INFO] Новость опубликована в VK!')
                            except:
                                send_message('[ОШИБКА] Новость не была опубликована в VK. Работа программы продолжается.')
                            try:
                                post_parsed_news_fb(element)
                                send_message('Новость опубликована в facebook!')
                            except:
                                send_message('[ОШИБКА] Новость не была опубликована в Facebook. Работа программы продолжается.')
                            return 0
    except:
        send_message('Превышено время ожидания ответа. Отправляем новое сообщение с тем же содержимым..')
        send_parsed_news(element)
        print(f'[{datetime.now().strftime("%H:%M:%S")}] [INFO] Превышено время ожидания ответа')

def ftp_upload():
    ftp = FTP('xtagfnap.beget.tech')
    ftp.login(ftp_login, ftp_password)
    ftp.delete('parser.db')
    db_file = open('parser.db', 'rb')
    ftp.storbinary('STOR ' + 'parser.db', db_file)
    db_file.close()
    ftp.close()

def parse_ria():
    for keyword in keywords:
        try:
            ria = bs(requests.get(f'http://ria.ru/search?query={keyword}').text, 'html.parser')
        except: continue
        news = ria.find_all('div', {'class': 'list-item'})
        for element in news:
            try:
                title = element.find_all('span')[-1].attrs['data-title']
                link = element.find_all('span')[-1].attrs['data-url']
            except: continue
            parsed.append((title, link, 'РИА'))

def parse_iz():
    for keyword in keywords:
        try:
            iz = bs(requests.get(f'http://iz.ru/search?text={keyword}').text, 'html.parser')
        except: continue
        news = iz.find_all('div', {'class': 'view-search'})
        for element in news:
            title = element.find_all('a')[0].text
            link = element.find_all('a')[0]['href']
            parsed.append((title, link, 'Известия'))

def parse_bbc():
    for keyword in keywords:
        try:
            bbc = bs(requests.get(f'http://bbc.com/russian/search?q={keyword}').text, 'html.parser')
        except: continue
        news = bbc.find_all('div', {'class': 'hard-news-unit'})
        for element in news:
            title = element.find('a').text
            link = element.find('a', href=True)['href']
            parsed.append((title, link, 'BBC'))

def parse_rt():
    for keyword in keywords:
        try:
            rt = bs(requests.get(f'http://russian.rt.com/search?q={keyword}').text, 'html.parser')
        except: continue
        news = rt.find_all('li', {'class': 'listing__column'})
        for element in news:
            title = element.find('a', {'class': 'link'}).text.strip()
            link = 'http://russian.rt.com' + element.find('a', {'class': 'link'}, href=True)['href']
            parsed.append((title, link, 'RussiaToday'))
            
def parse_vesti():
    for keyword in keywords:
        try:
            vesti = bs(requests.get(f'http://vesti.ru/search?q={keyword}').text, 'html.parser')
        except: continue
        news = vesti.find_all('div', {'class': 'search-item'})
        for element in news:
            title = element.find('a').text
            link = 'http://vesti.ru' + element.find('a', href=True)['href']
            if title != '':
                parsed.append((title, link, 'Вести'))
        
def parse_tvel():
    for keyword in keywords:
        try:
            tvel = bs(requests.get(f'http://tvel.ru/search/index.php?q={keyword}').text, 'html.parser')
        except: continue
        news = tvel.find_all('div', {'class': 'search-list-title'})
        for element in news:
            title = element.text.strip()
            link = 'http://tvel.ru' + element.find('a', href=True)['href']
            parsed.append((title, link, 'ТВЭЛ'))
        
def parse_rbk():
    for keyword in keywords:
        try:
            rbk = bs(requests.get(f'http://rbc.ru/search/?project=rbcnews&query={keyword}').text, 'html.parser')
        except: continue
        news = rbk.find_all('div', {'class': 'search-item'})
        for element in news:
            title = element.find('span', {'class': 'search-item__title'}).text
            link = element.find('a', href=True)['href']
            parsed.append((title, link, 'РБК'))
            
def parse_komm():
    date_today = datetime.now().strftime('%d.%m.%Y')
    for keyword in keywords:
        try:
            komm = bs(requests.get(f'http://kommersant.ru/search/results?places=&categories=&isbankrupt=&datestart={date_today}&dateend={date_today}&sort_type=0&sort_dir=&regions=&result_count=&page=1&search_query={keyword}&sort_by=0&search_full=1&time_range=2&dateStart={date_today}&dateEnd={date_today}').text, 'html.parser')
        except: continue
        news = komm.find_all('div', {'class': 'search_results_item'})
        for element in news:
            title = element.find_all('a')[-2].text.strip()
            link = 'http://kommersant.ru' + element.find_all('a', href=True)[-1]['href']
            if 'Главные новости к' not in title:
                parsed.append((title, link, 'Коммерсант'))            
            
# =====Electrostal_START=====
def parse_inelstal():
    for keyword in keywords:
        try:
            inelstal = bs(requests.get(f'http://inelstal.ru/search?q={keyword}&global=0&category%5B%5D=новости').text, 'html.parser')
        except: continue
        news = inelstal.find_all('div', {'class': 'search-result-itm'})
        for element in news:
            title = element.find('a').text
            link = element.find('a', href=True)['href']
            parsed.append((title, link, 'Новости Электросталь'))

def parse_vrt():
    for keyword in keywords:
        try:
            vrt = bs(requests.get(f'http://vrt.tv/search.html?query={keyword}').text, 'html.parser')
        except: continue
        news = vrt.find_all('div', {'class': 'search-list-row'})
        for element in news:
            title = element.find('a').text
            link = 'http://vrt.tv/' + element.find('a', href=True)['href']
            parsed.append((title, link, 'Восточный региональный телеканал'))

def parse_vostexpress():
    for keyword in keywords:
        try:
            vostexpress = bs(requests.get(f'http://vostexpress.info/?s={keyword}').text, 'html.parser')
        except: continue
        news = vostexpress.find_all('article')
        for element in news:
            title = element.find('a').text
            link = element.find('a', href=True)['href']
            parsed.append((title, link, 'Восточный экспресс'))
            
def parse_tv360():
    for keyword in keywords:
        try:
            tv360 = bs(requests.get(f'http://360tv.ru/search/?q={keyword}').text, 'html.parser')
        except: continue
        news = tv360.find_all('div', {'class': 'news-list-wrapper'})
        for element in news:
            title = element.find('p').text
            link = 'http://' + element.find('a', href=True)['href'][2:]
            parsed.append((title, link, '360 TV'))
            
def parse_electrostal():
    for keyword in keywords:
        try:
            iz = bs(requests.get(f'http://search.electrostal.ru/?search={keyword}').text, 'html.parser')
        except: continue
        news = iz.find('div', {'class': 'workspace'}).find_all('a', href=True)
        for element in news:
            title = element.text
            link = element['href']
            parsed.append((title, link, 'Электросталь'))
# =====Electrostal_END=====

# =====Zelenogorsk_START=====
def parse_trkzelenogorsk():
    for keyword in keywords_new:
        try:
            trk = bs(requests.get(f'http://trkzelenogorsk.ru/news/itemlist/search?searchword={keyword}&categories=').text, 'html.parser')
        except: continue
        news = trk.find_all('h2', {'class': 'genericItemTitle'})
        for element in news:
            title = element.find('a').text.strip()
            link = 'http://trkzelenogorsk.ru' + element.find('a', href=True)['href']
            parsed.append((title, link, 'Телерадиокомпания Зеленогорск'))
            
def parse_sgzt():
    for keyword in keywords_new:
        try:
            sgzt = bs(requests.get(f"http://sgzt.com/?search_rubric=&search_day_from=01&search_month_from=01&search_year_from={datetime.now().strftime('%Y')}&search_day_to={datetime.now().strftime('%d')}&search_month_to={datetime.now().strftime('%m')}&search_year_to={datetime.now().strftime('%Y')}&search_place=1&search_logic=1&query={keyword}&go.x=6&go.y=4&module=search").text, 'html.parser')
        except: continue
        news = sgzt.find_all('div', {'class': 'article-name'})
        for element in news:
            title = element.find('a').text
            link = 'http://sgzt.com/' + element.find('a', href=True)['href']
            parsed.append((title, link, 'Сегодняшняя газета'))
            
def parse_ecp():
    for keyword in keywords_new:
        try:
            ecp = bs(requests.get(f'http://www.ecp.ru/search/node/{keyword}/1/1/1').text, 'html.parser')
        except: continue
        news = ecp.find('div', {'class': 'content'}).find_all('a', href=True)
        for element in news:
            title = element.text.strip()
            link = 'http://ecp.ru' + element['href']
            parsed.append((title, link, 'ПО "Электрохимический завод"'))
            
def parse_afontovo():
    for keyword in keywords_new:
        try:
            afontovo = bs(requests.get(f'http://afontovo.ru/search/?q={keyword}&spell=1&where=&how=d').text, 'html.parser')
        except: continue
        news = afontovo.find_all('a', {'class': 'article-item__link'}, href=True)
        for element in news:
            title = element.text
            link = 'http://afontovo.ru' + element['href']
            parsed.append((title, link, 'Афонтово'))
# =====Zelenogorsk_END=====
        
# =====Glazov_START=====
def parse_krznamya():
    for keyword in keywords_new:
        try:
            krznamya = bs(requests.get(f'http://kr-znamya.ru/index.php?searchword={keyword}&ordering=&searchphrase=all&Itemid=63&option=com_search').text, 'html.parser')
        except: continue
        news = krznamya.find_all('fieldset')
        for element in news:
            title = element.find('a').text.strip()
            link = 'http//kr-znamya.ru' + element.find('a', href=True)['href']
            parsed.append((title, link, 'Красное знамя'))

def parse_glazovlife():
    for keyword in keywords_new:
        try:
            glazovlife = bs(requests.get(f'http://glazovlife.ru/?s={keyword}').text, 'html.parser')
        except: continue
        news = glazovlife.find_all('h2', {'class': 'entry-title'})
        try:
            for element in news:
                title = element.text.strip()
                link = element.find('a', href=True)['href']
                parsed.append((title, link, 'Glazov Life'))
        except: continue
            
def parse_chmz():
    for keyword in ['%D2%C2%DD%CB', '%F0%EE%F1%E0%F2%EE%EC', '%ED%E0%F3%EA%E0', '%FD%ED%E5%F0%E3%E8%FF','%D4%E8%EB%E8%EC%EE%ED%EE%E2', '%F6%E8%F0%EA%EE%ED%E8%E9', '%F3%F0%E0%ED', '%EA%E0%EB%FC%F6%E8%E9', '%F1%E2%E5%F0%F5%EF%F0%EE%E2%EE%E4%ED%E8%EA%EE%E2%E0%FF+%EF%F0%EE%E4%F3%EA%F6%E8%FF', '%F2%E8%F2%E0%ED', '%C0%ED%E8%F9%F3%EA', '%D0%EE%F1%F1%E8%FF', '%EB%E5%F2%EE', '%EA%E0%F0%ED%E0%E2%E0%EB']: # keywords+zel_glazov in url encode
        try:
            iz = bs(requests.get(f'http://chmz.net/search/index.php?q={keyword}&spell=1&where=&how=d').text, 'html.parser')
        except: continue
        news = iz.find_all('a', {'class': 'searchHead'}, href=True)
        for element in news:
            title = element.text.strip()
            link = 'http://chmz.net' + element['href']
            parsed.append((title, link, 'ЧМЗ'))
            
# =====Glazov_END=====

# =====Novouralsk_START=====

def parse_novouralsknews():
    try:
        novouralsknews = bs(requests.get(f'http://novouralsk-news.ru/').text, 'html.parser')
    except: return 0
    news = novouralsknews.find_all('h4')
    for element in news:
        title = element.find('a').text.strip()
        link = element.find('a', href=True)['href']
        parsed.append((title, link, 'Новости Новоуральска'))
            
def parse_admngo():
    for keyword in keywords_new:
        try:
            admngo = bs(requests.get(f'http://adm-ngo.ru/search/node/{keyword}').text, 'html.parser')
        except: continue
        news = admngo.find_all('h3', {'class': 'title'})
        for element in news:
            try:
                title = element.find('a').text.strip()
                link = element.find('a', href=True)['href']
                parsed.append((title, link, 'Администрация Новоуральского городского округа'))
            except: continue
            
def parse_novouralsktv():
    for keyword in keywords_new:
        try:
            novouralsktv = bs(requests.get(f'http://novouralsk.tv/?s={keyword}').text, 'html.parser')
        except: continue
        news = novouralsktv.find_all('h2', {'class': 'entry-title'})
        for element in news:
            title = element.find('a').text
            link = element.find('a', href=True)['href']
            parsed.append((title, link, 'Новоуральская вещательная компания'))
            
def parse_nugazeta():
    for keyword in keywords_new:
        try:
            nugazeta = bs(requests.get(f'http://nugazeta.ru/component/search/?searchword={keyword}&searchphrase=all').text, 'html.parser')
        except: continue
        news = nugazeta.find_all('dt', {'class': 'result-title'})
        for element in news:
            title = element.find('a').text.strip()
            link = 'http://nugazeta.ru' + element.find('a', href=True)['href']
            parsed.append((title, link, 'Новоуральская газета'))
            
def parse_neyvanews():
    for keyword in keywords_new:
        try:
            neyvanews = bs(requests.get(f'https://neyva-news.ru/component/search/?searchword={keyword}&searchphrase=all').text, 'html.parser')
        except: continue
        news = neyvanews.find_all('dt', {'class': 'result-title'})
        for element in news:
            title = element.find('a').text.strip()
            link = element.find('a', href=True)['href']
            parsed.append((title, link, 'Газета "Нейва"'))

# =====Novouralsk_END=====
"""
# =====Vladimir_START=====
            
def parse_progorod33():
    try:
        progorod33 = bs(requests.get(f'https://progorod33.ru/articles/list').text, 'html.parser')
    except: continue
    news = progorod33.find_all('h3', {'class': 'article-list__item-title'})
    for element in news:
        title = element.find('a').text.strip()
        link = 'http://progorod33.ru' + element.find('a', href=True)['href']
        parsed.append((title, link, 'Портал PROГОРОД'))
            
def parse_tvmig():
    for keyword in keywords_new:
        try:
            tvmig = bs(requests.get(f'https://www.tv-mig.ru/search/?q={keyword}').text, 'html.parser')
        except: continue
        news = tvmig.find_all('div', {'class': 'search-item'})
        for element in news:
            title = element.find('a').text.strip()
            link = 'http://tv-mig.ru' + element.find('a', href=True)['href']
            parsed.append((title, link, 'ТВ МИГ'))
            
def parse_provladimir():
    for keyword in keywords_new:
        try:
            provladimir = bs(requests.get(f'{keyword}').text, 'html.parser')
        except: continue
        news = provladimir.find_all('h2', {'class': 'post-title'})
        for element in news:
            title = element.find('a').text.strip()
            link = element.find('a', href=True)['href']
            parsed.append((title, link, 'ПроВладимир'))
            
def parse_zebratv():
    for keyword in keywords_new:
        try:
            _ = bs(requests.get(f'{keyword}').text, 'html.parser')
        except: continue
        news = _.find()
        for element in news:
            title = element.
            link = element.
            parsed.append((title, link, ''))

def parse_prizyv():
    for keyword in keywords_new:
        try:
            _ = bs(requests.get(f'{keyword}').text, 'html.parser')
        except: continue
        news = _.find()
        for element in news:
            title = element.
            link = element.
            parsed.append((title, link, ''))
            
def parse_6tv():
    for keyword in keywords_new:
        try:
            _ = bs(requests.get(f'{keyword}').text, 'html.parser')
        except: continue
        news = _.find()
        for element in news:
            title = element.
            link = element.
            parsed.append((title, link, ''))
            
def parse_kovrovgorod():
    for keyword in keywords_new:
        try:
            _ = bs(requests.get(f'{keyword}').text, 'html.parser')
        except: continue
        news = _.find()
        for element in news:
            title = element.
            link = element.
            parsed.append((title, link, ''))
            
def parse_nashregion33():
    for keyword in keywords_new:
        try:
            _ = bs(requests.get(f'{keyword}').text, 'html.parser')
        except: continue
        news = _.find()
        for element in news:
            title = element.
            link = element.
            parsed.append((title, link, ''))
            
def parse_vladtv():
    for keyword in keywords_new:
        try:
            _ = bs(requests.get(f'{keyword}').text, 'html.parser')
        except: continue
        news = _.find()
        for element in news:
            title = element.
            link = element.
            parsed.append((title, link, ''))

# =====Vladimir_END=====
"""

"""
def parse_():
    for keyword in []:
        try:
            _ = bs(requests.get(f'{keyword}').text, 'html.parser')
        except: continue
        news = _.find()
        for element in news:
            title = element.
            link = element.
            parsed.append((title, link, ''))
"""

while True:
    print(f'\n[{datetime.now().strftime("%H:%M:%S")}] [INFO] Парсинг начался')
    
    for site in site_names.values():
        print(f'[{datetime.now().strftime("%H:%M:%S")}] [INFO] Парсим {site}')
        eval('parse_'+site)()
    
    print(f'\n[{datetime.now().strftime("%H:%M:%S")}] [INFO] Найдено {len(parsed)} новостей!')
    
    db = sqlite3.connect('parser.db')
    sql = db.cursor()

    for site in site_names.values():
        sql.execute(f'''CREATE TABLE IF NOT EXISTS {site} (title TEXT, link TEXT, source TEXT)''')
        db.commit()

    parsed = list(set(parsed))

    for element in parsed:
        sql.execute(f'''SELECT * FROM {site_names[element[2]]}''')
        old_parsed = sql.fetchall()
        old_parsed_titles = []
        for k in old_parsed:
            old_parsed_titles.append(k[0].lower())
        if element[0].lower() not in old_parsed_titles:
            sql.execute(f'''INSERT INTO {site_names[element[2]]} VALUES (?, ?, ?)''', (element[0], element[1], element[2]))
            db.commit()
            new_news.append(element)

    db.close()
    
    if len(new_news) != 0:
        print(f'\nУникальных новостей: {len(new_news)}')
        
        #ftp_upload()
        #print(f'\n[{datetime.now().strftime("%H:%M:%S")}] [INFO] БД загружена на хостинг!')
        
        random.shuffle(new_news)

        for element in new_news:
            send_parsed_news(element)
    else:
        print('Нет уникальных новостей!')

    parsed, new_news = [], []
    
    print(f'\n[{datetime.now().strftime("%H:%M:%S")}] [INFO] Ждём {int(delay/60)} минут')
    time.sleep(delay)
