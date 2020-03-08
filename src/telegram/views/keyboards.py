from telegram import InlineKeyboardButton, InlineKeyboardMarkup


# Callback data
ONE, TWO, THREE, FOUR, FIVE, SIX = range(6)


def start_markup():
    # Build InlineKeyboard where each button has a displayed text
    # and a string as callback_data
    # The keyboard is a list of button rows, where each row is in turn
    # a list (hence `[[...]]`).
    keyboard = [
        [InlineKeyboardButton("Yes", callback_data=str(ONE)),
         InlineKeyboardButton("No", callback_data=str(TWO))]
    ]
    return InlineKeyboardMarkup(keyboard)


def joke_markup():
    # Build InlineKeyboard where each button has a displayed text
    # and a string as callback_data
    # The keyboard is a list of button rows, where each row is in turn
    # a list (hence `[[...]]`).
    keyboard = [
        [InlineKeyboardButton("1", callback_data="j" + str(ONE)),
         InlineKeyboardButton("2", callback_data="j" + str(TWO)),
         InlineKeyboardButton("3", callback_data="j" + str(THREE)),
         InlineKeyboardButton("4", callback_data="j" + str(FOUR)),
         InlineKeyboardButton("5", callback_data="j" + str(FIVE))],
        [InlineKeyboardButton("Offensive", callback_data="j" + str(SIX))]
    ]
    return InlineKeyboardMarkup(keyboard)
