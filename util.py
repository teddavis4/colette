#!/usr/bin/env python

from telegram.ext.dispatcher import run_async
from concurrent.futures import ThreadPoolExecutor
import time
from isodate import parse_duration
import string
import traceback

class Util:
    def __init__(self, testing=False):
        """Util functions"""
        self.executor = ThreadPoolExecutor(max_workers=500)

    def _reminder(self, sendMessage, chat_id, text, text_date, user, future_date):
        """Reminder function; meant to run in a thread this function will
        monitor the current time until future_date is reached at which point
        the reminder will be relayed to the user"""
        try:
            seconds = parse_duration("PT"+future_date.upper()).seconds
            future_date = time.time() + seconds

            while time.time() < future_date:
                time.sleep(0.15)
            remind_text = "@{0} Here is your reminder:\n\n{1}".format(user, text)
            print(remind_text)
            sendMessage(chat_id, text=remind_text)
        except Exception as e:
            traceback.print_exc()

    def remind(self, bot, update):
        """Function to set a reminder in the future"""
        id = update.message.from_user.id
        text = update.message.text
        future_date = text.split(" ", 2)[1]
        text = text.split(" ", 2)[2]
        text_date = update.message.date
        username = update.message.from_user.username
        channel = update.message.chat.title
        chat_id = update.message.chat_id
        self.executor.submit(self._reminder, bot.sendMessage, chat_id, text,
                text_date, username, future_date)
        bot.sendMessage(chat_id, text="Your reminder has been set for {} from now".format(future_date))

