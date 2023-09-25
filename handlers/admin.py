from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from create_bot import bot, dp, CHAT
from logics import logic
from utils.texts import Desc
from database.user_base import db

ID = [5630610750, 336299596]


class FSMAdmin(StatesGroup):
    image = State()


async def insert_image(msg: types.Message):
    """Старт для загрузки картинки"""
    if msg.from_user.id in ID:
        await FSMAdmin.image.set()
        await bot.send_message(msg.from_user.id,
                               text=Desc.INSERT_IMAGE)


async def insert_image_finish(msg: types.Message, state: FSMContext):
    """Хендлер для загрузки картинки в БД"""
    async with state.proxy() as data:
        data['photo'] = msg.photo[-1].file_id
        db.insert_image_db(data['photo'])
    await state.finish()
    await bot.send_message(msg.from_user.id,
                           text=Desc.INSERT_IMG_FIN)


async def admin_start_send_income(msg: types.Message):
    """Хендлер для запуска рассылки доходов"""
    if msg.from_user.id in ID:
        await bot.send_message(chat_id=CHAT,
                               text=Desc.SUCCESFILL_POOLING)
        await logic.calculation_thread()
        await bot.send_message(chat_id=CHAT,
                               text=Desc.STOP_POLLINF)


async def admin_start_send_image(msg: types.Message):
    """Хендлер для запуска рассылки картинок"""
    if msg.from_user.id in ID:
        await bot.send_message(chat_id=CHAT,
                               text=Desc.SUCCESFILL_POOLING_IMG)
        await logic.trade_screen()
        await bot.send_message(chat_id=CHAT,
                               text=Desc.STOP_POLLINF_IMG)


def register_message_admin(dis: dp):
    dis.register_message_handler(admin_start_send_income,
                                 commands=['start_polling'])
    dis.register_message_handler(admin_start_send_image,
                                 commands=['image_polling'])
    dis.register_message_handler(insert_image,
                                 commands=['insert'])
    dis.register_message_handler(insert_image_finish,
                                 content_types=['photo'],
                                 state=FSMAdmin.image)
