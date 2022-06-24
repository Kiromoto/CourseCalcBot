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

@bot.message_handler(commands=['start', 'help'])
def send__start_help(message):
    text_answer = '''Чтобы получить информацию о количестве денег, необходимых для покупки, выбранной Вами валюты по актуальному курсу, введите запрос в формате:\
<имя валюты (или ее аббревиатура), цену которой вы хотите узнать> <имя валюты (или ее аббревиатура), в которой надо узнать цену первой валюты> <количество первой валюты>\n 
Чтобы увидеть список всех достпных валют введите команду: /values\n
Чтобы узнать актуальный курс белорусского рубля к другим валютам введите команду: /BYN'''
    bot.reply_to(message, text_answer)


@bot.message_handler(commands=['values'])
def send__start_help(message):
    text_answer = '''Доступны к расчету курса следующие валюты:\n'''
    for key in money.keys():
        text_answer += f'{key}\n'
    bot.reply_to(message, text_answer[:-1])


@bot.message_handler(commands=['BYN'])
def byn_courses(message):
    r = requests.get('https://www.nbrb.by/api/exrates/rates?periodicity=0')
    texts = jsons.loads(r.content)

    tx = texts[0]
    text_answer = f'Актуальные курс белорусского рубля к иностранным валютам на {tx["Date"]}'
    text_answer = text_answer[:70] + ':\n'
    m = ''

    for tx in texts:
        text_answer += f'{tx["Cur_Scale"]} {tx["Cur_Name"]} {tx["Cur_Abbreviation"]} --> {tx["Cur_OfficialRate"]} BYN \n'
        # print(f'{tx["Cur_Scale"]} {tx["Cur_Name"]} {tx["Cur_Abbreviation"]} --- {tx["Cur_OfficialRate"]} BYN')
        m += f''' "{tx["Cur_Name"]}": "{tx["Cur_Abbreviation"]}", '''

    print(m)
    bot.send_message(message.chat.id, text_answer)


@bot.message_handler(content_types=['text'])
def exchange(message: telebot.types.Message):
    base, qoute, amount = message.text.split(' ')
    print(qoute, base, amount)
    base = money.get(base) if base in money.keys() else money_abbreviation.get(base)
    qoute = money.get(qoute) if qoute in money.keys() else money_abbreviation.get(qoute)
    print(qoute, base, amount)
    url = f"https://api.apilayer.com/exchangerates_data/convert?to={qoute}&from={base}&amount={amount}"

    payload = {}
    headers = {"apikey": "EMH1WNGM1H5SS5pMdM8JPPsuthqIbEUB"}

    response = requests.request("GET", url, headers=headers, data=payload)
    # result = response.text
    result = jsons.loads(response.content)
    text_answer = f'{result["query"]} --> {result["result"]}'
    print(type(result))
    print(result)

    bot.send_message(message.chat.id, text_answer)


bot.polling(none_stop=True)
