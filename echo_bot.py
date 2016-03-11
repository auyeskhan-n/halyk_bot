# -*- coding: utf-8 -*-
import telebot
import os
import mysql.connector
import math
import urllib.request
from bs4 import BeautifulSoup
from telebot import types

bot = telebot.TeleBot("")

text_messages = {
    'start':
        u'Добро пожаловать!\n\n'
        u'Я неофициальный бот от Халык Банка. \n'
        u'Наберите команду /help для того чтобы увидеть список доступных команд.',

    'about':
        u'АО «Народный банк Казахстана» — крупнейший универсальный коммерческий банк Республики Казахстан, '
        u'успешно работающий на благо своих клиентов уже более 90 лет, одна из самых надежных и диверсифицированных '
        u'финансовых структур Казахстана.\n\n'
        u'Юридический адрес: \n050008, г.Алматы, пр. Абая 109 В\n\n'
        u'Контакт-центр: \nтелефон: (727) 259-07-77 \nпо Казахстану бесплатный: 8 8000 8000 59\n\n'
        u'Факс-сервер: (727) 259-02-71 \nТелетайп: 251866 KPOKET\nТелекс: 251531 HSBK KZ\nКод SWIFT: HSBKKZKX\nКод Reuters: Dealing SVKZ\nE-mail: halykbank@halykbank.kz ',

    'otdeleniya':
    	u'— Алматинский Областной Филиал №139900: \n'
    	u'	г. Алматы, ул. Розыбакиева, 101\n\n'
    	u'— Расчётно-кассовое отделение 131506\n'
    	u'	г. Алматы, пл. Республики, 4\n\n'
    	u'— Расчётно-кассовое отделение 131499\n'
    	u'	г. Алматы, мкр. Аксай-4, д.100\n\n'
    	u'— Расчётно-кассовое отделение 131403\n'
    	u'	г. Алматы, пр. Райымбека, 383\n\n'
    	u'— Расчётно-кассовое отделение 131405\n'
    	u'	г. Алматы, мкр.4, д.10а',
    'bankomaty':
    	u'— Банкомат 13268: \n'
    	u'	пр. Жибек Жолы 54\n\n'
    	u'— Банкомат 00013008: \n'
    	u'	г. Алматы, мкр. 4, 10А (пр. Абая, уг. пр. Алтынсарина)\n\n'
    	u'— Банкомат 00013001: \n'
    	u'	г. Алматы, ул. Папанина, 220, уг. ул. Свердлова\n\n'
    	u'— Банкомат 00013002: \n'
    	u'	г. Алматы, ул. Панфилова, уг.ул. Карасай батыра\n\n'
    	u'— Банкомат 00013003: \n'
    	u'	г. Алматы, пр. Абая, 109В, уг. ул. Ауэзова, ТЦ "Глобус", 09:00 - 01:00',
    'block':
    	u'В случае утери или кражи карточки, необходимо осуществить следующие действия: \n'
    	u'Необходимо срочно заблокировать карточку, позвонив в  Контакт центр, либо отправить сообщение в формате '
    	u'"ИИН, последние 4 цифры карточки".',
    'bonus':
    	u'📍 Halyk Bank Bonus Club 📍\n\n'
    	u'Экономьте до 20% при оплате карточками Халык Банка '
    	u'в магазинах, кафе и ресторанах, аптеках, заправках и во многих других часто '
    	u'посещаемых Вами заведениях, входящих в список партнеров бонусного клуба «HALYK».\n\n'
    	u'1 бонус = 1 тенге!\n\n'
    	u'Как получать и тратить бонусы? \n Подробнее по ссылке: \nhttp://www.halykbank.kz/ru/bonus-club/about-club'
}

commands = {
			'start': 'Начать работу с ботом',
            'help': 'Показать существующие команды',
            'about': 'Информация о Народном Банке.',
            'menu': 'Вызвать меню.'
}

emergency = {
			'101': 'Пожарная служба',
			'102': 'Полиция',
			'103': 'Скорая помощь',
			'112': 'Служба спасения'
}

