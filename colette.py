#!/usr/bin/env python
"""Colette."""


from uuid import uuid4

import re

from telegram import InlineQueryResultArticle, ParseMode, \
    InputTextMessageContent
from telegram.ext import (Updater, InlineQueryHandler, CommandHandler, Filters,
                          MessageHandler)
import logging
import string
from telegram.ext.dispatcher import run_async
from quip import Quip
from util import Util
from user import User
from games import Games
from search import Search

TEST = False

user = User(testing=TEST)

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - '
                    '%(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.


def start(bot, update):
    """Ensure bot is started."""
    bot.sendMessage(update.message.chat_id, text='Hi!')


def help(bot, update):
    """Print help."""
    with open('help_message') as f:
        bot.sendMessage(update.message.chat_id, text=f.read())


@run_async
def math(bot, update):
    """Do math."""
    text = update.message.text.split()
    try:
        if len([g for g in text[1] if g in string.ascii_letters]) > 0:
            raise
        math_result = eval(text[1])
    except Exception:
        math_result = 0
    bot.sendMessage(update.message.chat_id, text=math_result)


def channel_logger(bot, update):
    """Quip store."""
    # time_or_times = 'times'
    global buzzwords
    global words
    games = Games()
    id = update.message.from_user.id
    text = update.message.text
    text_date = update.message.date
    username = update.message.from_user.username
    channel = update.message.chat.title
    if text[0:2] == 'e ' or text[0:2] == 'E ':
        return games.emote(bot, update)
    # output = '@{} has said '.format(username)
    user.check_user_exist(id, username)
    # for word in words:
    #    lc_text = text.lower()
    #    if word in text.lower():
    #        c = len(lc_text.split(word))-1
    #        # Reply with the count of gays.
    #        if word not in buzzwords.keys():
    #            buzzwords[word] = {}
    #        gaycount = buzzwords[word].setdefault(username, 0) + c
    #        if gaycount == 1:
    #            time_or_times = 'time'
    #        buzzwords[word][username] += c
    #        if 'time' in output:
    #            output += "; '{}' {} {}".format(word, gaycount, time_or_times)
    #        else:
    #            output += "'{}' {} {}".format(word, gaycount, time_or_times)
    # if 'time' in output:
    #    bot.sendMessage(update.message.chat_id, text="{}"
    #            " this session".format(output))
    with open('telegram_log', 'a') as f:
        f.write('{0} ({1}) [{2}]: {3}\n'.format(text_date, channel, username,
                                                text))


def escape_markdown(text):
    """Escape telegram markup symbols."""
    escape_chars = r'\*_`\['
    return re.sub(r'([%s])' % escape_chars, r'\\\1', text)


def inlinequery(bot, update):
    """Do inlinequery."""
    query = update.inline_query.query
    results = list()

    results.append(
        InlineQueryResultArticle(
            id=uuid4(),
            title="Caps",
            input_message_content=InputTextMessageContent(
                query.upper())))

    results.append(
        InlineQueryResultArticle(
            id=uuid4(),
            title="Bold",
            input_message_content=InputTextMessageContent(
                "*%s*" %
                escape_markdown(query),
                parse_mode=ParseMode.MARKDOWN)))

    results.append(
        InlineQueryResultArticle(
            id=uuid4(),
            title="Italic",
            input_message_content=InputTextMessageContent(
                "_%s_" %
                escape_markdown(query),
                parse_mode=ParseMode.MARKDOWN)))

    bot.answerInlineQuery(update.inline_query.id, results=results)


def error(bot, update, error):
    """Output errors."""
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def read_config(testing=False):
    """Read configuration."""
    config = 'colette_config'
    if testing:
        config += '_test'
    with open(config, 'r') as f:
        return f.read().strip()


def main():
    """Main."""
    global buzzwords
    global words

    quip = Quip(user, testing=TEST)
    util = Util()

    search = Search()

    words = ['gay', 'something something', 'nigger', 'i mean', 'guttersnipe',
             'jesus edwin', '😢']
    buzzwords = {}
    # Create the Updater and pass it your bot's token.
    token = read_config(testing=TEST)
    updater = Updater(token)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    # dp.add_handler(CommandHandler("register", register))
    # dp.add_handler(CommandHandler("bemail", email))
    # dp.add_handler(CommandHandler("bsearch", search))
    dp.add_handler(CommandHandler("google", search.get_ifl_link,
                                  allow_edited=True))
    dp.add_handler(CommandHandler("Google", search.get_ifl_link,
                                  allow_edited=True))
    dp.add_handler(CommandHandler("quote", quip.quipper))
    dp.add_handler(CommandHandler("quip", quip.quipper))
    dp.add_handler(CommandHandler("getq", quip.get_quote))
    dp.add_handler(CommandHandler("getquote", quip.get_quote))
    dp.add_handler(CommandHandler("delquote", quip.delete_quote_by_id))
    dp.add_handler(CommandHandler("math", math))
    dp.add_handler(CommandHandler("seve_pikjur", quip.seve_pikjur))
    dp.add_handler(CommandHandler("seve", quip.seve_pikjur))
    dp.add_handler(CommandHandler("save", quip.seve_pikjur))
    dp.add_handler(CommandHandler("get", quip.get_pikjur))
    dp.add_handler(CommandHandler("git", quip.get_pikjur))
    dp.add_handler(CommandHandler("stock", search.get_stock))
    dp.add_handler(CommandHandler("remindme", util.remind))
    dp.add_handler(CommandHandler("remind", util.remind))
    dp.add_handler(CommandHandler("rem", util.remind))
    dp.add_handler(CommandHandler("free_me", util.free_me))
    dp.add_handler(CommandHandler("spam_me", util.spam_me))
    dp.add_handler(CommandHandler("everyone", util.everyone))
    dp.add_handler(CommandHandler("feedback", util.feedback))
    # dp.add_handler(CommandHandler("restart", restart_git))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(InlineQueryHandler(inlinequery))

    # log all errors
    dp.add_error_handler(error)

    # Add message handler for quips!
    # dp.add_handler(MessageHandler([Filters.text], quipper))
    dp.add_handler(MessageHandler(Filters.text, channel_logger))

    # Start the Bot
    updater.start_polling()

    # Block until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
