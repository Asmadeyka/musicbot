#!/usr/bin/python3.8
# -*- coding: utf-8 -*-
import telebot
from transliterate import translit, get_available_language_codes
import urllib.request
import re
import requests
import time
from pytube import YouTube
from bs4 import BeautifulSoup
from telebot import types
import lxml
from lxml import etree
import subprocess
import os
token = '5178606516:AAHJmWCO6oMz_odhaCDmh7t1sxqvgMXeOx0'
botik = telebot.TeleBot(token)
i = 0
buttons = [None] * 10
ssilki = [None] * 10
path = "./downloaded/"    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!  убрать !!!
chatik = ''
answer = ''
nazvanie = ''
downloading = ''
sending = ''

def search(a):
    global i
    global buttons
    global ssilki
    idrequest = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + a).read().decode()
    print("File entered...")
    video_ids = re.findall(r"watch\?v=(\S{11})", idrequest)
    print("Found id-s....")
    for i in range(3):
        x = "https://www.youtube.com/watch?v=" + video_ids[i]
        source = requests.get(x).text
        soup = BeautifulSoup(source, 'lxml')
        links = soup.find_all('link')
        try:
            channel = links[23]
        except:
            botik.send_message(message.chat.id,"sorry(")
        buttons[i] = soup.title.string.replace(" - YouTube","") + ' - ' + channel['content']
        ssilki[i] = x
    print("Names were parsed succesfully ^-^")
    return buttons
    return ssilki

def send(chatik):
    global sending
    global path
    global nazvanie
    sending = botik.send_message(chatik,'Sending mp3 to you....')
    audio_url = "./downloaded/songtosend.mp3"
    botik.send_audio(chatik,audio=open(audio_url,'rb'),title=nazvanie.replace(".mp4",".mp3"))
    botik.delete_message(chatik,sending.message_id)
    print("File sent!")





def download(link):
    global ssilki
    global path
    global nazvanie
    global downloading
    downloading = botik.send_message(chatik,'Downloading....')
    print("Starting to download!!")
    os.chdir(path)  # !!!!!!!!!!!!!!!!!!!!!!!!!11 убрать!!
    selected = YouTube('https://youtube.com/watch?v=' + link)
    track = selected.streams.filter(only_audio= True,file_extension="mp4").first()
    nazvanie = track.default_filename
    track.download(path)
    try:
        os.remove("songtosend.mp4")
        os.remove("songtosend.mp3")
    except:
        pass
    time.sleep(10)
    os.rename(track.default_filename, 'songtosend.mp4')
    vid_path = path + "songtosend.mp4"
    aud_path = path + "songtosend.mp3"
    cmd = "ffmpeg -i {} -vn {}".format(vid_path, aud_path)
    os.system(cmd)
    botik.delete_message(chatik,downloading.message_id)
    print("Download success! Sending...")






@botik.message_handler(commands=['start'])
def process_start(message):
    try:
        botik.send_message(message.chat.id,'Привет,' + message.from_user.username + '!\n' + 'Я помогу тебе скачать музыку из ютуба. Просто отправь мне поисковый запрос и я выдам тебе результаты)')
    except:
        botik.send_message(message.chat.id,'ку')
@botik.message_handler(content_types = ['text'])
def step1(message):
    global chatik
    global answer
    chatik  = message.chat.id
    nenormal = message.text.replace(" ","+")
    try:
        search(nenormal)
    except:
         normal = translit(nenormal, reversed=True)
         search(normal)
    botik.delete_message(message.chat.id,message.message_id)
    menu1 = telebot.types.InlineKeyboardMarkup()
    menu1.add(telebot.types.InlineKeyboardButton(text = str(buttons[0]), callback_data ='first'))
    menu1.add(telebot.types.InlineKeyboardButton(text = str(buttons[1]), callback_data ='second'))
    menu1.add(telebot.types.InlineKeyboardButton(text = str(buttons[2]), callback_data ='third'))
    menu1.add(telebot.types.InlineKeyboardButton(text="X",callback_data='exit'))
    answer = botik.send_message(message.chat.id,"Вот что я нашел, жалкий человечишка!",reply_markup=menu1)
@botik.callback_query_handler(func=lambda call: True)
def step2(call):
    global answer
    global chatik
    if call.data == 'first':
        botik.answer_callback_query(call.id)
        botik.delete_message(chatik, answer.message_id)
        try:
            download(ssilki[0])
            send(chatik)
        except:
            botik.send_message(chatik,'Could not dowwload this shit((')
    elif call.data == 'second':
        botik.answer_callback_query(call.id)
        botik.delete_message(chatik, answer.message_id)
        try:
            download(ssilki[1])
            send(chatik)
        except:
            botik.send_message(chatik,'Could not dowwload this shit((')
    elif call.data == 'third':
        botik.answer_callback_query(call.id)
        botik.delete_message(chatik, answer.message_id)
        try:
            download(ssilki[2])
            send(chatik)
        except:
            botik.send_message(chatik,'Could not dowwload this shit((')
    elif call.data == 'exit':
        botik.answer_callback_query(call.id)
        botik.delete_message(chatik,answer.message_id)
botik.polling()