deposits = {
	'Стандартный': 	u'Самый простой и надежный способ вложения свободных денег.\n\n'
					u'1. Срок вклада составляет 1,3,6,9,12,18,24,30,36 месяцев.\n'
					u'2. Капитализация: ежемесячно.\n'
					u'3. Выплата вознаграждения по вкладу осуществляется по окончании срока вклада. \n'
					u'4. Возможность пополнения вклада не предусмотрена.\n'
					u'5. Возможность частичного изъятия вклада не предусмотрена.\n'
					u'6. Минимальный размер вклада: 15 000 тенге, или 100 долларов США или 100 евро.\n'
					u'7. Ставка вознаграждения остается неизменной в течение срока вклада, если иное не будет установлено договором Банковского вклада, либо дополнительным соглашением к Договору.',
	'Пенсионный': 	u'Вклад для пенсионеров и лиц предпенсионного возраста.\n\n'
					u'1. Особые условия: вкладчиками могут выступить физические лица в возрасте старше 50 лет, либо лица в возрасте до 50 лет, предъявившие пенсионные удостоверения.\n'
					u'2. Срок вклада составляет 6 и 12 месяцев.\n'
					u'3. Ставка вознаграждения по вкладу остается неизменной в течение срока вклада.\n'
					u'4. Капитализация вознаграждения: в конце срока вклада. По желанию клиента вознаграждение может выплачиваться ежемесячно на текущий или карточный счет.\n'
					u'5. Возможность пополнения вклада: допускается при условии минимального размера дополнительного взноса – 500 тенге, или 5 долларов США, или 5 евро.\n'
					u'6. Возможность частичного изъятия вклада не предусмотрена.\n'
					u'7. Минимальный размер вклада: 2 000 тенге, или 20 долларов США, или 20 евро.',
	'Универсальный':u'Удобный способ управления сбережениями.  \n\n'
					u'1. Срок вклада составляет 9, 12, 36 месяцев.\n'
					u'2. Капитализация: ежемесячно.\n'
					u'3. Выплата вознаграждения: по окончании срока вклада.\n'
					u'4. Возможность пополнения вклада: допускается при условии минимального размера дополнительного взноса – 7 000 тенге, или 50 долларов США, или 50 евро.\n'
					u'5. Возможность частичного изъятия вклада: допускается при условии сохранения на сберегательном счете неснижаемого остатка в размере 75 000 тенге, или 500 долларов США, или 500 евро.\n'
					u'6. Ставка вознаграждения остается неизменной в течение срока вклада, если иное не будет установлено договором банковского вклада, либо дополнительным соглашением к Договору.\n'
					u'7. Дополнительно: возможность пополнения вклада путем осуществления перевода со своих текущих счетов без посещения Банка через Интернет банкин',
}
### currency parser ###################################################################################
def get_html(url):
	response = urllib.request.urlopen(url)
	return response.read()

def parse_currency(html):
    soup = BeautifulSoup(html, "html5lib") 
    table = soup.find('table',class_='rates-1 js-rates-1') 
    currency = [] 
    for row in table.find_all('tr')[1:]: 
        cols = row.find_all('td') 
        img= cols[2].img 
        currency.append({'currency': cols[0].text,'buy': cols[1].text.strip(),'sold':cols[2].text.strip()})           
    return currency

def parse_kotirovka(html):
    soup = BeautifulSoup(html, "html5lib") 
    table = soup.find_all('div',class_='indicators_vert__group') 
    data = [] 
    for row in table[1].find_all('a'): 
        cols = row.find_all('span')
        data.append({ 'data': cols[0].text.strip(),'value': cols[2].text.strip()})             
    return data

kot = parse_kotirovka(get_html('http://rbc.ru/'))
cur = parse_currency(get_html('http://halykbank.kz/'))
########################################################################################################
###################################location#############################################################
def find_longlat(message,location):
    lat = location.latitude
    long = location.longitude
    findNear(message,lat,long)    
