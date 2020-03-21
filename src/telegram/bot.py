#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Inline keyboard bot with multiple CallbackQueryHandlers.

"""
import hashlib
import logging
import random
import re

from telegram import ParseMode
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler

from config import MENU_OPTIONS, JOKE, CATEGORIES, SIZES

from controllers.joker import Joker
from views.keyboards import start_markup, joke_markup
from views.messages import start_message

from views.keyboards import ONE, TWO, THREE, FOUR, FIVE, SIX

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

joker = Joker()


def start(update, context):
    """Send message on `/start`."""
    # Get user that sent /start and log his name
    user = update.message.from_user['id']
    context.user_data["this_user"] = hashlib.sha224(user).hexdigest()

    logger.info("User %s started the conversation.", user)

    # Send message with text and appended InlineKeyboard
    update.message.reply_text(
        text=start_message(),
        reply_markup=start_markup(),
        parse_mode=ParseMode.MARKDOWN
    )
    # Tell ConversationHandler that we're in state `MENU_OPTIONS` now
    return MENU_OPTIONS


def joke(update, context):
    """Show new choice of buttons"""
    query = update.callback_query
    bot = context.bot

    selection = query.data
    logger.info(f"Query data: {selection}")
    if re.match(r'^j', selection):
        text = f"{context.user_data['joke']} | {context.user_data['category']} | {selection[1:]}\n"
        with open(f"./data/{context.user_data['this_user']}.txt", "a+") as f:
            f.write(text)
            context.user_data['joke'] = ""
            context.user_data['category'] = ""

    content = random.choice(CATEGORIES)
    size = SIZES[0]

    text = joker.render(types=[size, content])
    context.user_data["category"] = [size, content]
    context.user_data["joke"] = text

    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text=text,
        reply_markup=joke_markup(),
        parse_mode=ParseMode.MARKDOWN
    )
    return JOKE


def end(update, context):
    user_data = context.user_data
    update.message.reply_text("Sorry! Maybe you'll change your mind, see you then!")
    user_data.clear()
    return ConversationHandler.END


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    # Create the Updater and pass it your bot's token.
    from config import API_KEY
    updater = Updater(API_KEY, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Setup conversation handler with the states FIRST and SECOND
    # Use the pattern parameter to pass CallbackQueries with specific
    # data pattern to the corresponding handlers.
    # ^ means "start of line/string"
    # $ means "end of line/string"
    # So ^ABC$ will only allow 'ABC'
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start, pass_job_queue=True, pass_chat_data=True)],
        states={
            MENU_OPTIONS: [CallbackQueryHandler(joke, pattern='^' + str(ONE) + '$'),
                           CallbackQueryHandler(end, pattern='^' + str(TWO) + '$')],

            JOKE: [CallbackQueryHandler(joke, pattern='^' + "j" + str(ONE) + '$'),
                   CallbackQueryHandler(joke, pattern='^' + "j" + str(TWO) + '$'),
                   CallbackQueryHandler(joke, pattern='^' + "j" + str(THREE) + '$'),
                   CallbackQueryHandler(joke, pattern='^' + "j" + str(FOUR) + '$'),
                   CallbackQueryHandler(joke, pattern='^' + "j" + str(FIVE) + '$'),
                   CallbackQueryHandler(joke, pattern='^' + "j" + str(SIX) + '$')]
        },
        fallbacks=[CommandHandler('start', start)]
    )

    # Add ConversationHandler to dispatcher that will be used for handling
    # updates
    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
