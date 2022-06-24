import requests

url = "https://api.apilayer.com/exchangerates_data/convert?to=RUB&from=EUR&amount=100"

payload = {}
headers = {"apikey": "EMH1WNGM1H5SS5pMdM8JPPsuthqIbEUB"
           }

response = requests.request("GET", url, headers=headers, data=payload)

status_code = response.status_code
result = response.text
print(type(result))
print(result)

