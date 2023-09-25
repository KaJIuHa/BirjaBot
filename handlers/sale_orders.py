from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from create_bot import bot, dp
from keybords.keyboard import cancel_but, confirm_but
from database.user_base import db
from utils.texts import Desc
from utils.error_texts import Erorrs


class FSMClientOrderBuy(StatesGroup):
    order_id = State()
    confirm = State()


async def buy_bot_start(call: types.CallbackQuery):
    await bot.send_message(call.from_user.id,
                           text=Desc.BUY_STR,
                           reply_markup=cancel_but)
    await FSMClientOrderBuy.order_id.set()
    await call.answer(cache_time=1)


async def check_order_id(msg: types.Message, state: FSMContext):
    if msg.text.isdigit():
        res = db.check_order(int(msg.text))
        if res is not None:
            async with state.proxy() as data:
                data['order_id'] = int(msg.text)
                data['user_id_sell'] = msg.from_user.id     # Уменьшить количестов ботов,увеличить баланса
                data['user_id_buy'] = res[0]  #Увеличить количество ботов
                data['count'] = res[1]
                data['price'] = res[2]
                if db.check_users_bot(msg.from_user.id) >= data['count']:
                    await bot.send_message(msg.from_user.id,
                                           text=Desc.info_user_buy(data),
                                           reply_markup=confirm_but)
                    await FSMClientOrderBuy.next()
                else:
                    await bot.send_message(msg.from_user.id,
                                           text=Erorrs.ER_MONEY,
                                           reply_markup=cancel_but)
        else:
            await bot.send_message(msg.from_user.id,
                                   text=Erorrs.ER_COUNT_VAL,
                                   reply_markup=cancel_but)


async def confirm_buy_order(call: types.CallbackQuery, state: FSMContext):
    try:
        async with state.proxy() as data:
            db.add_buy_bots(data)
            db.add_bots_for_order(data)
            await bot.send_message(chat_id=data['user_id_buy'], text=Desc.CONGRET)
            db.deactivate_order(data['order_id'])
            await state.finish()
        await bot.send_message(call.from_user.id,text = Desc.CONGRET_BUER )
        await call.answer(cache_time=1)
    except Exception as ex:
        print(Erorrs.error_buy_order(ex))
        await bot.send_message(call.from_user.id,
                               text=Erorrs.ERR_ADD)
        await call.answer(cache_time=1)


def register_message_sale_orders(dis: dp):
    dis.register_callback_query_handler(buy_bot_start, text="Sellbotuser")
    dis.register_message_handler(check_order_id, state=FSMClientOrderBuy.order_id)
    dis.register_callback_query_handler(confirm_buy_order, text="yes", state=FSMClientOrderBuy.confirm)
