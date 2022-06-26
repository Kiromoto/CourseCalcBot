import telebot
import requests
import jsons
from config import TOKEN, money
from extensions import ConvertException, Exchangers

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def send__start_help(message):
    text_answer = '''Чтобы получить информацию о количестве денег, необходимых для покупки, выбранной Вами валюты по актуальному курсу, введите запрос в формате: \
"количество первой валюты" "международную аббревиатуру валюты)" "аббревиатуру валюты в которую нужно пересчитать сумму"\n
Пример ввода: "100 USD BYN"\n
Чтобы увидеть список всех достпных валют введите команду: /values\n
Чтобы узнать актуальный курс белорусского рубля к другим валютам введите команду: /BYN'''
    bot.reply_to(message, text_answer)


@bot.message_handler(commands=['values'])
def send_start_help(message):
    text_answer = '''Доступны к расчету курса следующие валюты:\n'''
    for key in money.keys():
        text_answer += f'{key} - {money.get(key)}\n'
    bot.reply_to(message, text_answer[:-1])


@bot.message_handler(commands=['BYN', 'Byn', 'byn'])
def byn_courses(message):
    try:
        r = requests.get('https://www.nbrb.by/api/exrates/rates?periodicity=0')
        texts = jsons.loads(r.content)

        tx = texts[0]
        text_answer = f'Актуальный курс белорусского рубля к иностранным валютам на {tx["Date"]}'
        text_answer = text_answer[:70] + ':\n'

        for tx in texts:
            text_answer += f'{tx["Cur_Scale"]} {tx["Cur_Name"]} {tx["Cur_Abbreviation"]} --> {tx["Cur_OfficialRate"]} BYN \n'
    except ConvertException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        bot.send_message(message.chat.id, text_answer)


@bot.message_handler(content_types=['text'])
def telegram_convert(message: telebot.types.Message):
    try:
        str_command = message.text.split(' ')
        if len(str_command) < 3:
            raise ConvertException('Вы указали недостаточно параметров. Пример запроса: "100 USD BYN"')
        elif len(str_command) > 3:
            raise ConvertException('Вы указали лишние параметры. Пример запроса: "100 USD BYN"')

        amount, base, quote = str_command
        base = base.upper()
        quote = quote.upper()
        if base == 'BYN' or quote == 'BYN':
            text_answer = Exchangers.get_price_nbrb(amount, base, quote)
        else:
            text_answer = Exchangers.get_price_exchangerates(amount, base, quote)
    except ConvertException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        bot.reply_to(message, text_answer)


bot.polling(none_stop=True)
