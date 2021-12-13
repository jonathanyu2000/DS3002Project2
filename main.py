import tweepy
import time
import requests
import re

Bearer_Token = "AAAAAAAAAAAAAAAAAAAAAPObWwEAAAAArbgXlkVueEql0%2BTs%2BLHsoKivzlY%3DDV1SqHvUPFNOwefLYdvv24GxTi2aAWBq26oKB6DRm3QmNfNpVv"
Consumer_Key = "ffVjQ5dyx0eiNqMd4Wf24XBGG"
Consumer_Secret = "6QSlsoiBlEHIJkq1RnchjH8EvrFy3sdZKKKgwbe9eVfFncGrPg"
Access_Token = "1470107004706377734-ztbh4KR5OntR1L98um7NQPLauTY36i"
Access_Token_Secret = "wJGQD3yylSz6nszQ91h2WoqEusF468Nm3DUVtp6OwbW4v"

# Authenticate to Twitter
auth = tweepy.OAuthHandler(Consumer_Key,Consumer_Secret)
auth.set_access_token(Access_Token,Access_Token_Secret)
api = tweepy.API(auth)

try:
    api.verify_credentials()
    print("Authentication works")
except:
    print("Error")

def YahooStockAPI(stocksymbol):
    apikey='IFzpK3ZLbd6Eo9iSq2yst2qaT6uiwqj66RyAw99e'
    url = "https://yfapi.net/v6/finance/quote"
    querystring = {"symbols": stocksymbol}
    headers = {
        'x-api-key': apikey
    }
    response = requests.get(url, headers=headers, params=querystring)
    return response.json()

def FoodishAPI():
    url = "https://foodish-api.herokuapp.com/"
    response = requests.request("GET", url)
    response.raise_for_status()
    return response.json()

def replyStock():
    mentions = api.mentions_timeline(count = 1)
    for mention in reversed(mentions):
        print(str(mention.id) + ' : ' + mention.text)
        last_seen_id = mention.id
        if '$' in mention.text:
            x = re.findall("(?<=\$)[A-Z]+", mention.text)
            for stock in x:
                try:
                    stock_json = YahooStockAPI(stock)
                    status = '@' + mention.user.screen_name + ' ' + (
                            stock_json['quoteResponse']['result'][0]["shortName"] + "\n"
                                                                                    "Regular Market Day High: $" + str(
                        stock_json['quoteResponse']['result'][0]['regularMarketDayHigh']) + "\n"
                                                                                            "Regular Market Day Low: $" + str(
                        stock_json['quoteResponse']['result'][0]['regularMarketDayLow']) + "\n"
                                                                                           "Fifty Day Average: $" + str(
                        stock_json['quoteResponse']['result'][0]['fiftyDayAverage']) + "\n"
                                                                                       "Price: $" + str(
                        stock_json['quoteResponse']['result'][0]["regularMarketPrice"]) + "\n"
                                                                                          "Market Time: " + str(
                        time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(
                            (stock_json['quoteResponse']['result'][0]["regularMarketTime"])))) + "\n"
                    )
                except:
                    status = '@' + mention.user.screen_name + " There is no valid stock ticker in your tweet...please try again with a valid stock ticker"

                try:
                    api.update_status(status=status, in_reply_to_status_id=last_seen_id)
                except:
                    print("Already Replied To")

        if "food" in mention.text:
            food_json = FoodishAPI()
            print(food_json)
            status = food_json["image"]
            try:
                api.update_status(status=status, in_reply_to_status_id=last_seen_id)
            except:
                print("Already Replied To")

        else:
            status = '@' + mention.user.screen_name + " There is no valid stock ticker in your tweet...please try again with a valid stock ticker"
            try:
                api.update_status(status=status, in_reply_to_status_id=last_seen_id)
            except:
                print("Already Replied To")

    return

while True:
    replyStock()
    time.sleep(15)