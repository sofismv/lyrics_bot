import telebot
import lyricsgenius
import json
from flask import Flask, request
import os

TOKEN = '1761980685:AAGORkIW_RKibK_gU3ntnbP-0b-cvji90hU'
genius = lyricsgenius.Genius("<genius-token>")
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def info(message):
    text = (
        "Используй /lyrics название песни, чтобы найти текст данной песни.\n"
        "Используй /findsong строчка из песни, чтобы найти название песни.\n"
    )
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['lyrics'])
def send_lyrics(message):
    bot.send_message(message.chat.id, "В поисках нужного текста, подожди чуть-чуть :)")
    song_name = message.text
    song_name = telebot.util.extract_arguments(song_name)

    lyric = genius.search_song(song_name, get_full_info=True)
    lyric = lyric.lyrics

    bot.send_message(message.chat.id, lyric)


@bot.message_handler(commands=['findsong'])
def send_songname(message):
    bot.send_message(message.chat.id, "В поисках нужной песни, подожди чуть-чуть :)")
    lyric = message.text
    lyric = telebot.util.extract_arguments(lyric)

    song_names = genius.search_lyrics(lyric)
    song_names_lis = []
    for hits in song_names['sections'][0]['hits']:
        song_names_lis.append(hits['result']['title'])

    titles = "\n".join(song_names_lis)
    bot.send_message(message.chat.id, f"Все песни, содержащие строчку {lyric}:-\n\n{titles}")


bot.polling()
