import telebot
import requests
import jsons

TOKEN = '5443961552:AAGG8XQrZdWXL24QOAeJLX79zLE1tXYUE_w'
bot = telebot.TeleBot(TOKEN)

# money = {'евро': 'EUR',
#          'EUR': 'EUR',
#          'доллар': 'USD',
#          'доллары': 'USD',
#          'долларов': 'USD',
#          'USD': 'USD',
#          'российский рубль': 'RUB',
#          'российских рублей': 'RUB',
#          'российских рубля': 'RUB',
#          'RUB': 'RUB',
#          'белорусский рубль': 'BYN',
#          'белорусских рублей': 'BYN',
#          'белорусских рубля': 'BYN',
#          'BYN': 'BYN',
#          }

money = {'евро': 'EUR',
         'долларСША': 'USD',
         'росрубль': 'RUB',
         'белрубль': 'BYN',
         'англфунт': 'GBP',
         'юань': 'CNY',
         'польскийзлотый': 'PLN',
         'япониена': 'JPY'
         }

@bot.message_handler(commands=['start', 'help'])
def send__start_help(message):
    text_answer = '''Чтобы получить информацию о количестве денег, необходимых для покупки, выбранной Вами валюты по актуальному курсу, введите запрос в формате:\
<имя валюты (или ее аббревиатура), цену которой вы хотите узнать> <имя валюты (или ее аббревиатура), в которой надо узнать цену первой валюты> <количество первой валюты>\n 
Чтобы увидеть список всех достпных валют введите команду: /values'''
    bot.reply_to(message, text_answer)


@bot.message_handler(commands=['values'])
def send__start_help(message):
    text_answer = '''Доступны к расчету курса следующие валюты:\n'''
    for key in money.keys():
        text_answer += f'{key}\n'
    bot.reply_to(message, text_answer[:-1])


# @bot.message_handler()
# def echo_hello(message: telebot.types.Message):
#     bot.send_message(message.chat.id, f'Hello, {message.chat.username}!')


@bot.message_handler(content_types=['text'])
def exchange(message: telebot.types.Message):
    # r = requests.get('https://belarusbank.by/api/kursExchange')
    # texts = jsons.loads(r.content)
    # for tx in texts:
    #     print(tx)

    r = requests.get('https://www.nbrb.by/api/exrates/rates?periodicity=0')
    texts = jsons.loads(r.content)

    tx = texts[0]
    text_answer = f'Актуальные курсы на {tx["Date"]}'
    text_answer = text_answer[:30]+':\n'

    for tx in texts:
        # cur_scale = tx['Cur_Scale'] if tx['Cur_Scale']>0 else cur_scale = ''
        text_answer += tx['Cur_Abbreviation']+' '+tx['Cur_Name']+' '+str(tx['Cur_OfficialRate'])+'\n'
        print(tx['Cur_Abbreviation']+' '+tx['Cur_Name']+' '+str(tx['Cur_OfficialRate']))

    bot.send_message(message.chat.id, text_answer)


bot.polling(none_stop=True)
