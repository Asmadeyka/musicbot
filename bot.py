#!/usr/bin/python3.8
# -*- coding: utf-8 -*-
import telebot
import time
token = '1273658182:AAEY60WZtXQU0mJN90bEVTouZ7nDg1kwXFs'
botik = telebot.TeleBot(token)
@botik.message_handler(content_types=['text'])
def aaa(message):
    bbb = str(message.text)
    botik.send_message(message.chat.id,bbb + bbb)
botik.polling()
