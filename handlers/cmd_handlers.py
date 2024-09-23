import re

import requests
import asyncio

from datetime import datetime, timedelta
from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InputFile
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import time

from config import DB_NAME
from handlers.state.user_state import HamsterState
from keybords.inleniekeybor import hamster_inline_keyboard
from utils.database import Database

cmd_router = Router()
db = Database(DB_NAME)


@cmd_router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    try:
        # print(message.text.split()[1])  # referal
        await message.answer(
            text=f"<a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a> xush kelibsiz!\n"
                 f"O'zinggizga kerak viloyatmi tanlang")
    except Exception as e:
        print(e)


@cmd_router.message(Command('hamster'))
async def tanalsh_func(message: Message, state: FSMContext):
    url = (r'https://digitalninja.ru/hamster')    # Send a GET request to the URL

    response = requests.get(url)

    # Parse HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    # print(soup)
    divs = soup.find_all('div', class_='promo-item__name')
    div_texts = [div.get_text(strip=True) for div in divs]
    await message.answer(text='Tanlang:', reply_markup=hamster_inline_keyboard(div_texts))
    await state.set_state(HamsterState.tanalsh)
    # ChromeDriver yo'lini ko'rsating


@cmd_router.callback_query(HamsterState.tanalsh)
async def hamster_loading(cb_query: CallbackQuery, state: FSMContext):
    driver_service = Service(executable_path=r'C:\webdriver\chromedriver.exe')  # Bu joyni to'g'rilang
    driver = webdriver.Chrome(service=driver_service)
    # Sahifani ochish
    driver.get('https://digitalninja.ru/hamster')

    # Tugmani bosishdan oldin holatni olish
    time.sleep(3)  # 3 soniya kutish (sahifa yuklanishi uchun)

    # Ma'lumotlarni olish
    list_button = []
    buttons = driver.find_elements(By.CLASS_NAME, 'promo-item.content-wrapper')
    for number, item in enumerate(buttons):
        if number == int(cb_query.data):
            item.click()
    # Tugmani bosish
    # button = driver.find_element(By.CLASS_NAME, 'promo-item.content-wrapper')
    # button.click()

    for _ in range(3):
        warning_buttons = driver.find_elements(By.CLASS_NAME, 'btn.btn_warning')
        for warning_button in warning_buttons:
            warning_button.click()
            time.sleep(1)
    # Tugmani bosgandan keyin sahifa o'zgarishi uchun kutish
    time.sleep(300)
    promo_cods = driver.find_elements(By.CLASS_NAME, 'promo-code__text')
    for promo_cod in promo_cods:
        print(promo_cod.text)
        await cb_query.bot.send_message(text=promo_cod.text, chat_id=cb_query.from_user.id)
    # Tugmani bosgandan keyingi holatni olish

    driver.quit()  # Brauzerni yopish

    # url = (r'https://digitalninja.ru/hamster')    # Send a GET request to the URL
    #
    # response = requests.get(url)
    #
    # # Parse HTML content
    # soup = BeautifulSoup(response.content, 'html.parser')
    # # print(soup)
    # button = soup.find_all('button', class_='promo-item content-wrapper')

    # await message.answer(text=f"https://t.me/math_hard_bot?start={message.from_user.id}") # referal
