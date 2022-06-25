import telebot
import requests
import jsons

TOKEN = '5443961552:AAGG8XQrZdWXL24QOAeJLX79zLE1tXYUE_w'
bot = telebot.TeleBot(TOKEN)


def get_key_money(d, value):
    for k, v in d.items():
        if v == value:
            return k


def input_validation(amount, base, quote):
    global input_ok
    input_ok = True
    try:
        amount_fl = float(amount)
    except KeyError:
        input_ok = False
        raise ConvertException('Ошибка запроса! Количество валюты должно быть указано числом.\nПример: "100 USD BYN"')

    if float(amount) <= 0:
        input_ok = False
        raise ConvertException(
            'Ошибка запроса! Количество валюты должно быть положительным числом.\nПример: "100 USD BYN"')

    if base in money:
        base = money.get(base)
    elif base not in money_abbreviation:
        input_ok = False
        raise ConvertException(f'Для валюты {base} расчет не возможен!')

    if quote in money:
        quote = money.get(quote)
    elif quote not in money_abbreviation:
        input_ok = False
        raise ConvertException(f'Для валюты {quote} расчет не возможен!')

    if base == quote:
        input_ok = False
        raise ConvertException('Ошибка запроса! Вы указали одинаковые валюты.\nПример: "100 USD BYN"')

    return input_ok


class ConvertException(Exception):
    pass


class Exchangers:
    @staticmethod
    def get_price_nbrb(amount, base, quote):
        if input_validation(amount, base, quote):
            r = requests.get('https://www.nbrb.by/api/exrates/rates?periodicity=0')
            texts = jsons.loads(r.content)
            for tx in texts:
                if tx["Cur_Abbreviation"] == base:
                    sum = (float(amount)) / tx["Cur_Scale"] * tx["Cur_OfficialRate"]
                    text_answer = f'{(float(amount)):.2f} {get_key_money(money, base)} {base} стоят {sum:.2f} {get_key_money(money, quote)} {quote}'
                elif tx["Cur_Abbreviation"] == quote:
                    sum = (float(amount)) / tx["Cur_OfficialRate"] * tx["Cur_Scale"]
                    text_answer = f'{(float(amount)):.2f} {get_key_money(money, base)} {base} стоят {sum:.2f} {get_key_money(money, quote)} {quote}'

        else:
            text_answer = 'Что-то пошло не так!'

        return text_answer

    @staticmethod
    def get_price_exchangerates(amount, base, quote):
        if input_validation(amount, base, quote):
            url = f"https://api.apilayer.com/exchangerates_data/convert?to={quote}&from={base}&amount={amount}"
            payload = {}
            headers = {"apikey": "EMH1WNGM1H5SS5pMdM8JPPsuthqIbEUB"}
            response = requests.request("GET", url, headers=headers, data=payload)
            result = jsons.loads(response.content)
            text_answer = f'{(float(amount)):.2f} {get_key_money(money, base)} {base} стоят {float(result["result"]):.2f} {get_key_money(money, quote)} {quote}'
        else:
            text_answer = 'Что-то пошло не так!'

        return text_answer


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
    r = requests.get('https://www.nbrb.by/api/exrates/rates?periodicity=0')
    texts = jsons.loads(r.content)

    tx = texts[0]
    text_answer = f'Актуальный курс белорусского рубля к иностранным валютам на {tx["Date"]}'
    text_answer = text_answer[:70] + ':\n'

    for tx in texts:
        text_answer += f'{tx["Cur_Scale"]} {tx["Cur_Name"]} {tx["Cur_Abbreviation"]} --> {tx["Cur_OfficialRate"]} BYN \n'

    bot.send_message(message.chat.id, text_answer)


