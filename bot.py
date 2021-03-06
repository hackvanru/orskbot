#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import random
import datetime

import telebot
import requests
import xmltodict
from pytz import timezone

import config

bot = telebot.TeleBot(config.token)

@bot.message_handler(commands=['w', 'п'])
@bot.message_handler(regexp="^.п$")
@bot.message_handler(regexp="^п$")
def send_weather(message):
    r = requests.get('http://pc.ornpz.ru/meteo/temperature1day.png')
    if r.status_code == 200:
        f = open('out.jpg', 'wb')
        f.write(r.content)
        f.close()

        bot.send_chat_action(message.chat.id, 'upload_photo')
        img = open('out.jpg', 'rb')
        bot.send_photo(message.chat.id, img)
        img.close()
    else:
        bot.send_message(message.chat.id, "Произошла какаято хуйня (URL: http://pc.ornpz.ru/meteo/temperature1day.png)...") 

    # get temperature
    r = requests.get('http://pc.ornpz.ru/meteo/meteo.xml')
    if r.status_code == 200:
        doc = xmltodict.parse(r.text)
            
        for section in doc['points']['point']:
            key = section.get('@name', None)
            # направление ветра
            #if key == 'PointName01':
            #    value = section.get('@value', None)
            #    print 'P:'+value

            # температура
            if key == 'PointName05':       
                value = section.get('@value', None)
                print('T:' + value)
                bot.send_message(message.chat.id,'T: ' + value)
    else:
        bot.send_message(message.chat.id, u"cannot get content of ( URL: http://pc.ornpz.ru/meteo/meteo.xml)... ERROR:" + str(r.status))


@bot.message_handler(commands=['ku', 'ку'])
@bot.message_handler(regexp="^(ку|\.ку|ku|\.ku|re|\.re)$")
def send_ku(message):
    tz = 'Asia/Yekaterinburg'
    fmt = '%Y-%m-%d %H:%M:%S'
    utc = datetime.datetime.utcnow()
    time_str = timezone(tz).fromutc(utc).strftime(fmt)
    bot.send_message(message.chat.id, time_str)


@bot.message_handler(regexp="^(ку|\.ку|ku|\.ku|re|\.re) ([А-Яa-я]*)")
def send_ku_town(message):
    tz = 'Asia/Yekaterinburg'

    if re.search(r'Орск|Orsk', message.text):
        tz = 'Asia/Yekaterinburg'

    if re.search(r'Москва|Moscow|Питер|Piter|СПб', message.text):
        tz = 'Europe/Moscow'

    fmt = '%Y-%m-%d %H:%M:%S'
    utc = datetime.datetime.utcnow()
    time_str = timezone(tz).fromutc(utc).strftime(fmt)
    bot.send_message(message.chat.id, time_str)


@bot.message_handler(commands=['сиськи'])
@bot.message_handler(regexp="^(сиськи|\.сиськи)$")
def send_cucki(message):
    f = open('cucbka.dat')
    links = f.read().split('\n')
    f.close()

    i = random.randint(0, len(links) - 1)
    url = "https://blog.stanis.ru/" + links[i]
    bot.send_message(message.chat.id, url)


bot.polling(none_stop=True)