def distFrom(lat1,long1,lat2,long2):
    earthRadius=6371.0
    dLat= math.radians(lat2-lat1)
    dLng= math.radians(long2-long1)
    sindLat = math.sin(dLat/2)
    sindLng = math.sin(dLng/2)

    a = math.pow(sindLat,2) +math.pow(sindLng,2) *math.cos(math.radians(lat1))*math.cos(math.radians(lat2))
    c = 2*math.atan2(math.sqrt(a),math.sqrt(1-a))
    dist = earthRadius*c

    return dist
def findNear(message,lat,long): 
    db = mysql.connector.connect(host="localhost",user="root",passwd="",db="telebot")  
    cur = db.cursor()
    cur.execute("SELECT * FROM bank_loc")
    rows = cur.fetchall()
    min_distance = 25
    temp = 0
    min_bank = -1
    for eachrow in rows:
        temp = distFrom(lat,long,eachrow[5],eachrow[4])
        if(temp<min_distance):
            min_distance=temp
            min_bank=eachrow[0]
    temp = distFrom(lat,long,rows[min_bank][5],rows[min_bank][4])
    bot.send_location(message.chat.id,rows[min_bank][5],rows[min_bank][4])
    db.close()
########################################################################################################
# => start
@bot.message_handler(commands=['start'])
def send_welcome(message):
	cid = message.chat.id 
	bot.send_message(cid, "Здравстуйте Ruslan! Это неофициальный бот от Халык Банк!")
	markup = types.ReplyKeyboardMarkup()
	markup.add('🏢 Отделения', '🏧 Банкоматы')
	markup.add('💱 Валюта', 'Котировки')
	markup.add('Дополнительно', 'О банке')
	bot.send_message(cid, 'Выберите операцию: ', reply_markup = markup)

# => menu
@bot.message_handler(func=lambda msg: msg.text == 'Меню')
def send_mmenu(message):
	cid = message.chat.id 
	markup = types.ReplyKeyboardMarkup()
	markup.add('🏢 Отделения', '🏧 Банкоматы')
	markup.add('💱 Валюта', 'Котировки')
	markup.add('Дополнительно', 'О банке')
	bot.send_message(cid, 'Выберите операцию: ', reply_markup = markup)

# => about 
@bot.message_handler(commands=['about'])
@bot.message_handler(func=lambda msg: msg.text == 'О банке')
def send_about(message):
	cid = message.chat.id
	bot.send_message(cid, text_messages['about'])

# => help
@bot.message_handler(commands=['help'])
@bot.message_handler(func=lambda msg: msg.text == 'Список команд')
def command_help(message):
    cid = message.chat.id
    help_text = "Доступны следующие команды: \n"
    for key in commands:  
        help_text += "/" + key + ": "
        help_text += commands[key] + "\n"
    bot.send_message(cid, help_text)  

# => отделения
@bot.message_handler(func=lambda msg: msg.text == '🏢 Отделения')
def send_otdeleniya(message):
	cid = message.chat.id 
	markup = types.ReplyKeyboardMarkup()
	markup.add('🏢 Список отделении', 'Найти ближайшее отделение')
	bot.send_message(cid, 'Выберите операцию: ', reply_markup = markup)

# => список отдел
@bot.message_handler(func=lambda msg: msg.text == '🏢 Список отделении')
def send_bankomaty(message):
	cid = message.chat.id 
	bot.send_message(cid, text_messages['otdeleniya'])

# => nearest 
@bot.message_handler(func=lambda msg: msg.text == 'Найти ближайшее отделение')
def send_bankomaty(message):
	cid = message.chat.id 
	bot.send_message(cid, "Отправьте ваше местоположение чтобы найти ближайшее отделение.")

# => location handler
@bot.message_handler(content_types=['location'])
def send_location(message):
	find_longlat(message,message.location)

# => банкоматы 
@bot.message_handler(func=lambda msg: msg.text == '🏧 Банкоматы')
def send_bankomaty(message):
	cid = message.chat.id 
	bot.send_message(cid, text_messages['bankomaty'])