@bot.message_handler(content_types=['text'])
def telegram_convert(message: telebot.types.Message):
    str_command = message.text.split(' ')
    if len(str_command) < 3:
        raise ConvertException('Ошибка запроса! Вы указали недостаточно параметров. Пример: "100 USD BYN"')
    elif len(str_command) > 3:
        raise ConvertException('Ошибка запроса! Вы указали лишние параметры. Пример: "100 USD BYN"')

    amount, base, quote = str_command
    base = base.upper()
    quote = quote.upper()
    if base == 'BYN' or quote == 'BYN':
        text_answer = Exchangers.get_price_nbrb(amount, base, quote)
    else:
        text_answer = Exchangers.get_price_exchangerates(amount, base, quote)

    bot.reply_to(message, text_answer)

    # if not amount.isdigit():
    #     raise ConvertException('Ошибка запроса! Количество валюты должно быть указано числом. Пример: "100 USD BYN"')
    #
    # if int(amount) <= 0:
    #     raise ConvertException(
    #         'Ошибка запроса! Количество валюты должно быть положительным числом. Пример: "100 USD BYN"')
    #
    # if len(base) == len(quote) == 3:
    #     base = base.upper()
    #     quote = quote.upper()
    #     if base == quote:
    #         raise ConvertException('Ошибка запроса! Вы указали одинаковые валюты. Пример: "100 USD BYN"')
    #
    #     if base not in money_abbreviation:
    #         raise ConvertException(f'Для валюты {base} расчет не возможен!')
    #
    #     if quote not in money_abbreviation:
    #         raise ConvertException(f'Для валюты {quote} расчет не возможен!')
    #
    #
    #
    #     base = money.get(base) if base in money.keys() else money_abbreviation.get(base)
    #     quote = money.get(quote) if quote in money.keys() else money_abbreviation.get(quote)
    #
    #     url = f"https://api.apilayer.com/exchangerates_data/convert?to={quote}&from={base}&amount={amount}"
    #
    #     payload = {}
    #     headers = {"apikey": "EMH1WNGM1H5SS5pMdM8JPPsuthqIbEUB"}
    #
    #     response = requests.request("GET", url, headers=headers, data=payload)
    #     result = jsons.loads(response.content)
    #     text_answer = f'{(float(amount)):.2f} {get_key_money(money, base)} {base} стоят {float(result["result"]):.2f} {get_key_money(money, quote)} {quote}'
    #
    #
    #     bot.send_message(message.chat.id, text_answer)
    # else:
    #     raise ConvertException(
    #         'Ошибка запроса! Международный код валюты должен содержать 3 символа. Пример: "100 USD BYN"')


money = {"Австралийский_доллар": "AUD",
         "Армянский_драм": "AMD",
         "Болгарский_лев": "BGN",
         "Белорусский_рубль": "BYN",
         "Гривна": "UAH",
         "Датская_крона": "DKK",
         "Доллар_США": "USD",
         "Евро": "EUR",
         "Злотый": "PLN",
         "Иена": "JPY",
         "Иранский_риал": "IRR",
         "Исландская_крона": "ISK",
         "Канадский_доллар": "CAD",
         "Китайский_юань": "CNY",
         "Кувейтский_динар": "KWD",
         "Молдавский_леев": "MDL",
         "Новозеландский_доллар": "NZD",
         "Норвежская_крона": "NOK",
         "Российских_рублей": "RUB",
         "Сингапурcкий_доллар": "SGD",
         "Сомы": "KGS",
         "Тенге": "KZT",
         "Турецкая_лира": "TRY",
         "Фунт_стерлингов": "GBP",
         "Чешская_крона": "CZK",
         "Шведская_крона": "SEK",
         "Швейцарский_франк": "CHF"
         }

money_abbreviation = {"AUD": "AUD", "AMD": "AMD", "BGN": "BGN", "UAH": "UAH", "DKK": "DKK", "USD": "USD", "EUR": "EUR",
                      "PLN": "PLN", "JPY": "JPY", "IRR": "IRR", "ISK": "ISK", "CAD": "CAD", "CNY": "CNY", "KWD": "KWD",
                      "MDL": "MDL", "NZD": "NZD", "NOK": "NOK", "RUB": "RUB", "SGD": "SGD", "KGS": "KGS", "KZT": "KZT",
                      "TRY": "TRY", "GBP": "GBP", "CZK": "CZK", "SEK": "SEK", "CHF": "CHF", "BYN": "BYN"
                      }



bot.polling(none_stop=True)
