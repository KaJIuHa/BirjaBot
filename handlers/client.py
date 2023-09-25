from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from create_bot import bot, dp, CHAT
from keybords.keyboard import bt_my_bots, bt_market, bt_u_inc, cancel_but, confirm_but2, sel_b
from logics import logic
from utils.texts import Desc
from utils.error_texts import Erorrs
from database.user_base import db


class FSMCLientMoney(StatesGroup):
    value = State()
    phone = State()
    confirm = State()


async def my_bots(msg: types.Message):
    """Хендлер команды (мои боты)"""
    await bot.send_message(msg.from_user.id,
                           text=Desc.my_bots(
                               count=db.check_users_bot(msg.from_user.id)),
                           reply_markup=bt_my_bots)


async def market(msg: types.Message):
    """Хендлер кнопки 'Доход' """
    await bot.send_message(msg.from_user.id,
                           text=Desc.my_bots(
                               count=db.check_users_bot(msg.from_user.id)),
                           reply_markup=bt_market)


async def user_income(msg: types.Message):
    """Хендлер доходов пользователя"""
    await bot.send_photo(msg.from_user.id,
                         photo=open('pic/rogo.jpg', 'rb'),
                         caption=Desc.balance_info(
                             balance=db.check_user_balance(msg.from_user.id)),
                         reply_markup=bt_u_inc)


async def buy_bots(call: types.CallbackQuery):
    """Хендлер подвтерждения покупки ботов """
    try:
        link = db.get_buy_link(table=call.data)
        await bot.send_message(call.from_user.id,
                               text=Desc.buy_bots(call.data),
                               reply_markup=InlineKeyboardMarkup().add(
                                   InlineKeyboardButton('Купить',
                                                        url=link)))
        await call.answer(cache_time=3)
        await db.close_link(table=call.data,
                            link=link)
        await bot.send_message(chat_id=CHAT,
                               text=Desc.info_admin_of_buy(user_id=call.from_user.id,
                                                           count=call.data,
                                                           link=link)
                               )
    except Exception as ex:
        print(Erorrs.error_buy(ex))
        await bot.send_message(call.from_user.id,
                               text=Desc.NOTHING_TO_BUY)
        await call.answer(cache_time=3)


async def show_my_orders(call: types.CallbackQuery):
    """Просмотр только своиз ордеров"""
    try:
        result = logic.get_my_order_list(call.from_user.id)
        await bot.send_message(call.from_user.id,
                               text=result)
        await call.answer(cache_time=1)
    except Exception as ex:
        print(Erorrs.error_show(ex))
        await bot.send_message(call.from_user.id,
                               text=Erorrs.ERR_ADD)


async def show_all(call: types.CallbackQuery):
    """Просмотр всех ордеров"""
    try:
        await bot.send_message(call.from_user.id,
                               text=logic.get_all_order_list(),
                               reply_markup=sel_b)
        await call.answer(cache_time=1)
    except Exception as ex:
        print(Erorrs.error_show(ex))
        await bot.send_message(call.from_user.id,
                               text=Erorrs.ERR_ADD)


async def want_money_start(call: types.CallbackQuery):
    await bot.send_photo(call.from_user.id,
                         photo=open('pic/rogo.jpg', 'rb'),
                         caption=Desc.WANT_MONEY,
                         reply_markup=cancel_but)
    await call.answer(cache_time=1)
    await FSMCLientMoney.value.set()


async def want_get_value(msg: types.Message, state: FSMContext):
    """Получения и проверка запроса пользователя(количество выводимых денег)"""
    if msg.text.isdigit():
        res = db.check_user_balance(msg.from_user.id)
        if int(msg.text) > 500:
            if res > int(msg.text):
                async with state.proxy() as data:
                    data['value'] = int(msg.text)
                    data['user_id'] = msg.from_user.id
                await bot.send_message(msg.from_user.id,
                                       text=Desc.ADD_PHONE)
                await FSMCLientMoney.next()
            else:
                await bot.send_message(msg.from_user.id,
                                       text=Erorrs.ER_MONEY_WANT,
                                       reply_markup=cancel_but)
        else:
            await bot.send_message(msg.from_user.id,
                                   text=Erorrs.ER_MONEY_WANT,
                                   reply_markup=cancel_but)
    else:
        await bot.send_message(msg.from_user.id,
                               text=Erorrs.ER_COUNT_VAL,
                               reply_markup=cancel_but)


async def want_add_phone(msg: types.Message, state: FSMContext):
    """Получение и проверка номера телефона"""
    async with state.proxy() as data:
        data['phone'] = msg.text
        await bot.send_message(msg.from_user.id,
                               text=Desc.info_want_user(data),
                               reply_markup=confirm_but2)
    await FSMCLientMoney.next()


async def money_finish(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=1)
    async with state.proxy() as data:
        db.update_user_balance_money(data)
        await bot.send_message(chat_id=CHAT,
                               text=Desc.info_want_user_admin(data))
    await state.finish()
    await bot.send_message(call.from_user.id,
                           text=Desc.SUC_WANT)


def register_message_client(dis: dp):
    dis.register_message_handler(my_bots,
                                 Text(equals='Мои боты'))
    dis.register_message_handler(market,
                                 Text(equals='Биржа'))
    dis.register_message_handler(user_income,
                                 Text(equals='Доход'))
    dis.register_callback_query_handler(buy_bots,
                                        Text(startswith='bots'))
    dis.register_callback_query_handler(show_my_orders,
                                        text='my_orders')
    dis.register_callback_query_handler(show_all,
                                        text='order')
    dis.register_callback_query_handler(want_money_start,
                                        text="Send_money")
    dis.register_message_handler(want_get_value,
                                 state=FSMCLientMoney.value)
    dis.register_message_handler(want_add_phone,
                                 state=FSMCLientMoney.phone)
    dis.register_callback_query_handler(money_finish,
                                        text='yess',
                                        state=FSMCLientMoney.confirm)
