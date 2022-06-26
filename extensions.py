import requests
import jsons
from config import money, money_abbreviation


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
                    text_answer = f'{(float(amount)):.2f} {get_key_money(money, base)} {base} ==> {sum:.2f} {get_key_money(money, quote)} {quote}'
                elif tx["Cur_Abbreviation"] == quote:
                    sum = (float(amount)) / tx["Cur_OfficialRate"] * tx["Cur_Scale"]
                    text_answer = f'{(float(amount)):.2f} {get_key_money(money, base)} {base} ==> {sum:.2f} {get_key_money(money, quote)} {quote}'

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
            text_answer = f'{(float(amount)):.2f} {get_key_money(money, base)} {base} ==> {float(result["result"]):.2f} {get_key_money(money, quote)} {quote}'
        else:
            text_answer = 'Что-то пошло не так!'

        return text_answer


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
        raise ConvertException('Количество валюты должно быть указано числом.\nПример запроса: "100 USD BYN"')

    if float(amount) <= 0:
        input_ok = False
        raise ConvertException('Количество валюты должно быть положительным числом.\nПример запроса: "100 USD BYN"')

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
        raise ConvertException(f'Вы указали одинаковые валюты {base}.\nПример запроса: "100 USD BYN"')

    return input_ok

