from __future__ import unicode_literals
from telegram.ext import Updater, Dispatcher, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram import Update, Audio
import tb_constants
import logging
from youtube_search import YoutubeSearch
import youtube_dl
import os


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='I am a bot. Type {/search} to search artist and song name. You will recieve a message when the file is ready for download')


def get_url(update: Update, context=CallbackContext):
    text = update.message.text
    results = YoutubeSearch(text, max_results=1).to_json()

    yt_result = results.split('"')
    new_result = yt_result[-2:-1]

    url = 'https://www.youtube.com'
    full_url = url + url.join(new_result)
    get_dl(full_url)
    context.bot.send_message(chat_id=update.effective_chat.id, text='The file is finished downloading. Type {/download} to download the file. ')
    

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
        

def get_audio(update, context):       
        for file in os.listdir(r'C:\Users\Digital\Documents\Mikyle\PyFiles'):
            if file.endswith('.mp3'):
                context.bot.send_audio(chat_id=update.effective_chat.id, audio=open(f'{file}', 'rb'))
                os.remove(file)


def main():
    updater = Updater(token=tb_constants.api_key)
    dispatcher = updater.dispatcher
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    updater.dispatcher.add_handler(CommandHandler('search', get_url))
    updater.dispatcher.add_handler(CommandHandler('download', get_audio))

    updater.start_polling()
    updater.idle()


main()