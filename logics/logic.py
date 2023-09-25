import random
import asyncio
from database.user_base import db
from create_bot import bot, CHAT
from utils.texts import Desc
from utils.error_texts import Erorrs


async def calculation_thread():
    while True:
        delay_seconds = random.randint(10, 20)
        try:
            users = db.get_users()
            for user in users:
                print(user[0])
                result = db.take_values_user(user_id=user[0])
                print(result)
                # balance = result[1]
                num_bots = result[0]
                z = db.take_income_value()
                # Calculate q
                if num_bots > 0 and z > 0:
                    a = random.uniform(0.9, 9.9)
                    q = ((z / 100) * (0.0023 * num_bots)) / a
                    z -= q
                    print(float(q))
                    db.update_income(res=float(q))
                    db.update_user_balnce(user_id=user[0],
                                          res=float(q))
                    await bot.send_message(chat_id=user[0],
                                           text=Desc.calculation_result(result=float(q)))
                    await asyncio.sleep(delay_seconds)
                else:
                    delay_seconds = random.randint(1, 3)  # 300,7200
                    await asyncio.sleep(delay_seconds)
        except Exception as ex:
            print(Erorrs.error_logic(ex))
            await asyncio.sleep(delay_seconds)
            continue


async def trade_screen():
    delay_seconds = random.randint(10, 20)
    try:
        captions = db.get_images()
        users = db.get_users()
        for caption in captions:
            for user in users:
                await bot.send_photo(chat_id=user[0],
                                     photo=caption[0],
                                     caption=Desc.CAP_INFO)

                await asyncio.sleep(delay_seconds)
                db.update_image(res=caption[0])
        await bot.send_message(chat_id=CHAT,
                               text=Desc.STOP_IMG)
    except Exception as ex:
        print(Erorrs.error_logic(ex))
        await asyncio.sleep(delay_seconds)


def get_my_order_list(user_id):
    orders = db.get_user_orders(user_id)
    a = []
    for order in orders:
        a.append(Desc.orders_info(order))
    return "\n".join(a)


def get_all_order_list():
    orders = db.get_all_orders()
    res = []
    for order in orders:
        res.append(Desc.orders_info(order))
    return "\n".join(res)
