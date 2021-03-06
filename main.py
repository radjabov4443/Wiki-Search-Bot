from telegram.bot import Bot
from telegram.user import User
from telegram.ext import Updater, Dispatcher, CommandHandler, CallbackContext, MessageHandler
from telegram.update import Update
from telegram.ext.filters import Filters
import requests
import settings
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG)

updater = Updater(token=settings.TELEGRAM_TOKEN)


def start(update: Update, context: CallbackContext):
    update.message\
        .reply_text('Assalamu Alaykum! Vikipediyadan ma\'lumot qidiruvchi '
                    'botga Xush kelibsiz! Biron nima izlash uchun /search '
                    'va so\'rovingizni yozing. Misol uchun /search Amir Temur')

def search(update: Update, context: CallbackContext):
    args = context.args

    logging.info('checking args length')

    if len(args) == 0:
        update.message.reply_text('Hech bo\'lmasa nimadir kiriting. Misol uchun /search Amir Temur')
    else:
        search_text = ' '.join(args)
        logging.info('sending request to Wikipedia API')
        response = requests.get('https://uz.wikipedia.org/w/api.php', {
            'action': 'opensearch',
            'search': search_text,
            'limit': 1,
            'namespace': 0,
            'format': 'json',
        })

        logging.info('result from Wikipedia API')
        result = response.json()
        link = result[3]

        if len(link):
            update.message\
                .reply_text('Sizning so\'rovingiz bo\'yicha havola: ' + link[0])
        else:
            update.message\
                .reply_text('Sizning so\'rovingiz bo\'yicha hech nima yo\'q!')


dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('search', search))
dispatcher.add_handler(MessageHandler(Filters.all, start))

updater.start_polling()
updater.idle()
