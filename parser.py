# -*- coding: utf-8 -*-

try:
    from bs4 import BeautifulSoup as bs
    import requests
    import vk_api
except ImportError:
    print('Перед использованием программы установите в окружении необходимые зависимости из файла requirements.txt, используя pip.'); exit()

from datetime import datetime
from ftplib import FTP
import sqlite3
import random
import time    
    
DELAY = 600

new = '\n'

vk_token = '5e0ec624a9904b970aadde6f3d40dc22b83e270b2e7709c457eb5706c9b11a52a111a846086ec2eb1c2d0'
fb_token = ''

vk_session = vk_api.VkApi(token=vk_token)

from vk_api.longpoll import VkLongPoll, VkEventType
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()

vk_posting = vk_api.VkApi(token='7b9f75ed8adabebe1a5ffadd54fb5090d31b9c5ae5bd08e3a2e7589cff42dfb56fddb1b5fbfbe9666143b')
ftp_login = 'xtagfnap_python'
ftp_password = '45xyz625'

user_id_for_bot = 221003515
group_id = -193536475

parsed_news_tvel = []
parsed_news_ria = []
parsed_news_rt = []
parsed_news_bbc = []
parsed_news_vesti = []
parsed_news_iz = []
parsed_news_komm = []
parsed_news_rbk = []
parsed_news_rosatom = []

link_ria = 'http://ria.ru/search/?query='
link_iz = 'http://iz.ru/search?text='
link_bbc = 'https://www.bbc.com/russian/search?q='
link_rt = 'http://russian.rt.com/search?q='
link_rosatom = 'http://rosatom.ru/journalist/news/search/?q='
link_tvel = 'http://tvel.ru/search/index.php?q='
link_vesti = 'http://vesti.ru/search?q='
link_rbk = 'https://www.rbc.ru/search/?project=rbcnews&query='

keywords = ['ядерный', 'атомный', 'твэл', 'росатом', 'атомная станция', 'атомное топливо', 'нейтрино', 'атомный реактор', 'атомный ледокол', 'атомная энергетика', 'ядерная установка', 'ядерные исследования', 'атомные источники тока', 'термоядерный синтез', 'вниинм', 'чмз', 'чепецкий механический завод', 'аэхк', 'ангарский электролизный химический комбинат', 'энергетика']

new_news = [] # [ ('header', 'link', 'source'), (...) ]

def posting(post):
    vk_posting.method('wall.post', {'owner_id': group_id, 'from_group': 1, 'message': f'{post[0]}. Источник: {post[-1]}. Подробнее: {post[1]}. '})

def send(message):
    vk.messages.send(user_id=user_id_for_bot, random_id=random.randint(-999999999999, 999999999999), message=message)
    
def send_with_keyboard(message):
    vk.messages.send(user_id=user_id_for_bot, random_id=random.randint(-999999999999, 999999999999), message=message, keyboard=open('keyboard.json').read())

def parse_ria():
    global parsed_news_ria; parsed_news_ria = []
    for keyword in keywords:
        try:
            ria = bs(requests.get(link_ria + keyword).text, 'html.parser')
        except: continue
        news = ria.find_all('div', {'class': 'list-item'})
        for elem in range(len(news)):
            title = news[elem].find_all('span')[-1].attrs['data-title']
            link = news[elem].find_all('span')[-1].attrs['data-url']
            parsed_news_ria.append((title, link, 'РИА'))
            z = []
            rep = []
            for k in parsed_news_ria:
                if k[0] not in rep:
                    z.append(k)
                    rep.append(k[0])
            parsed_news_ria = z
            del(z, rep)
    print(f'Найдено {len(parsed_news_ria)} новостей!')

def parse_iz():
    global parsed_news_iz; parsed_news_iz = []
    for keyword in keywords:
        try:
            iz = bs(requests.get(link_iz + keyword).text, 'html.parser')
        except: continue
        news = iz.find_all('div', {'class': 'view-search'})
        for elem in range(len(news)):
            title = news[elem].find_all('a')[0].text
            link = news[elem].find_all('a')[0]['href']
            parsed_news_iz.append((title, link, 'Известия'))
            z = []
            rep = []
            for k in parsed_news_iz:
                if k[0] not in rep:
                    z.append(k)
                    rep.append(k[0])
            parsed_news_iz = z
            del(z, rep)
    print(f'Найдено {len(parsed_news_iz)} новостей!')

