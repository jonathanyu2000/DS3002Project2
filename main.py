#Computing ID: jxy7du
#Name: Jonathan Yu

#Worked with Melanie Le on creating initial bot
import tweepy
import time
import requests
import re

#API Tokens for Twitter API
Bearer_Token = "AAAAAAAAAAAAAAAAAAAAAPObWwEAAAAArbgXlkVueEql0%2BTs%2BLHsoKivzlY%3DDV1SqHvUPFNOwefLYdvv24GxTi2aAWBq26oKB6DRm3QmNfNpVv"
Consumer_Key = "ffVjQ5dyx0eiNqMd4Wf24XBGG"
Consumer_Secret = "6QSlsoiBlEHIJkq1RnchjH8EvrFy3sdZKKKgwbe9eVfFncGrPg"
Access_Token = "1470107004706377734-ztbh4KR5OntR1L98um7NQPLauTY36i"
Access_Token_Secret = "wJGQD3yylSz6nszQ91h2WoqEusF468Nm3DUVtp6OwbW4v"

# Authenticate to Twitter - makes sure API keys check out
auth = tweepy.OAuthHandler(Consumer_Key,Consumer_Secret)
auth.set_access_token(Access_Token,Access_Token_Secret)
api = tweepy.API(auth)

try:
    api.verify_credentials()
    print("Authentication works")
except:
    print("Error")


def YahooStockAPI(stocksymbol):
    '''
    :param stocksymbol: stock ticker symbol for Yahoo Finance API
    :return: returns a json structure with all of the information about the stock
    '''
    # API key generated from Yahoo Finance API
    apikey='IFzpK3ZLbd6Eo9iSq2yst2qaT6uiwqj66RyAw99e'
    # URL of Yahoo Finance API
    url = "https://yfapi.net/v6/finance/quote"
    # Assigns symbols as the way to search on API
    querystring = {"symbols": stocksymbol}
    headers = {
        'x-api-key': apikey
    }
    response = requests.get(url, headers=headers, params=querystring)
    return response.json()

# Creates text file to keep track of mentioned ids.
filename = "mentionid.txt"

def replyStock():
    '''
    Main function for the Twitter Bot including responses to help, info, stock ticker, and
    things that do not have a stock-ticker.
    :return: Makes Twitter Bot respond to tweets that it is mentioned in and depending on the content of the tweet,
    the bot will respond a certain way.
    '''
    # Gets latest mention in Twitter timeline from Yahoo API
    mentions = api.mentions_timeline(count=1)
    for mention in reversed(mentions):
        # Opens text document to add last mentions
        mentionfile = open(filename, "a+")
        mentionfile.seek(0, 0)
        # Makes sure to not try and reply to tweets that have already been replied to
        if (str(mention.id)+"\n") in mentionfile.readlines():
            print("Already replied to")
        else:
            mentionfile.write(str(mention.id) + "\n")
            print(str(mention.id) + ' : ' + mention.text)
            last_seen_id = mention.id
            print(mention.text)
            # What the bot should respond with if user tweets help at the bot
            if "help" in mention.text.lower():
                status = '@' + mention.user.screen_name + " To use this bot, please tweet at YuStockBot '$(stockticker)'.  " \
                                                          "Example stock ticker format '$AMZN $TSLA $GOOG'. " \
                                                          "Make sure each stock ticker is separated by a space and preceded by '$'."
                try:
                    api.update_status(status=status, in_reply_to_status_id=last_seen_id)
                    return
                except:
                    return
            # What the bot should respond with if user tweets info at the bot
            if "info" in mention.text.lower():
                status = '@' + mention.user.screen_name + " This bot responds with stock information when given one or multiple tickers. " \
                                                          "Information given includes Regular Market Day High, Regular Market Day Low, Fifty Day Average, Price, and Market Time."
                try:
                    api.update_status(status=status, in_reply_to_status_id=last_seen_id)
                    return
                except:
                    return
            # What the bot should respond with if user tweets a stock ticker at the bot
            if '$' in mention.text:
                # Finds stock ticker from tweet usign RegEx
                x = re.findall("(?<=\$)[A-Za-z]+", mention.text)
                for stock in x:
                    # Capitalize the stock ticker in case it is lowercase
                    stock = stock.upper()
                    try:
                        # Searches stock ticker using YahooStockAPI function and stores json structure into stock_json
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
                        # Attempt to use stock ticker but stock ticker does not exist in Yahoo Finance API
                        status = '@' + mention.user.screen_name + " " + stock + " is not a valid stock ticker in your tweet...please try again with a valid stock ticker. For help please '@' the bot and type help. For more info please '@' the bot and type info."

                    try:
                        api.update_status(status=status, in_reply_to_status_id=last_seen_id)
                    except:
                        return
            # If input is none of the previously assigned ones, then bot responds with this
            else:
                status = '@' + mention.user.screen_name + " One or more of your stock tickers are not valid in your tweet...please try again with a valid stock ticker. For help please '@' the bot and type help. For more info please '@' the bot and type info."
                try:
                    api.update_status(status=status, in_reply_to_status_id=last_seen_id)
                except:
                    return

    return

#Runs the bot
while True:
    replyStock()
    time.sleep(15)