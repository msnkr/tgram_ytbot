from __future__ import unicode_literals
from telegram.ext import Updater, Dispatcher, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram import Update, Audio, Video
import logging
from youtube_search import YoutubeSearch
import youtube_dl
import os

try:
    def start(update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text='I am a bot. Type {/audio {artist song}} to search artist and song name audio. Type {/video} to search artist and song video. You will recieve a message when the file is ready for download. Example {/video Joji Gimme Love}. ')


    def get_audio_url(update: Update, context=CallbackContext):
        for file in os.listdir(r'C:\Users\Digital\Documents\GitHub\tgram_ytbot'):
                if file.endswith('.mp3'):
                    os.remove(file)

        text = update.message.text
        results = YoutubeSearch(text, max_results=1).to_json()

        yt_result = results.split('"')
        new_result = yt_result[-2:-1]

        url = 'https://www.youtube.com'
        full_url = url + url.join(new_result)
        print(full_url)
        get_audio_dl(full_url)
        context.bot.send_message(chat_id=update.effective_chat.id, text='The file is finished downloading. Type {/downloadaudio} to download the file. ')
        

    def get_audio_dl(full_url):
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
            for file in os.listdir(r'C:\Users\Digital\Documents\GitHub\tgram_ytbot'):
                if file.endswith('.mp3'):
                    context.bot.send_audio(chat_id=update.effective_chat.id, audio=open(f'{file}', 'rb'))
                    os.remove(file)


    def get_video_url(update: Update, context=CallbackContext):
        for file in os.listdir(r'C:\Users\Digital\Documents\GitHub\tgram_ytbot'):
                if file.endswith('.mp4'):
                    os.remove(file)

        text = update.message.text
        results = YoutubeSearch(text, max_results=1).to_json()

        yt_result = results.split('"')
        new_result = yt_result[-2:-1]

        url = 'https://www.youtube.com'
        full_url = url + url.join(new_result)
        get_video_dl(full_url)
        context.bot.send_message(chat_id=update.effective_chat.id, text='The file is finished downloading. Type {/downloadvideo} to download the file. ')
        

    def get_video_dl(full_url):
        with youtube_dl.YoutubeDL({'format': '18'}) as ydl:
            ydl.download([full_url])
            

    def get_video(update, context):       
            for file in os.listdir(r'C:\Users\Digital\Documents\GitHub\tgram_ytbot'):
                if file.endswith('.mp4'):
                    context.bot.send_video(chat_id=update.effective_chat.id, video=open(f'{file}', 'rb'))
                    os.remove(file)


    def main():
        updater = Updater(token='2142016721:AAE22YldNZti1624JLxBuAS6ko5oUqAX51I')
        dispatcher = updater.dispatcher
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

        start_handler = CommandHandler('start', start)
        dispatcher.add_handler(start_handler)

        updater.dispatcher.add_handler(CommandHandler('audio', get_audio_url))
        updater.dispatcher.add_handler(CommandHandler('video', get_video_url))
        updater.dispatcher.add_handler(CommandHandler('downloadaudio', get_audio))
        updater.dispatcher.add_handler(CommandHandler('downloadvideo', get_video))

        updater.start_polling()
        updater.idle()


    main()

except FileNotFoundError:
    pass