def parse_bbc():
    global parsed_news_bbc; parsed_news_bbc = []
    for keyword in keywords:
        try:
            bbc = bs(requests.get(link_bbc + keyword).text, 'html.parser')
        except: continue
        news = bbc.find_all('div', {'class': 'hard-news-unit'})
        for elem in range(len(news)):
            title = news[elem].find('a').text
            link = news[elem].find('a', href=True)['href']
            parsed_news_bbc.append((title, link, 'BBC'))
            z = []
            rep = []
            for k in parsed_news_bbc:
                if k[0] not in rep:
                    z.append(k)
                    rep.append(k[0])
            parsed_news_bbc = z
            del(z, rep)
    print(f'Найдено {len(parsed_news_bbc)} новостей!')

def parse_rt():
    global parsed_news_rt; parsed_news_rt = []
    for keyword in keywords:
        try:
            rt = bs(requests.get(link_rt + keyword).text, 'html.parser') 
        except: continue
        news = rt.find_all('li', {'class': 'listing__column'})
        for elem in range(len(news)):
            title = news[elem].find('a', {'class': 'link'}).text.strip()
            link = 'http://russian.rt.com' + news[elem].find('a', {'class': 'link'}, href=True)['href']
            parsed_news_rt.append((title, link, 'RT'))
            z = []
            rep = []
            for k in parsed_news_rt:
                if k[0] not in rep:
                    z.append(k)
                    rep.append(k[0])
            parsed_news_rt = z
            del(z, rep)
    print(f'Найдено {len(parsed_news_rt)} новостей!')

def parse_rosatom():
    global parsed_news_rosatom; parsed_news_rosatom = []
    for keyword in keywords:
        try:
            rosatom = bs(requests.get(link_rosatom + keyword).text, 'html.parser')
        except: continue
        news = rosatom.find_all('div', {'class': 'cardsBlockGrey'})
        for elem in range(len(news)):
            title = news[elem].find_all('span')[-1].text
            link = 'http://rosatom.ru' + news[elem].find('a', href=True)['href']
            parsed_news_rosatom.append((title, link, 'Росатом'))
            z = []
            rep = []
            for k in parsed_news_rosatom:
                if k[0] not in rep:
                    z.append(k)
                    rep.append(k[0])
            parsed_news_rosatom = z
            del(z, rep)
    print(f'Найдено {len(parsed_news_rosatom)} новостей!')

def parse_tvel():
    global parsed_news_tvel; parsed_news_tvel = []
    for keyword in keywords:
        try:
            tvel = bs(requests.get(link_tvel + keyword).text, 'html.parser')
        except: continue
        news = tvel.find_all('div', {'class': 'search-list-title'})
        for elem in range(len(news)):
            title = news[elem].text.strip(new)
            link = 'http://tvel.ru' + news[elem].find('a', href=True)['href']
            parsed_news_tvel.append((title, link, 'ТВЭЛ'))
            z = []
            rep = []
            for k in parsed_news_tvel:
                if k[0] not in rep:
                    z.append(k)
                    rep.append(k[0])
            parsed_news_tvel = z
            del(z, rep)
    print(f'Найдено {len(parsed_news_tvel)} новостей!')

def parse_vesti():
    global parsed_news_vesti; parsed_news_vesti = []
    for keyword in keywords:
        try:
            vesti = bs(requests.get(link_vesti + keyword).text, 'html.parser')
        except: continue
        news = vesti.find_all('div', {'class': 'search-item'})
        for elem in range(len(news)):
            title = news[elem].find('a').text
            if title == '':
                continue
            link = 'http://vesti.ru' + news[elem].find('a', href=True)['href']
            parsed_news_vesti.append((title, link, 'Вести'))
            z = []
            rep = []
            for k in parsed_news_vesti:
                if k[0] not in rep:
                    z.append(k)
                    rep.append(k[0])
            parsed_news_vesti = z
            del(z, rep)
    print(f'Найдено {len(parsed_news_vesti)} новостей!')

