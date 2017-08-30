#!/usr/bin/env python

import sqlite3
from telegram.ext.dispatcher import run_async
import urllib.parse
import requests
from yahoo_finance import Share
from google import google

from auth import Auth

TEST=True
auth = Auth(testing=TEST)

class Search:
    def __init__(self, testing=False):
        """ Do searches for things (google, stocks, images, etc) """
    @run_async
    def get_ifl_link(self, bot, update):
        query = update.message.text.split(' ', 1)[1]
        search_results = google.search(query)
        result = search_results[0]
        bot.sendMessage(update.message.chat_id, text=result.link)

    @auth.needadmin
    def get_stock(self, bot, update):
        """ Get stock quotes """
        line_s = update.message.text.split()
        ticker = line_s[1].upper()
        yahoo = Share(ticker.upper())
        last_price = yahoo.get_price()
        last_time = yahoo.get_trade_datetime()
        div = yahoo.get_dividend_yield()
        bot.sendMessage(update.message.chat_id, "[{0}] ${1} @{2} ({3})".format(ticker,
            last_price, last_time, div))

    def search(self, bot, update):
        query = update.message.text.split(' ', 1)[1]
        if len(query)<=2:
            bot.sendMessage(update.message.chat_id, text="You gotta ask for a book")
        #return str(find_book(query))
        book_results = find_book(query)
        msg_reply = '\n'.join(book_results.split('\n')[:3])
        bot.sendMessage(update.message.chat_id, text=str(msg_reply))

