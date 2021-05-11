import datetime

TOKEN = """1818574200:AAEv8q_kWQZGjn1ESD6f4sxOXctsJYFBphw"""

urls = {'ETH/USD': 'https://ru.investing.com/crypto/ethereum/eth-usd-technical',
        'BTC/USD': 'https://ru.investing.com/crypto/bitcoin/btc-usd-technical',
        'LTC/USD': 'https://ru.investing.com/crypto/litecoin/ltc-usd-technical',
        'ETC/USD': 'https://ru.investing.com/crypto/ethereum-classic/etc-usd-technical',
        'ETH/BTC': 'https://ru.investing.com/crypto/ethereum/eth-btc-technical',
        'IOTA/USD': 'https://ru.investing.com/crypto/iota/iota-usd-technical',
        'XRP/USD': 'https://ru.investing.com/crypto/xrp/xrp-usd-technical'}

subscriptions = ['ETH/USD', 'BTC/USD']

set_time = datetime.time(1, 8).strftime("%H:%M")

my_id = '299013792'
