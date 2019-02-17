#!/usr/bin/env python
"""Colette games."""

import sqlite3
import re
from telegram import ParseMode


class Games:
    """Colette games."""

    def __init__(self, db='quipper', testing=False):
        """Game class, for things liek buzzwords."""
        self.testing = testing
        self.db = db
        if testing:
            self.db += "_test"

    def backup(self, table=None, values={None: None}):
        """Backup game data to table."""

    def rehash(self, table):
        """Rehash from the DB."""
        # Return fetchall of SELECT * FROM table
        with sqlite3.connect(self.db) as c:
            cur = c.cursor()
            cur.execute("SELECT * FROM {0}".format(table))
            return cur.fetchall()

    def handler(self, bot, update):
        """Handle incoming requests."""

    def emote(self, bot, update):
        """Do an emote."""
        room = update.message.chat.id
        text = ' '.join(update.message.text.split()[1:])
        username = update.message.from_user.username
        bot.sendMessage(room, text=f"<i>@{username} {text}</i>",
                        parse_mode=ParseMode.HTML)


def escape_markdown(text):
    """Escape telegram markup symbols."""
    escape_chars = r'\*_`\['
    return re.sub(r'([%s])' % escape_chars, r'\\\1', text)
