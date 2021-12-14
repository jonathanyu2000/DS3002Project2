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

filename = "mentionid.txt"
def replyStock():
    mentions = api.mentions_timeline(count=1)
    for mention in reversed(mentions):
        mentionfile = open(filename, "a+")
        mentionfile.seek(0, 0)
        if (str(mention.id)+"\n") in mentionfile.readlines():
            print("Already replied to")
        else:
            mentionfile.write(str(mention.id) + "\n")
            print(str(mention.id) + ' : ' + mention.text)
            last_seen_id = mention.id
            print(mention.text)
            if "help" in mention.text.lower():
                status = '@' + mention.user.screen_name + " To use this bot, please tweet at YuStockBot '$(stockticker)'.  Example '$AMZN $TSLA $GOOG'"
                try:
                    api.update_status(status=status, in_reply_to_status_id=last_seen_id)
                    return
                except:
                    return
            if "info" in mention.text.lower():
                status = '@' + mention.user.screen_name + " This bot responds with stock information when given one or multiple tickers. Information includes Regular Market Day High, Regular Market Day Low, Fifty Day Average, Price, and Market Time."
                try:
                    api.update_status(status=status, in_reply_to_status_id=last_seen_id)
                    return
                except:
                    return
            if '$' in mention.text:
                x = re.findall("(?<=\$)[A-Za-z]+", mention.text)
                for stock in x:
                    stock = stock.upper()
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
                        status = '@' + mention.user.screen_name + " One or more of your stock tickers are not valid in your tweet...please try again with a valid stock ticker. For help please '@' the bot and type help. For more info please '@' the bot and type info."

                    try:
                        api.update_status(status=status, in_reply_to_status_id=last_seen_id)
                    except:
                        return
            else:
                status = '@' + mention.user.screen_name + " One or more of your stock tickers are not valid in your tweet...please try again with a valid stock ticker. For help please '@' the bot and type help. For more info please '@' the bot and type info."
                try:
                    api.update_status(status=status, in_reply_to_status_id=last_seen_id)
                except:
                    return

    return

while True:
    replyStock()
    time.sleep(15)