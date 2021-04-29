import telebot
import lyricsgenius
from requests import get
import json
from flask import Flask, request
import os

TOKEN = '1761980685:AAGORkIW_RKibK_gU3ntnbP-0b-cvji90hU'
genius = lyricsgenius.Genius("<genius-token>")
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def info(message):
    text = (
        "Используй /lyrics <название песни>, чтобы найти текст данной песни.\n"
        "Используй /findsong <строчка из песни>, чтобы найти название песни.\n"
    )
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['lyrics'])
def send_lyrics(message):
    try:
        bot.send_message(message.chat.id, "В поисках нужного текста, подожди чуть-чуть :)")
        song_name = message.text
        song_name = telebot.util.extract_arguments(song_name)
        lyric = genius.search_song(song_name, get_full_info=True)
        lyric = lyric.lyrics
        index = 0
        while lyric[index] != '\n':
            index += 1
        index1 = index + 1
        while lyric[index1] != '\n':
            index1 += 1
        line = lyric[index + 1:index1]
        bot.send_message(message.chat.id, lyric)
        song_names = genius.search_lyrics(line)
        song_images = []
        for hits in song_names['sections'][0]['hits']:
            song_images.append(hits['result']['header_image_url'])
        url = song_images[0]
        print(song_names)
        bot.send_photo(message.chat.id, get(url).content)
    except:
        bot.send_message(message.chat.id, "Что-то пошло не так, попробуй снова :(")


@bot.message_handler(commands=['findsong'])
def send_songname(message):
    bot.send_message(message.chat.id, "В поисках нужной песни, подожди чуть-чуть :)")
    try:
        lyric = message.text
        lyric = telebot.util.extract_arguments(lyric)

        song_names = genius.search_lyrics(lyric)
        song_names_lis = []
        for hits in song_names['sections'][0]['hits']:
            song_names_lis.append(hits['result']['full_title'])
        print(song_names)
        titles = "\n".join(song_names_lis)
        bot.send_message(message.chat.id, f"Все песни, содержащие строчку {lyric}:-\n\n{titles}")
    except:
        bot.send_message(message.chat.id, "Не смог найти подходящих песен, попробуй снова :(")


bot.polling()