# => валюта
@bot.message_handler(func=lambda msg: msg.text == '💱 Валюта')
def send_currency(message):
	cid = message.chat.id 
	cur_text = "Курсы валют: \nПокупка: \n"
	for i in range (len(cur)):
	    cur_text += "1 " + cur[i]['currency'] + ": "
	    cur_text += cur[i]['buy'] + " KZT \n"
	cur_text += "\nПродажа: \n"
	for i in range (len(cur)):
	    cur_text += "1 " + cur[i]['currency'] + ": "
	    cur_text += cur[i]['sold'] + " KZT \n"
	bot.send_message(cid, cur_text)

# => котировки
@bot.message_handler(func=lambda msg: msg.text == 'Котировки')
def send_kotirovki(message):
	cid = message.chat.id 
	kotirovki = ""
	for i in range(len(kot)):
		kotirovki += kot[i]['data'] + ": "
		kotirovki += kot[i]['value'] + "\n"
	bot.send_message(cid, kotirovki)

# => moreMore
@bot.message_handler(func=lambda msg: msg.text == 'Дополнительно')
def more(message):
	cid = message.chat.id 
	markup = types.ReplyKeyboardMarkup(row_width=2)
	markup.add('🆘', '🎁 Бонусный клуб')
	markup.add('Разное', 'Услуги')
	markup.add('Меню')
	bot.send_message(cid, 'Выберите операцию: ', reply_markup = markup)

# => СОС
@bot.message_handler(func=lambda msg: msg.text == '🆘')
def more(message):
	cid = message.chat.id 
	markup = types.ReplyKeyboardMarkup(row_width=2)
	markup.add('Список экстренных служб', 'Блокировка карточки', 'Меню')
	bot.send_message(cid, 'Выберите операцию: ', reply_markup = markup)

# => emergency
@bot.message_handler(func=lambda msg: msg.text == 'Список экстренных служб')
def send_emergency(message):
	cid = message.chat.id
	t = ""
	for i in emergency:
		t += i + ": "
		t += emergency[i] + "\n"
	bot.send_message(cid, t)

# => card block
@bot.message_handler(func=lambda msg: msg.text == 'Блокировка карточки')
def send_block(message):
	cid = message.chat.id 
	bot.send_message(cid, text_messages['block'])

# => card check
@bot.message_handler(regexp = "[x]\d{4}")
def send_block(message):
	cid = message.chat.id 
	bot.send_message(cid, "Blocked!")

# => bonus
@bot.message_handler(func=lambda msg: msg.text == '🎁 Бонусный клуб')
def send_bonus(message):
	cid = message.chat.id
	bot.send_message(cid, text_messages['bonus'])
	photo = open('bonus.jpg', 'rb') 
	bot.send_photo(cid, photo)

# => uslugi
@bot.message_handler(func=lambda msg: msg.text == 'Услуги')
def send_uslugi(message):
	cid = message.chat.id
	markup = types.ReplyKeyboardMarkup(row_width=2)
	markup.add('Частным клиентам', 'Корп. клиентам', 'Меню')
	bot.send_message(cid, 'Выберите услугу: ', reply_markup = markup)

# => chastnim
@bot.message_handler(func=lambda msg: msg.text == 'Частным клиентам')
def send_uslugi(message):
	cid = message.chat.id
	markup = types.ReplyKeyboardMarkup(row_width=2)
	markup.add('Депозиты', 'Кредиты', 'Платежные карточки', 'Мобильный банкинг', 'Меню')
	bot.send_message(cid, 'Выберите услугу: ', reply_markup = markup)

# => deposit
@bot.message_handler(func=lambda msg: msg.text == 'Депозиты')
def send_deposit(message):
	cid = message.chat.id
	t = ""
	for i in deposits:
		t += i + ": "
		t += deposits[i] + "\n"
	bot.send_message(cid, t)
	
# => корпоратив
@bot.message_handler(func=lambda msg: msg.text == 'Корп. клиентам')
def send_uslugi(message):
	cid = message.chat.id
	markup = types.ReplyKeyboardMarkup(row_width=2)
	markup.add('Продукты и услуги казначейства', 'Расчётно-кассовое обслуживание', 'Кредитование', 'Мобильный банкинг', 'Меню')
	bot.send_message(cid, 'Выберите услугу: ', reply_markup = markup)
bot.polling()
