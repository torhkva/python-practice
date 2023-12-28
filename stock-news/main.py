from datetime import datetime, timedelta
import requests
import os
from twilio.rest import Client

#Se declaran las variables iniciales
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
TO = os.environ.get("cel_number")


# Esta función obtiene los valores de la accion deseada
def get_stock_price(STOCK, COMPANY_NAME, TO):
    # Se obtiene primeramente la llave de la API de una variable de entorno
    alva_api_key = os.environ.get("ALVA_API_KEY")
    # Se declara la url del API utilizando como variables el stock y la llave del API

    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={STOCK}&apikey={alva_api_key}'
    # Se hace la petición y se usa el try and except para cachar algún error
    try:
        response = requests.get(url=url)
        if response.status_code == 200:
            result = response.json()
            list_close_values = []
            for key, value in list(result["Time Series (Daily)"].items())[:2]:
                list_close_values.append(value["4. close"])
            variance = round(((float(list_close_values[0]) - float(list_close_values[1])) / float(list_close_values[1] )) * 100, 2)
            if variance >= 5.0:
                stock_variance = f"{STOCK}: 🔼 {variance}%"
                get_stock_news(stock_variance, COMPANY_NAME, TO)
            elif variance <= -5.0:
                stock_variance = f"{STOCK}: 🔽 {variance}%"
                get_stock_news(stock_variance, COMPANY_NAME, TO)
            else:
                return print(f"No news {variance}")
        else:
            print(f'Error: {response.status_code}')
            print(response.text)
    except Exception as e:
        print(f'Error: {e}')


# Esta función obtiene las dos noticias mas relevantes sobre la acción deseada
def get_stock_news(stock_variance, COMPANY_NAME, TO):
    neap_api_key = os.environ.get("NEAP_API_KEY")
    news_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    url = f"https://newsapi.org/v2/everything?q={COMPANY_NAME}&from={news_date}&sortBy=publishedAt&apiKey={neap_api_key}"
    try:
        response = requests.get(url=url)
        if response.status_code == 200:
            result = response.json()
            list_news = []
            for items in result["articles"][:2]:
                text_news = f"Headline: {items['title']}\nBrief: {items['description']}\n"
                list_news.append(text_news)
            news = ("".join(list_news))
            send_sms(stock_variance, news, TO)
        else:
            print(f'Error: {response.status_code}')
            print(response.text)
    except Exception as e:
        print(f'Error: {e}')


# Esta función manda un mensaje sms con los datos anteriores
def send_sms(stock_variance, news, TO):
    account_sid = os.environ.get("account_sid")
    auth_token = os.environ.get("auth_token")
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        from_=os.environ.get("twilio_number"),
        body=f"{stock_variance}\n{news}",
        to=f'{TO}'
    )
    print(message.sid)

get_stock_price(STOCK, COMPANY_NAME, TO)