#
# @cmd_router.callback_query(Test.Game)
# async def get_category(cb_query: CallbackQuery, state: FSMContext):
#     await state.update_data(region=cb_query.data)
#     if cb_query.data == '1':
#         await cb_query.bot.edit_message_text(
#             text='Toifani belgilang', chat_id=cb_query.from_user.id, message_id=cb_query.message.message_id,
#             reply_markup=get_category_markup())
#     else:
#         await cb_query.bot.edit_message_text(
#             text='Toifani belgilang', chat_id=cb_query.from_user.id, message_id=cb_query.message.message_id,
#             reply_markup=get_category_markup2())
#     await state.set_state(Test.Game1)
#
#
# @cmd_router.callback_query(Test.Game1)
# async def handle_callback_query(cb_query: CallbackQuery, state: FSMContext):
#     if cb_query.data == 'back':
#         await cb_query.bot.edit_message_text(
#             text="O'zinggizga kerak viloyatni tanlang",
#             chat_id=cb_query.from_user.id,
#             message_id=cb_query.message.message_id,
#             reply_markup=get_region_list())
#         await state.set_state(Test.Game)
#     else:
#         await state.update_data(toifa=cb_query.data)
#         await cb_query.bot.edit_message_text(
#             text='qancha kun ?',
#             chat_id=cb_query.from_user.id,
#             message_id=cb_query.message.message_id,
#             reply_markup=days_markup()
#         )
#         await state.set_state(Test.Game2)
#
#
# @cmd_router.callback_query(Test.Game2)
# async def send_message(cb_query: CallbackQuery, state: FSMContext):
#     if cb_query.data == 'back':
#         await cb_query.bot.edit_message_text(
#             text='Toifani belgilang', chat_id=cb_query.from_user.id, message_id=cb_query.message.message_id,
#             reply_markup=get_category_markup() if int(
#                 (await state.get_data())['region']) == 1 else get_category_markup2())
#         await state.set_state(Test.Game1)
#     else:
#         # ---------------DATA------------
#         all_data = await state.get_data()
#         reg_id = int(all_data['region'])
#         toifa = all_data['toifa']
#         days = int(cb_query.data)
#         # --------------- DATE ---------------
#         sana = datetime.now() + timedelta(days=days)
#         sana_str = sana.strftime('%d-%m-%Y')
#         # ------------------------------------
#         price_list = price_shahar if reg_id == 1 else price_viloyat
#         reg_type = toshkent if reg_id == 1 else others
#         toifa_narxi = price_list[price_list.index(int(toifa))]
#
#         await state.clear()
#         await cb_query.message.delete()
#         text = (f"<b>Бугун: {sana_str}</b>  \n\n"
#                 f"💸:<b>{reg_type[toifa_narxi]['crl']} \n\n Худуд: {regions[reg_id - 1]}</b>\n\n")
#         all_data = db.get_numbers_reg_price(reg_id, toifa)
#         len_data = sikl_data(len(all_data))
#         qwerty = len_data
#         for i, number in enumerate(all_data):
#             if i % 2 == 1:
#                 text += f"  <b>{reg_type[toifa_narxi]['sticker']}  {number[5]}</b>\n"
#             else:
#                 text += f"<b>{number[5]}</b>"
#             if i == len_data:
#                 len_data += qwerty
#                 await cb_query.bot.send_message(text=text, chat_id=cb_query.from_user.id)
#                 text = (f"<b>Бугун: {sana_str}</b>  \n\n"
#                         f"💸:<b>{reg_type[toifa_narxi]['crl']} \n\n Худуд: {regions[reg_id - 1]}</b>\n\n")
#         if len(all_data) % qwerty != 0:
#             await cb_query.bot.send_message(text=text, chat_id=cb_query.from_user.id)
#
#
#
#
# @cmd_router.message()
# async def test_1(message: Message):
#     for i in message:
#         print(i)
#     region_id = message.text[0:2]
#     number = message.text[3:11]
#     data = db.search_number(region_id, number)
#     if data:
#         await message.answer(text=f"{regions[int(data[1]) - 1]}\n"
#                                   f"<a href='https://avtoraqam.uzex.uz/ru/lot/item/{data[2]}'>lot number</a>: {data[2]}\n"
#                                   f"{data[3]}\n"
#                                   f"{data[4]} {data[5]}\n"
#                                   f"{data[6]} so'm\n"
#                                   f"{data[7]} {data[8]}")
#     else:
#         await message.answer(text=f"'{message.text}' Bunday nomer topilmadi iltimos nomer shunaqa xolatda "
#                                   f"bo'lsin\nNamuna:01 A 001 AA")
