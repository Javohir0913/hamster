from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def hamster_inline_keyboard(items: list) -> InlineKeyboardMarkup:
    rows = []
    row = []
    for number, item in enumerate(items):
        date = InlineKeyboardButton(text=item, callback_data=f"{number}")
        row.append(date)
        if number % 2 == 1 and number != 0:
            rows.append(row)
            row = []
    if row:
        rows.append(row)
    markup = InlineKeyboardMarkup(inline_keyboard=rows)

    return markup
