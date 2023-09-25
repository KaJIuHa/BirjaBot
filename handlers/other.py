from aiogram import types
from aiogram.dispatcher.filters import Text

from create_bot import bot, dp
from utils.texts import Desc
from keybords.keyboard import kb_start, sup_kb
from database.user_base import db



async def cmd_start(msg: types.Message):
    """Хендлер команды старт"""
    if db.check_user(msg.from_user.id):
        # await logic.calculation_thread(msg.from_user.id)
        await bot.send_message(msg.from_user.id,
                           text=Desc.start_command(msg.from_user.first_name),
                           reply_markup=kb_start)
    else:
        db.create_user(msg.from_user.id)
        # await logic.calculation_thread(msg.from_user.id)
        await bot.send_message(msg.from_user.id,
                               text=Desc.start_command(msg.from_user.first_name),
                               reply_markup=kb_start)


async def get_id(msg: types.Message):
    """Хендлер инфо ID"""
    await bot.send_message(msg.from_user.id,
                           text=Desc.id_info(
                               tg_id=msg.from_user.id))


async def update_info(msg: types.Message):
    """Хендлер для информиции об обновлении"""
    await bot.send_message(msg.from_user.id,
                           text=Desc.UPDATE_INFO)


async def support_info(msg: types.Message):
    """Хендлер для получении информации о саппорте"""
    await bot.send_message(msg.from_user.id,
                           text=Desc.SUPPORT,
                           reply_markup=sup_kb)


def register_message_other(dis: dp):
    dis.register_message_handler(cmd_start,
                                 commands=['start', 'help'])
    dis.register_message_handler(get_id,
                                 Text(equals='Ваш ID'))
    dis.register_message_handler(update_info,
                                 Text(equals='Обновление 2.03'))
    dis.register_message_handler(support_info,
                                 Text(equals='Канал/Support'))
