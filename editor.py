import asyncio
import os
import os.path
import numpy as np
import cv2
import sys
from PIL import Image

from aiogram.client import bot
import logging
import json
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, CommandObject, Text
from aiogram.enums import ParseMode
from aiogram.types import URLInputFile, InlineKeyboardMarkup, InlineKeyboardButton, InputFile, FSInputFile, CallbackQuery


API_TOKEN = '...'  # هنا تضع الرمز السري الخاص بك. يمكنك معرفته من خلال @BotFather
JSON_FILE = 'photos.json'
logging.basicConfig(level = logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# الأزرار الرئيسية لكل وظيفة
main_buttons = [
        [
            types.InlineKeyboardButton(text = "🖍 الألوان", callback_data = "btn_colors"), 
            types.InlineKeyboardButton(text = "🗂 الفلتر", callback_data = "btn_filter")
        ],
        [
            types.InlineKeyboardButton(text = "⚙️ الإعدادات", callback_data = "btn_settings"),  
            types.InlineKeyboardButton(text = "📐 التدوير", callback_data = "btn_rotate")
        ],
        [
            types.InlineKeyboardButton(text = "📥 التحميل", callback_data = "btn_download")
        ]
    ]
main_keyboard = types.InlineKeyboardMarkup(inline_keyboard = main_buttons)

colors_buttons = [
        [
            types.InlineKeyboardButton(text = "أصفر", callback_data = "btn_yellow"), 
            types.InlineKeyboardButton(text = "أحمر", callback_data = "btn_red")
        ],
        [
            types.InlineKeyboardButton(text = "أزرق", callback_data = "btn_blue"), 
            types.InlineKeyboardButton(text = "أخضر", callback_data = "btn_green")
        ],
        [
            types.InlineKeyboardButton(text = "📚 القائمة الرئيسية", callback_data = "btn_main_menu")
        ]
    ]
colors_keyboard = types.InlineKeyboardMarkup(inline_keyboard = colors_buttons)

filter_buttons = [
        [
            types.InlineKeyboardButton(text = "HDR", callback_data = "btn_hdr"), 
            types.InlineKeyboardButton(text = "سبييا", callback_data = "btn_sepia")
        ],
        [
            types.InlineKeyboardButton(text = "درجات الرمادي", callback_data = "btn_grey"), 
            types.InlineKeyboardButton(text = "العكس", callback_data = "btn_invert")
        ],
        [
            types.InlineKeyboardButton(text = "📚 القائمة الرئيسية", callback_data = "btn_main_menu")
        ]
]
filter_keyboard = types.InlineKeyboardMarkup(inline_keyboard = filter_buttons)

settings_buttons = [
        [
            types.InlineKeyboardButton(text = "السطوع", callback_data = "btn_brightness"), 
            types.InlineKeyboardButton(text = "التباين", callback_data = "btn_contrast")
        ],
        [
            types.InlineKeyboardButton(text = "الإشباع", callback_data = "btn_saturation"), 
            types.InlineKeyboardButton(text = "الحواف", callback_data = "btn_edge")
        ],
        [
            types.InlineKeyboardButton(text = "📚 القائمة الرئيسية", callback_data = "btn_main_menu")
        ]
    ]
settings_keyboard = types.InlineKeyboardMarkup(inline_keyboard = settings_buttons)

rotate_buttons = [
        [
            types.InlineKeyboardButton(text = "90°", callback_data = "btn_90"), 
            types.InlineKeyboardButton(text = "-90°", callback_data = "btn_minus_90")
        ],
        [
            types.InlineKeyboardButton(text = "180°", callback_data = "btn_180"), 
            types.InlineKeyboardButton(text = "-180°", callback_data = "btn_minus_180")
        ],
        [
            types.InlineKeyboardButton(text = "📚 القائمة الرئيسية", callback_data = "btn_main_menu")
        ]
    ]
rotate_keyboard = types.InlineKeyboardMarkup(inline_keyboard = rotate_buttons)

download_buttons = [
        [
            types.InlineKeyboardButton(text = "PNG", callback_data = "btn_png"), 
            types.InlineKeyboardButton(text = "JPG", callback_data = "btn_jpg")
        ],
        [
            types.InlineKeyboardButton(text = "WEbP", callback_data = "btn_webp"),  
            types.InlineKeyboardButton(text = "TIFF", callback_data = "btn_tiff")
        ],
        [
            types.InlineKeyboardButton(text = "📚 القائمة الرئيسية", callback_data = "btn_main_menu")
        ]
    ]
download_keyboard = types.InlineKeyboardMarkup(inline_keyboard = download_buttons)


# تحميل البيانات من ملف JSON
def load_data():
    try:
        with open(JSON_FILE, 'r', encoding='utf-8') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


# حفظ البيانات في ملف JSON
def save_data(data):
    with open(JSON_FILE, 'w', encoding='utf-8') as file:
        json.dump(data, file)


chat_counts = load_data()


# الأوامر الرئيسية للبوت
@dp.message(Command(commands = ['start']))
async def cmd_start(message: types.Message):
    await message.answer('🖼 <b>بوت تعديل الصور</b> — هو <b>أداة مريحة</b> لتحرير <b>صورك</b> بسرعة وجودة في <b>تليجرام</b>. <b>بفضل</b> هذا <b>البوت</b>, يمكنك <b>تحويل</b> صورك العادية إلى <b>تحف فنية</b> في <b>بضع خطوات</b>. \n\n📚 <b>الوظائف الرئيسية</b>: \n\n✂️ القص؛ \n🗂 الفلتر؛ \n⚙️ الإعدادات؛ \n📐 التدوير.\n\n🗒 <b>أوامر البوت</b>:\n\n🖥 تشغيل البوت - <b>/start</b>\n⁉️ الدعم الفني - <b>/help</b>\n\n⚠️ <b>للتعديل أرسل صورة (وليس مستندًا)</b>')

@dp.message(Command(commands = ['help']))
async def cmd_help(message: types.Message):
    await message.answer("⁉️<b> إذا كنت تواجه مشاكل.</b> \n"
                         "✉️ <b>اتصل بي على</b> <a href = 'https://t.me/nikit0ns'>@nikit0ns</a><b>.</b>", 
                         disable_web_page_preview = True)

@dp.message(F.photo)
async def handle_message(message: types.Message, state):
    data = await state.get_data()
    if data.get("last_message_id"):
        try:
            await bot.delete_message(chat_id=message.chat.id, message_id=data.get("last_message_id"))
        except:
            pass    
        
    chat_id = str(message.chat.id)  # المفاتيح في ملف JSON يجب أن تكون على شكل سلاسل نصية
    if chat_id not in chat_counts:
        chat_counts[chat_id] = {"photo": None, "last_msg_id": None}
    
    if chat_counts[chat_id]["last_msg_id"]:
        try: 
            os.remove(chat_counts[chat_id]["photo"])
        except Exception as e:
            print(e)

    path = f"{message.from_user.id}.jpg"
    await bot.download(
        message.photo[-1],
        destination=path
    )

    image = FSInputFile(
        path=path
    ) 
    sent_message =  await bot.send_photo(chat_id, photo = image,parse_mode = ParseMode.MARKDOWN, reply_markup = main_keyboard)
    chat_counts[chat_id]["last_msg_id"] = sent_message.message_id
    chat_counts[chat_id]["photo"] = path
    save_data(chat_counts)
    await state.update_data(last_message_id = sent_message.message_id)
    await message.delete()

# متابعة باقي الكود من حيث الترجمة للأوامر والأزرار.
