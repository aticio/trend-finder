import json
from datetime import datetime
import requests
import time
from multiprocessing import Process
import schedule


EXCHANGE_INFO = "https://api.binance.com/api/v3/exchangeInfo"
TICKER_INFO = "https://api.binance.com/api/v3/ticker/24hr"

CANDIDATES = []

def main():
    schedule.every().minute.do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)


def init_ops():
    exchange_info = get_exchange_info()
    pairs = get_pairs(exchange_info)
    busd_pairs = filter_busd_pairs(pairs)

    ticker_info = get_ticker_info()
    for ticker in ticker_info:
        for bp in busd_pairs:
            if ticker["symbol"] == bp:
                if float(ticker["priceChangePercent"]) > 2.0:
                    if bp not in CANDIDATES:
                        CANDIDATES.append(bp) 


def filter_busd_pairs(pairs):
    busd_paris = []
    for pair in pairs:
        if "BUSD" in pair and "USDT" not in pair and "USDC" not in pair and "USDC" not in pair:
            busd_paris.append(pair)
    return busd_paris


def get_pairs(exchange_info):
    pairs = []
    for symbol in exchange_info["symbols"]:
        if symbol["status"] == "TRADING":
            pairs.append(symbol["symbol"])
    return pairs


def get_exchange_info():
    response = requests.get(EXCHANGE_INFO)
    exchange_info = response.json()
    return exchange_info


def get_ticker_info():
    response = requests.get(TICKER_INFO)
    ticker_info = response.json()
    return ticker_info


if __name__ == "__main__":
    main()