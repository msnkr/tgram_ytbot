from __future__ import unicode_literals
from telegram.ext import Updater, Dispatcher, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram import Update, Audio
import tb_constants
import logging
from youtube_search import YoutubeSearch
import youtube_dl
import os


def start(update, bot):
    bot.send_message(chat_id=update.effective_chat.id, text='I am a bot.')


def get_url(update: Update, context=CallbackContext ):
    text = update.message.text
    results = YoutubeSearch(text, max_results=1).to_json()

    yt_result = results.split('"')
    new_result = yt_result[-2:-1]

    url = 'https://www.youtube.com'
    full_url = url + url.join(new_result)
    get_dl(full_url)
    

def get_dl(full_url):
    ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }]}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([full_url])
 

def aud(update, context):
    for audio_file in os.listdir(r'C:\Users\Digital\Documents\Mikyle\PyFiles'):
        context.bot.send_audio(chat_id=update.effective_chat.id, audio=open(f'{audio_file}.mp3', 'rb'))


def main():
    updater = Updater(token=tb_constants.api_key)
    dispatcher = updater.dispatcher
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    updater.dispatcher.add_handler(CommandHandler('download', get_url))


    updater.start_polling()
    updater.idle()


main()