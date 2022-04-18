#!/usr/bin/python3.8
# -*- coding: utf-8 -*-
import telebot
from time import gmtime, strftime,localtime
token = '1273658182:AAEY60WZtXQU0mJN90bEVTouZ7nDg1kwXFs'
botik = telebot.TeleBot(token)
@botik.message_handler(content_types=['text'])
def aaa(message):
    t = strftime("%H", localtime())
    if int(t) < 8:
        botik.send_message(message.chat.id,"спать!")
        return
    else:
        try:
            bbb = str(message.text)
            botik.send_message(message.chat.id,bbb + bbb[0])
        except:
            exit()
botik.polling()
