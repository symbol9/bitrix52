import logging

from aiogram import Bot
from aiogram import Router, F
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, default_state, State
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Message, CallbackQuery
from redis.asyncio.client import Redis

from config.config import load_config
from keyboards.keyboards import (phone_kb, fill_form_kb, cancel_btn_kb)
from lexicon.lexicon import LEXICON
from work_with_leads.add_lead import create_lead

logger = logging.getLogger(__name__)

config = load_config()

redis = Redis(host='localhost')

storage = RedisStorage(redis=redis)

webhook_url = config.webhooks.webhook
webhook_url2 = config.webhooks.webhook2


async def lead_data_f(redis):
    # Получаем данные из Redis
    name = await redis.get('lead_name')
    phone_number = await redis.get('lead_phone_number')
    email = await redis.get('lead_email')
    message = await redis.get('lead_message')

    # Строим словарь данных лида
    lead_data = {
        'fields': {
            "NAME": name,
            "STATUS_ID": "NEW",
            "OPENED": "Y",
            "ASSIGNED_BY_ID": 1,
            "PHONE": [{"VALUE": phone_number,
                       "VALUE_TYPE": "WORK"}],
            "EMAIL": [{"VALUE": email,
                       "VALUE_TYPE": "WORK"}],
            "COMMENTS": message
        },
        'params': {
            "REGISTER_SONET_EVENT": "Y"
        }
    }
    return lead_data


def convert_bytes_to_str(data):
    for key, value in data.items():
        if isinstance(value, bytes):
            data[key] = value.decode()
        elif isinstance(value, dict):
            convert_bytes_to_str(value)
        elif isinstance(value, list):
            for item in value:
                convert_bytes_to_str(item)

    return data


bot = Bot(token=config.tg_bot.token)
router = Router()


class FSMFillForm(StatesGroup):
    fill_name = State()
    fill_phone_number = State()
    fill_email = State()
    fill_message = State()


@router.message(CommandStart(), StateFilter(default_state))
async def start_command(message: Message):
    user_id = message.from_user.id

    with open('ids.txt', 'r+') as file:
        existing_ids = file.read().splitlines()
        if str(user_id) not in existing_ids:
            await message.answer(text=f'Привет, {message.from_user.first_name}!\n\n'
                                      f'Я - Нейросетевой бот компании Stroika и я'
                                      f' помогу тебе узнать об услугах нашей компании!\n'
                                      f'Когда будете готовы к приобретению ***,'
                                      f' можете заполнить анкету и обратиться к нам за более подробной консультацией,',
                                 reply_markup=fill_form_kb())
            await message.answer('Если клавиатура не открылась - действуйте по инструкции ниже')
            photo = 'https://avatars.mds.yandex.net/get-images-cbir/2203007/cROjPWcVCuSiB56otJBaig936/ocr'
            await bot.send_photo(chat_id=message.from_user.id, photo=photo)

        else:
            await message.answer(f"Привет, {message.from_user.first_name}!\n\n"
                                 f"Я твой нейросетевой помощник, спрашивай все что захочешь о нашей компании,"
                                 f" я постараюсь оответить!")


@router.message(F.text == 'Заполнить анкету📝', StateFilter(default_state))
async def fillform_command(message: Message, state: FSMContext):
    keyboard = phone_kb()
    cancel_keyboard = cancel_btn_kb()
    await message.answer(text=LEXICON['fillform'],
                         reply_markup=keyboard)
    await message.answer(text=LEXICON['cancel'],
                         reply_markup=cancel_keyboard)
    await state.set_state(FSMFillForm.fill_phone_number)


@router.message(F.contact, StateFilter(FSMFillForm.fill_phone_number))
async def filling_phone_number(message: Message, state: FSMContext):
    phone_number = message.contact.phone_number
    await state.update_data(phone_number=phone_number)
    await redis.set('lead_phone_number', phone_number)
    cancel_keyboard = cancel_btn_kb()
    await message.answer(text=LEXICON['phone_number_filled'],
                         reply_markup=cancel_keyboard)
    await state.set_state(FSMFillForm.fill_name)


@router.callback_query(F.data == 'cancel_fill_form_pressed', StateFilter(FSMFillForm.fill_phone_number))
async def cancel_fill_form_pressed(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(LEXICON['cancel_filling'])
    await state.clear()


@router.message(StateFilter(FSMFillForm.fill_phone_number))
async def filling_phone_number_error(message: Message):
    await message.answer(LEXICON['filling_phone_number_error'])


@router.message(StateFilter(FSMFillForm.fill_name))
async def process_name(message: Message, state: FSMContext):
    await redis.set('lead_name', message.text)
    await message.answer("Введите ваш email:")
    await state.set_state(FSMFillForm.fill_email)


@router.message(StateFilter(FSMFillForm.fill_email), lambda x: '@' in x.text)
async def filling_mail(message: Message, state: FSMContext):
    await state.update_data(email=message.text)
    await redis.set('lead_email', message.text)
    await message.answer(text=LEXICON['email_filled'])
    await state.set_state(FSMFillForm.fill_message)


@router.callback_query(F.data == 'cancel_fill_form_pressed', StateFilter(FSMFillForm.fill_email))
async def cancel_fill_form_pressed(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(LEXICON['cancel_filling'])
    await state.clear()


@router.message(StateFilter(FSMFillForm.fill_email))
async def filling_mail_error(message: Message):
    await message.answer(LEXICON['filling_mail_error'])


@router.message(StateFilter(FSMFillForm.fill_message))
async def process_message(message: Message, state: FSMContext):
    user_id = message.from_user.id
    with open('ids.txt', 'r+') as file:
        file.write(f'{str(user_id)}\n')

    await redis.set('lead_message', message.text)
    data = await lead_data_f(redis)
    new_data = convert_bytes_to_str(data)
    logger.info(msg=new_data)

    # Вызываем функцию для создания лида (нужно определить функцию create_lead)
    await create_lead(webhook_url, new_data)
    # Очищаем данные из Redis
    await redis.delete('lead_name', 'lead_phone_number', 'lead_email', 'lead_message')
    await state.clear()
    await message.answer("Спасибо, ваша заявка принята!\n\n"
                         "На указаный вами номер будет отправлено сообщение с чатом для дальнейшей консультации,"
                         "либо просто перейдите по ссылке @Openai_stroika_bot")
