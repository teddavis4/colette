#!/usr/bin/env python
"""Utilities for colette."""

from concurrent.futures import ThreadPoolExecutor
import time
from isodate import parse_duration
import traceback
import sqlite3


class Util:
    """Colette utilities."""

    def __init__(self, testing=False):
        """Util functions."""
        self.executor = ThreadPoolExecutor(max_workers=500)

    def _reminder(self, sendMessage, chat_id, text,
                  text_date, user, future_date):
        """Reminder function.

        meant to run in a thread this function will monitor the current time
        until future_date is reached at which point the reminder will be
        relayed to the user.
        """
        try:
            seconds = parse_duration("PT" + future_date.upper()).seconds
            future_date = time.time() + seconds

            while time.time() < future_date:
                time.sleep(0.15)
            remind_text = "@{0} Here is your reminder:\n\n{1}".format(
                user, text)
            print(remind_text)
            sendMessage(chat_id, text=remind_text)
        except Exception:
            traceback.print_exc()

    def remind(self, bot, update):
        """Set a reminder in the future."""
        text = update.message.text
        future_date = text.split(" ", 2)[1]
        text = text.split(" ", 2)[2]
        text_date = update.message.date
        username = update.message.from_user.username
        chat_id = update.message.chat_id
        self.executor.submit(self._reminder, bot.sendMessage, chat_id, text,
                             text_date, username, future_date)
        bot.sendMessage(chat_id, text="Your reminder has been set for {} from "
                        "now".format(future_date))

    def everyone(self, bot, update):
        """Message everyone in the room."""
        users = None
        room = update.message.chat.id
        text = ' '.join(update.message.text.split()[1:])
        username = update.message.from_user.username
        with sqlite3.connect('everyone') as conn:
            c = conn.cursor()
            c.execute("select username from users where room=?", (room,))
            users = c.fetchall()
        user_list = f''
        for user in users:
            user_list += f'@{user[0]} '
        message = f'[from @{username}] {user_list} {text}'
        bot.sendMessage(room, text=message)

    def spam_me(self, bot, update):
        """Add user to everyone list."""
        username = update.message.from_user.username
        room = update.message.chat.id
        with sqlite3.connect('everyone') as conn:
            c = conn.cursor()
            c.execute("select username from users where username=? and room=?",
                      (username, room))
            if c.fetchall():
                return
            c.execute("insert into users (username, room) values (?, ?)",
                      (username, room))
            conn.commit()
        bot.sendMessage(room, text="you asked for this")

    def free_me(self, bot, update):
        """Free yourself of spam."""
        username = update.message.from_user.username
        room = update.message.chat.id
        with sqlite3.connect('everyone') as conn:
            c = conn.cursor()
            c.execute("delete from users where username=? and room=?",
                      (username, room))
            conn.commit()
        bot.sendMessage(room, text="you have reached nirvana")

    def feedback(self, bot, update):
        """Give the author feedback."""
        username = update.message.from_user.username
        channel = update.message.chat.title
        room = update.message.chat.id
        feedback = ' '.join(update.message.text.split()[1:])
        with sqlite3.connect('feedback') as conn:
            c = conn.cursor()
            c.execute("insert into feedback (username, room, feedback) values "
                      "(?, ?, ?)", (username, channel, feedback))
            conn.commit()
        bot.sendMessage(room, text="Your feedback was received")
