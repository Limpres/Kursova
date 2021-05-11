from bs4 import BeautifulSoup
import requests
import datetime
from time import sleep
from config import TOKEN, urls, subscriptions, set_time, my_id
import re


class BotHandler:

    def __init__(self, token):
        self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(token)

    def get_updates(self, offset=None, timeout=20):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method, params)
        result_json = resp.json()['result']
        return result_json

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp

    def get_last_update(self):
        results = self.get_updates()
        if len(results) > 0:      
            last_update = results[-1]
        else:
            last_update = None
        return last_update

    def send_subscription(self, chat_id):
        if datetime.datetime.today().strftime("%H:%M") == set_time:
            for sub in subscriptions:
                params = {'chat_id': chat_id, 'text': investing_parser(sub)}
                method = 'sendMessage'
                resp = requests.post(self.api_url + method, params)


def investing_parser(ticker):
    try:
        response = requests.get(urls[ticker], headers={"user-agent": "Mozilla/5.0 (X11; Linux x86_64) \
                                                                     AppleWebKit/537.36 (K HTML, like Gecko) \
                                                                     Chrome/53.0.2785.143 Safari/537.36"})
        soup = BeautifulSoup(response.content, "html.parser")
        pattern = re.compile('Фибоначчи')
        pattern1 = re.compile('RSI')

        value = soup.find('input', {'class': 'newInput inputTextBox alertValue'}).get('value')
        value = value.replace(".", "")
        value = value.replace(",", ".")
        investing_price = round(float(value), 4)

        change = soup.find('div', {'class': 'top bold inlineblock'}).findAll('span')
        change_ = change[1].text
        change_persent = change[3].text

        pivot = soup.find('td', text=pattern).parent.findAll('td', {'class': 'bold'})[1].text

        rsi0 = soup.find('td', text=pattern1).parent.findAll('td')[1].text

        resume = soup.find('td', {'class': 'first left lastRow'}).findAll('p')[3].find('span').text

        resp = '{} \n\nPrice : {} \n\nChange for today : {} \n\nChange in % : {} \n\nPivot points Fibbo. : {} \n\nRSI : {} \n\nCommon solution out of tec.analisis : {}'.format(ticker, investing_price, change_, change_persent, pivot, rsi0, resume)
    except KeyError:
        resp = "You can append {}'s URL to config file.".format(ticker)
    return resp


def main():
    investing_bot = BotHandler(TOKEN)
    new_offset = None
    while True:
        investing_bot.get_updates(new_offset)
        last_update = investing_bot.get_last_update()
        investing_bot.send_subscription(my_id)
        if last_update:
            last_update_id = last_update['update_id']
            last_chat_text = last_update['message']['text']
            last_chat_id = last_update['message']['chat']['id']
            response = investing_parser(last_chat_text)
            investing_bot.send_message(last_chat_id, '{}'.format(response))
            new_offset = last_update_id + 1
        sleep(1)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
