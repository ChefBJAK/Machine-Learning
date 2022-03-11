from neuralintents import GenericAssistant
import matplotlib.pyplot as plt
import pandas as pd
import pandas_datareader as web
import mplfinance as mpf

import pickle
import sys
import datetime as dt

portfolio = {'APPL': 20, 'TSLA' : 5, 'GS' : 10}

with open('portfolio.pkl', 'wb') as f:
    portfolio = pickle.load(f)

def save_portfolio():
    with open('portfolio.pkl', 'wb') as f:
        pickle.dump(portfolio, f)

def add_portfolio():
    ticker = input("Which stock do you want to add: ")
    amount = input("How many shares do you want to add: ")

    if ticker in portfolio.keys():
        portfolio[ticker]+= int(amount)
    else:
        portfolio[ticker] = int(amount)
    
    save_portfolio()

def remove_portfolio():
    ticker = input("Which stock do you want to sell: ")
    amount = input("How many shares do you want to sell: ")

    if ticker in portfolio.keys():
        if amount <= portfolio(ticker):
            portfolio[ticker] -= int(amount)
            save_portfolio()
        else:
            print("You don't have enough shares")
    else:
        print(f"You don't own any shares of {ticker}")

def show_portfolio():
    print("Your Portfolio")
    for ticker in portfolio.keys():
        print(f"You own{portfolio[ticker]} shares of {ticker}")

def plot_chart():
    ticker = input("Choose a ticker symbol: ")
    starting_string = input("Choose a starting date (DD/MM/YYY)")

    plt.style.use('dark_background')

    start = dt.datetime.strptime(starting_string, "%d/%m/%Y")
    end = dt.datetime.now()

    data = web.DataReader(ticker, 'yahoo', start, end)

    colors = mpf.make_marketcolors(up='#00ff00', down="#ff0000", wick = 'inherit', edge='inherit', volume='in')
    mpf_style = mpf.make_mpf_style(base_mpf_style='nightclouds', marketcolors=colors)
    mpf.plot(data, type='candle', style=mpf_style, volume=True)

def bye():
    print("goodby")
    sys.exit(0)

mappings = {
    'plot_chart' : plot_chart,
    'add_portfolio' : add_portfolio,
    'remove_portfolio' : remove_portfolio,
    'show_portfolio' : show_portfolio,
    'bye' : bye
}

assistant = GenericAssistant('intents.json', mappings, "financial_assistant_model")

assistant.train_model()
assistant.save_model()

while True:
    message = input("")
    assistant.request(message)
