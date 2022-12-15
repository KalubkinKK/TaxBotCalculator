from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
# from states.user_states import UserStates
import calendar
from datetime import date
import emoji


def legal_form_choise():
    choise = InlineKeyboardMarkup(row_width=2)
    choise.add(
        InlineKeyboardButton(text="ИП", callback_data=1),
        InlineKeyboardButton(text="ООО", callback_data=2)
    )
    return choise


def tax_type_keyboard():
    choise = InlineKeyboardMarkup(row_width=1)
    choise.add(
        InlineKeyboardButton(text="Классическая система", callback_data=1),
        InlineKeyboardButton(text="УСН 6%", callback_data=2),
        InlineKeyboardButton(text="УСН 15%", callback_data=3)
    )
    return choise


def value_added_menu_keyboard():
    choise = InlineKeyboardMarkup(row_width=2)
    choise.add(
        InlineKeyboardButton(text="Да", callback_data=1),
        InlineKeyboardButton(text="Нет", callback_data=2)
    )
    return choise


def default_keyboard():
    choise = InlineKeyboardMarkup()
    choise.add(
        InlineKeyboardButton(
            text=f"ПРИСТУПИТЬ К РАСЧЕТАМ{emoji.emojize(':money_with_wings:')}", callback_data='/counter'
        ),
    )
    return choise


__all__ = [
    "legal_form_choise",
    "tax_type_keyboard",
    "value_added_menu_keyboard",
    "default_keyboard"
]
