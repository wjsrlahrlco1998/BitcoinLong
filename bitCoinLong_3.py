import pyupbit
import time
import datetime
import random
import numpy as np

access = ""
secret = ""

########################################################################

def get_start_time(ticker):
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time

def get_target_price(ticker, k):
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_ma15(ticker):
    df = pyupbit.get_ohlcv(ticker, interval="day", count=15)
    ma15 = df['close'].rolling(15).mean().iloc[-1]
    return ma15

def get_balance(ticker):
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0

def get_current_price(ticker):
    return pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]

def get_best_k(ticker):
    best_ror = 0
    best_k = 0.5
    for k in np.arange(0.1, 1.0, 0.1):
        df = pyupbit.get_ohlcv(ticker, count=7)
        df['range'] = (df['high'] - df['low']) * k
        df['target'] = df['open'] + df['range'].shift(1)

        df['ror'] = np.where(df['high'] > df['target'],
                             df['close'] / df['target'],
                             1)

        ror = df['ror'].cumprod()[-2]

        if best_ror < ror:
            best_ror = ror
            best_k = k

    return best_k

def colander_list(list):
    temp_list = []
    for i in list:
        df = pyupbit.get_ohlcv(i, count=7)
        if df is not None:
            if len(df) == 7:
                temp_list.append(i)
    return temp_list

########################################################################
# (초기)코인설정
coin_list = pyupbit.get_tickers(fiat="KRW")
coin_list = colander_list(coin_list)
rand_coin = random.choice(coin_list)
k = get_best_k(rand_coin)

choice_count = 0

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("Autotrade start")

while True:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time(rand_coin)
        end_time = start_time + datetime.timedelta(days=1)
        if start_time < now < end_time - datetime.timedelta(seconds=10):
            target_price = get_target_price(rand_coin, k)
            ma15 = get_ma15(rand_coin)
            current_price = get_current_price(rand_coin)
            if target_price < current_price and ma15 < current_price:
                krw = get_balance("KRW")
                if krw > 5000:
                    upbit.buy_market_order(rand_coin, krw*0.9995)
                    print(now, "Buy :", rand_coin)
                    choice_count = 1
            else:
                if choice_count == 0:
                    rand_coin = random.choice(coin_list)
                    k = get_best_k(rand_coin)

        else:
            numberOfCoin = get_balance(rand_coin[4:])
            if numberOfCoin > (5000 / get_current_price(rand_coin)):
                upbit.sell_market_order(rand_coin, numberOfCoin)
                print(now, "Sell :", rand_coin)
                rand_coin = random.choice(coin_list)
                k = get_best_k(rand_coin)
                choice_count = 0
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)
