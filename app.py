import telebot

TOKEN = '5443961552:AAGG8XQrZdWXL24QOAeJLX79zLE1tXYUE_w'
bot = telebot.TeleBot(TOKEN)

money = {'евро': 'EUR',
         'доллар': 'USD',
         'доллары': 'USD',
         'долларов': 'USD',
         'российский рубль': 'RUB',
         'российских рублей': 'RUB',
         'российских рубля': 'RUB',
         'белорусский рубль': 'BYN',
         'белорусских рублей': 'BYN',
         'белорусских рубля': 'BYN',
         }

@bot.message_handler(commands=['start', 'help'])
def send__start_help(message):
    text_answer = '''Чтобы получить информацию о количестве денег, необходимых для покупки, выбранной Вами валюты по актуальному курсу, введите запрос в формате:\
     <имя валюты (или ее аббревиатура), цену которой вы хотите узнать> <имя валюты (или ее аббревиатура), в которой надо узнать цену первой валюты> <количество первой валюты>'''
    bot.reply_to(message, text_answer)

@bot.message_handler(commands=['values'])
def send__start_help(message):
    text_answer = '''Доступны к расчету курса следующие валюты: евро (EUR), доллар (USD), российский рубль (RUB), белорусский рубль (BYN)'''
    bot.reply_to(message, text_answer)

@bot.message_handler()
def echo_hello(message: telebot.types.Message):
    bot.send_message(message.chat.id, f'Hello, {message.chat.username}!')



bot.polling(none_stop=True)