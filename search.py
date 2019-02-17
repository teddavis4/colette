#!/usr/bin/env python
"""Colette search."""

from telegram.ext.dispatcher import run_async
from yahoo_finance import Share
from google import google


class Search:
    """Do searches for things (google, stocks, images, etc)."""

    def __init__(self, testing=False):
        """Assign variables."""
        self.testing = testing

    @run_async
    def get_ifl_link(self, bot, update):
        """Get I'm feeling lucky link."""
        query = update.message.text.split(' ', 1)[1]
        search_results = google.search(query)
        result = search_results[0]
        bot.sendMessage(update.message.chat_id, text=result.link)

    def get_stock(self, bot, update):
        """Get stock quotes."""
        line_s = update.message.text.split()
        ticker = line_s[1].upper()
        yahoo = Share(ticker.upper())
        last_price = yahoo.get_price()
        last_time = yahoo.get_trade_datetime()
        div = yahoo.get_dividend_yield()
        bot.sendMessage(update.message.chat_id, "[{0}] ${1} @{2} "
                        "({3})".format(ticker, last_price, last_time, div))