def parse_rbk():
    global parsed_news_rbk; parsed_news_rbk = []
    for keyword in keywords:
        try:
            rbk = bs(requests.get(link_rbk + keyword).text, 'html.parser')
        except: continue
        news = rbk.find_all('div', {'class': 'search-item'})
        for elem in range(len(news)):
            title = news[elem].find('span', {'class': 'search-item__title'}).text
            link = news[elem].find('a', href=True)['href']
            parsed_news_rbk.append((title, link, 'РБК'))
            z = []
            rep = []
            for k in parsed_news_rbk:
                if k[0] not in rep:
                    z.append(k)
                    rep.append(k[0])
            parsed_news_rbk = z
            del(z, rep)
    print(f'Найдено {len(parsed_news_rbk)} новостей!')
            
def parse_komm():
    global parsed_news_komm; parsed_news_komm = []
    date_today = datetime.now().strftime('%d.%m.%Y')
    for keyword in keywords:
        try:
            komm = bs(requests.get(f'https://www.kommersant.ru/search/results?places=&categories=&isbankrupt=&datestart={date_today}&dateend={date_today}&sort_type=0&sort_dir=&regions=&results_count=&page=1&search_query=ядерная&sort_by=0&search_full=1&time_range=2&dateStart={date_today}&dateEnd={date_today}'+keyword).text, 'html.parser')
        except: continue
        news = komm.find_all('div', {'class': 'search_results_item'})
        for elem in range(len(news)):
            title = news[elem].find_all('a')[-2].text
            if 'Главные новости к' in title:
                continue
            link = news[elem].find_all('a', href=True)[-1]['href']
            parsed_news_komm.append((title, link, 'Коммерсант'))
            z = []
            rep = []
            for k in parsed_news_komm:
                if k[0] not in rep:
                    z.append(k)
                    rep.append(k[0])
            parsed_news_komm = z
            del(z, rep)
    print(f'Найдено {len(parsed_news_komm)} новостей!')
            
def bot(post):
    try:
        reacted = 0
        send_with_keyboard(f'Через 15 минут будет опубликована следующая новость: {post[0]}. Ссылка: {post[1]}. Источник: {post[-1]}. Проигнорируйте это сообщение, и новость будет опубликована автоматически, или воспользуйтесь функционалом бота при помощи кнопок ниже')
        time_when_started = datetime.now().time().strftime('%M')
        while int(datetime.now().time().strftime('%M')) != int(time_when_started) + 15 % 60:
            for event in longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
                    if event.text:
                        if event.from_user:
                            if event.text == 'Не опубликовывать':
                                reacted = 1
                                send('Запись не будет опубликована!')
                                return 0
                            if event.text == 'Опубликовать сейчас':
                                reacted = 1
                                try:
                                    posting(post) # posting VK
                                    send('Запись опубликована в VK!')
                                except:
                                    send('[ОШИБКА]: в VK запись не была опубликована. Работа программы продолжается.')
                                try:
                                    reacted = 0/0 # posting FB
                                    send('Запись опубликована в FB!')
                                except:
                                    send('FB временно не работает. Мы уже работаем над этим.')
                                return 0
        if reacted == 0:
            try:
                posting(post) # posting VK
                send('Запись опубликована в вк!')
            except:
                send('[ОШИБКА]: в VK запись не была опубликована. Работа программы продолжается.')
            try:
                reacted = 0/0 # posting FB
                send('Запись опубликована в FB!')
            except:
                send('FB временно не работает. Мы уже работаем над этим.')
            return 0        
        else:
            return 0
    except:
        send('Превышено время ожидания ответа. Отправляем новое сообщение.')
        bot(post)
    
