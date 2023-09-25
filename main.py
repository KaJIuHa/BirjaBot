import logging

from aiogram.utils import executor

from create_bot import dp

from handlers import client, other, create_orders, admin, sale_orders


async def on_startup(_):
    logging.basicConfig(filename='logfile.log',
                        filemode='a',
                        format='%(asctime)s, %(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.DEBUG)

    logging.info("Бот вышел в онлайн!!!!")
    print('Бот вышел в онлайн !!!!!!!!!')
    # await set_default_commands(bot)


client.register_message_client(dp)
admin.register_message_admin(dp)
other.register_message_other(dp)
create_orders.register_message_create_orders(dp)
sale_orders.register_message_sale_orders(dp)

executor.start_polling(dp,
                       skip_updates=True,
                       on_startup=on_startup)
