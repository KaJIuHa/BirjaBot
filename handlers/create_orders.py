from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from create_bot import bot, dp
from keybords.keyboard import cancel_but, confirm_but
from database.user_base import db
from utils.texts import Desc
from utils.error_texts import Erorrs


class FSMClientOrderSell(StatesGroup):
    count_bots = State()
    price = State()
    confirm = State()


async def sell_bots_start(call: types.CallbackQuery):
    """Запуск создания заявки"""
    await bot.send_message(call.from_user.id,
                           text=Desc.CLIENT_SELL,
                           reply_markup=cancel_but)
    await FSMClientOrderSell.count_bots.set()
    await call.answer(cache_time=3)


async def sell_bots_add_count(msg: types.Message, state: FSMContext):
    """Получаем от пользователя количество ботов для продажи"""
    if msg.text.isdigit():
        async with state.proxy() as data:
            data['count'] = int(msg.text)
        await bot.send_message(msg.from_user.id,
                               text=Desc.CLIENT_SELL_PRICE,
                               reply_markup=cancel_but)
        await FSMClientOrderSell.next()
    else:
        await bot.send_message(msg.from_user.id,
                               text=Erorrs.ER_COUNT_VAL,
                               reply_markup=cancel_but)


async def sell_bots_add_price(msg: types.Message, state: FSMContext):
    """Получаем от пользователя сумму продажи"""
    if msg.text.isdigit():
        async with state.proxy() as data:
            data['comission'] = data['count'] * 1
            data['price'] = int(msg.text) * data['count']
            data['total_price'] = data['price'] + data['comission']
            if db.check_user_balance(msg.from_user.id) >= data['total_price']:
                await bot.send_message(msg.from_user.id,
                                       text=Desc.user_sal_bots(data),
                                       reply_markup=confirm_but)
                await FSMClientOrderSell.next()
            else:
                await bot.send_message(msg.from_user.id,
                                       text=Erorrs.ER_BALANCE_VAL,
                                       reply_markup=cancel_but)

    else:
        await bot.send_message(msg.from_user.id,
                               text=Erorrs.ER_COUNT_VAL,
                               reply_markup=cancel_but)


async def confirm_sale_client_bot(call: types.CallbackQuery, state: FSMContext):
    """Добавляем значения в базу данных(у создавшего отнимаем количестов ботов в ордере,
     добавляем занчения в таблицу ордеров)"""
    try:
        async with state.proxy() as data:
            data['user_id'] = call.from_user.id
            db.create_order(data)
            # db.update_incom_comision(data['comission'])
            db.update_user_balance_commision(data)
            await bot.send_message(call.from_user.id,
                                   text=Desc.ORDER_ADD_SUC)

            await state.finish()
            await call.answer(cache_time=3)
    except Exception as ex:
        print(Erorrs.error_orders_add(ex))
        await state.finish()
        await bot.send_message(call.from_user.id,
                               text=Erorrs.ERR_ADD)


async def canceled(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.answer(text=Desc.CANCEl,
                      show_alert=True)


def register_message_create_orders(dis: dp):
    dis.register_callback_query_handler(sell_bots_start, text="Buybotuser")
    dis.register_message_handler(sell_bots_add_count, state=FSMClientOrderSell.count_bots)
    dis.register_message_handler(sell_bots_add_price, state=FSMClientOrderSell.price)
    dis.register_callback_query_handler(confirm_sale_client_bot, text='yes', state=FSMClientOrderSell.confirm)
    dis.register_callback_query_handler(canceled, text='no', state='*')