while True:    
    db = sqlite3.connect('parser.db')
    sql = db.cursor()
    
    sql.execute('CREATE TABLE IF NOT EXISTS ria (title TEXT, link TEXT, source TEXT)')
    db.commit()
    sql.execute('CREATE TABLE IF NOT EXISTS iz (title TEXT, link TEXT, source TEXT)')
    db.commit()
    sql.execute('CREATE TABLE IF NOT EXISTS bbc (title TEXT, link TEXT, source TEXT)')
    db.commit()
    sql.execute('CREATE TABLE IF NOT EXISTS rt (title TEXT, link TEXT, source TEXT)')
    db.commit()
    sql.execute('CREATE TABLE IF NOT EXISTS tvel (title TEXT, link TEXT, source TEXT)')
    db.commit()
    sql.execute('CREATE TABLE IF NOT EXISTS vesti (title TEXT, link TEXT, source TEXT)')
    db.commit()
    sql.execute('CREATE TABLE IF NOT EXISTS rosatom (title TEXT, link TEXT, source TEXT)')
    db.commit()
    sql.execute('CREATE TABLE IF NOT EXISTS rbk (title TEXT, link TEXT, source TEXT)')
    db.commit()
    sql.execute('CREATE TABLE IF NOT EXISTS komm (title TEXT, link TEXT, source TEXT)')
    db.commit()
    
    print('Парсим риа')
    parse_ria()
    print('Парсим известия')
    parse_iz()
    print('Парсим bbc')
    parse_bbc()
    print('Парсим рт')
    parse_rt()
    #print('Парсим твэл')
    #parse_tvel()
    print('Парсим вести')
    parse_vesti()
    #print('Парсим росатом')
    #parse_rosatom()
    print('Парсим РБК')
    parse_rbk()
    print('Парсим КоммерсантЪ')
    parse_komm()
    
    if len(parsed_news_ria) != 0:
        print('Проверяем новые РИА...')
        for k in range(len(parsed_news_ria)):
            sql.execute('SELECT * FROM ria')
            all_ria = sql.fetchall()
            if parsed_news_ria[k] not in all_ria:
                new_news.append(parsed_news_ria[k])
                sql.execute('INSERT INTO ria VALUES (?, ?, ?)', (parsed_news_ria[k][0], parsed_news_ria[k][1], parsed_news_ria[k][-1]))
                db.commit()
    else:
        print('Новостей нет!')
                    
    if len(parsed_news_iz) != 0:
        print('Проверяем новые ИЗВЕСТИЯ...')
        for k in range(len(parsed_news_iz)):
            sql.execute('SELECT * FROM iz')
            all_iz = sql.fetchall()
            if parsed_news_iz[k] not in all_iz:
                new_news.append(parsed_news_iz[k])
                sql.execute('INSERT INTO iz VALUES (?, ?, ?)', (parsed_news_iz[k][0], parsed_news_iz[k][1], parsed_news_iz[k][-1]))
                db.commit()
    else:
        print('Новостей нет!')
                      
    if len(parsed_news_bbc) != 0:
        print('Проверяем новые BBC...')
        for k in range(len(parsed_news_bbc)):
            if parsed_news_bbc[k][0][0:5] == 'Видео':
                continue
            sql.execute('SELECT * FROM bbc')
            all_bbc = sql.fetchall()
            if parsed_news_bbc[k] not in all_bbc:
                new_news.append(parsed_news_bbc[k])
                sql.execute('INSERT INTO bbc VALUES (?, ?, ?)', (parsed_news_bbc[k][0], parsed_news_bbc[k][1], parsed_news_bbc[k][-1]))
                db.commit()
    else:
        print('Новостей нет!')
       
    if len(parsed_news_rt) != 0:
        print('Проверяем новые RT...')    
        for k in range(len(parsed_news_rt)):
            sql.execute('SELECT * FROM rt')
            all_rt = sql.fetchall()
            if parsed_news_rt[k] not in all_rt:
                new_news.append(parsed_news_rt[k])
                sql.execute('INSERT INTO rt VALUES (?, ?, ?)', (parsed_news_rt[k][0], parsed_news_rt[k][1], parsed_news_rt[k][-1]))
                db.commit()
    else:
        print('Новостей нет!')
    
    #if len(parsed_news_rosatom) != 0:
        #print('Проверяем новые ROSATOM...')        
        #for k in range(len(parsed_news_rosatom)):
            #sql.execute('SELECT * FROM rosatom')
            #all_rosatom = sql.fetchall()
            #if parsed_news_rosatom[k] not in all_rosatom:
                #new_news.append(parsed_news_rosatom[k])
                #sql.execute('INSERT INTO rosatom VALUES (?, ?, ?)', (parsed_news_rosatom[k][0], parsed_news_rosatom[k][1], parsed_news_rosatom[k][-1]))
                #db.commit()
    #else:
        #print('Новостей нет!')
        
    if len(parsed_news_tvel) != 0:
        print('Проверяем новые ТВЭЛ...')
        z = []
        rep = []
        for k in parsed_news_tvel:
            if k[0] not in rep:
                z.append(k)
                rep.append(k[0])
        parsed_news_tvel = z
        del(z, rep)
                
        for k in range(len(parsed_news_tvel)):
            if parsed_news_tvel[k][0][0:7] == 'История':
                continue
            sql.execute('SELECT title FROM tvel')
            titles_tvel = sql.fetchall()
            if parsed_news_tvel[k][0] not in titles_tvel:
                new_news.append(parsed_news_tvel[k])
                sql.execute('INSERT INTO tvel VALUES (?, ?, ?)', (parsed_news_tvel[k][0], parsed_news_tvel[k][1], parsed_news_tvel[k][-1]))
                db.commit()
    else:
        print('Новостей нет!')
    
    if len(parsed_news_tvel) != 0:
        dump = open(f'tvel_news_{datetime.now().time().strftime("%Y%m%d_%H%M%S")}.txt', 'w')
        dump.write(str(parsed_news_tvel))
        dump.close()
        
    if len(parsed_news_vesti) != 0:
        print('Проверяем новые ВЕСТИ...')
        for k in range(len(parsed_news_vesti)):
            sql.execute('SELECT * FROM vesti')
            all_vesti = sql.fetchall()
            if parsed_news_vesti[k] not in all_vesti:
                new_news.append(parsed_news_vesti[k])
                sql.execute('INSERT INTO vesti VALUES (?, ?, ?)', (parsed_news_vesti[k][0], parsed_news_vesti[k][1], parsed_news_vesti[k][-1]))
                db.commit()
    else:
        print('Новостей нет!')
        
    if len(parsed_news_rbk) != 0:
        print('Проверяем новые РБК...')
        for k in range(len(parsed_news_rbk)):
            sql.execute('SELECT * FROM rbk')
            all_rbk = sql.fetchall()
            if parsed_news_rbk[k] not in all_rbk:
                new_news.append(parsed_news_rbk[k])
                sql.execute('INSERT INTO rbk VALUES (?, ?, ?)', (parsed_news_rbk[k][0], parsed_news_rbk[k][1], parsed_news_rbk[k][-1]))
                db.commit()
    else:
        print('Новостей нет!')
        
    if len(parsed_news_komm) != 0:
        print('Проверяем новые Коммерсант...')
        for k in range(len(parsed_news_komm)):
            sql.execute('SELECT * FROM komm')
            all_komm = sql.fetchall()
            if parsed_news_komm[k] not in all_komm:
                new_news.append(parsed_news_komm[k])
                sql.execute('INSERT INTO komm VALUES (?, ?, ?)', (parsed_news_komm[k][0], parsed_news_komm[k][1], parsed_news_komm[k][-1]))
                db.commit()
    else:
        print('Новостей нет!')
    
    print(f'Количество новых новостей: {len(new_news)}')
    
    if len(new_news) != 0:
        news_dump = open(f'parsed_news_{datetime.now().time().strftime("%Y%m%d_%H%M%S")}.txt', 'w', encoding='utf-8')
        news_dump.write(str(new_news))
        news_dump.close()
        
    random.shuffle(new_news)
    
    for new in new_news:
        bot(new)
        
    db.close()
    
    ftp = FTP('xtagfnap.beget.tech')
    ftp.login(ftp_login, ftp_password)
    ftp.delete('parser.db')
    f = open('parser.db', 'rb')
    ftp.storbinary('STOR ' + 'parser.db', f)
    f.close()
    ftp.close()
    
    parsed_news_ria, parsed_news_iz, parsed_news_bbc, parsed_news_rt, parsed_news_rosatom, parsed_news_tvel, parsed_news_vesti, new_news = [], [], [], [], [], [], [], []
    print(f'Ждем {DELAY} секунд начиная с {datetime.now().time().strftime("%H:%M:%S")}')
    time.sleep(DELAY)
