import requests
import os
import sys
import json
import copy
import pandas as pd
import datetime
import itertools
from dotenv import load_dotenv

sys.path.append(os.path.realpath(__file__).split("stock_data")[0]+"stock_data")

#Load in env variables
load_dotenv()
polygon_key = os.environ.get("polygon_key")

# from lib.helper import *
# from lib.env import *

def get_company_details(ticker):
    company_details = "https://api.polygon.io/v3/reference/tickers/{ticker}?apiKey={polygon_key}"
    r = requests.get(company_details.format(polygon_key = polygon_key, ticker=ticker))
    response_text = r.text
    response_dict = json.loads(response_text)
    results_dict = response_dict["results"]
    interested_keys = ["ticker", "name", "homepage_url", "phone_number", "market_cap", "currency_name", "address", "total_employees"]
    interested_results = {}
    for key in interested_keys:
        address_string = ""
        if key == 'address':
                for address_key in results_dict["address"].keys():
                    address_string = address_string + " " + results_dict["address"][address_key]
                    address_string = address_string[1:]
                interested_results[key] = address_string    
        else:
            interested_results[key] = results_dict[key]

    return copy.deepcopy(interested_results)

def get_open_close(ticker, date):
    open_close = "https://api.polygon.io/v1/open-close/{ticker}/{date}?adjusted=true&apiKey={polygon_key}"
    r = requests.get(open_close.format(ticker=ticker, polygon_key=polygon_key, date=date))
    response_text = r.text
    response_dict = json.loads(response_text)

    return copy.deepcopy(response_dict)


def company_detail_to_df(tickers):
    tickers = ["AAPL", "TSLA", "AMZN"]
    all_data = []
    for ticker in tickers: 
        all_data.append(get_company_details(ticker))

    return pd.DataFrame(all_data)


def open_close_to_df(tickers):
    all_data = []
    for key, value in tickers: 
        # for v in value: 
        #     all_data.append(get_open_close(key, str(v)))
        all_data.append(get_open_close(key, str(value)))
    df = pd.DataFrame(all_data)
    df = df.loc[:, df.columns != "status"]
    df = df.rename(columns={"from" : "date"})
    return df

tickers = ["AMZN", "TSLA"]
dates = ["2023-05-03", "2023-03-02"]

ticker_dates = list(itertools.product(tickers, dates))
# tickers = {"AMZN": ["2023-05-03", "2023-03-02"], "TSLA" : ["2023-05-02"]}
# # print(tickers)

print(open_close_to_df(tickers=ticker_dates))
# print(company_detail_to_df(tickers=tickers))