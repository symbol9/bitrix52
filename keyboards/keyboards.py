from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton, ReplyKeyboardMarkup)


def fill_form_kb():
    fill_form_button = KeyboardButton(text='Заполнить анкету📝')
    keyboard = ReplyKeyboardMarkup(keyboard=[[fill_form_button]],
                                   resize_keyboard=True,
                                   one_time_keyboard=True)
    return keyboard


def cancel_btn_kb():
    cancel_fill_form = InlineKeyboardButton(
        text='Отменить❌',
        callback_data='cancel_fill_form_pressed')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[cancel_fill_form]])
    return keyboard


def phone_kb():
    telephone_button = KeyboardButton(
        text='Отправить номер📱',
        request_contact=True
    )
    keyboard = ReplyKeyboardMarkup(keyboard=[[telephone_button]],
                                   resize_keyboard=True,
                                   one_time_keyboard=True)
    return keyboard

