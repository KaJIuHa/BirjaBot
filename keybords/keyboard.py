from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

"""Стартовые кнопки"""
btn1 = KeyboardButton("Мои боты")
btn2 = KeyboardButton("Доход")
btn3 = KeyboardButton("Ваш ID")
btn4 = KeyboardButton("Обновление 2.03")
btn5 = KeyboardButton("Биржа")
btn6 = KeyboardButton("Канал/Support")
kb_start = ReplyKeyboardMarkup(resize_keyboard=True).add(btn1, btn2, btn3, btn4, btn5, btn6)
"""Кнопки (мои боты)"""
button1 = InlineKeyboardButton(text="Купить 5 Ботов. Цена:520 rub",
                               callback_data="bots5")
button2 = InlineKeyboardButton(text="Купить 25 Ботов. Цена:2600 rub",
                               callback_data="bots25")
button3 = InlineKeyboardButton(text="Купить 50 Ботов. Цена:5200 rub",
                               callback_data="bots50")
button4 = InlineKeyboardButton(text="Купить 250 Ботов. Цена:26000 rub",
                               callback_data="bots250")
bt_my_bots = InlineKeyboardMarkup().add(
    button1).add(button2).add(button3).add(button4)
"""Кнопки (биржа)"""
# Create a keyboard with 2 buttons
button6 = InlineKeyboardButton(text="ПОКУПКА",
                               callback_data="Buybotuser")
button7 = InlineKeyboardButton(text="ПРОДАЖА",
                               callback_data="order")
button8 = InlineKeyboardButton('МОИ ОРДЕРА',
                               callback_data='my_orders')
bt_market = InlineKeyboardMarkup().row(button6, button7).row(button8)
"""Кнопки(доход)"""
button15 = InlineKeyboardButton(text="Вывод от 500₽",
                                callback_data="Send_money")
bt_u_inc = InlineKeyboardMarkup().add(button15)
"""Кнопка перехода на поддержку"""
sup = InlineKeyboardButton('Перейти',
                           url='https://t.me/Steam_OceanAI')
sup_kb = InlineKeyboardMarkup().add(sup)
"""Кнопка отмены состояния"""
no_add = InlineKeyboardButton('Отмена',
                              callback_data='no')
cancel_but = InlineKeyboardMarkup().add(no_add)
"""Подтверждение продажи(покупки)"""
conf_add = InlineKeyboardButton('Подтвердить',
                                callback_data='yes')
confirm_but = InlineKeyboardMarkup().add(conf_add).add(no_add)

"""Подтверждение продажи(покупки)"""
conf_add_2 = InlineKeyboardButton('Подтвердить',
                                  callback_data='yess')
confirm_but2 = InlineKeyboardMarkup().add(conf_add_2).add(no_add)
"""Кнопка продажи"""
sell_button = InlineKeyboardButton('Перейти к продаже',callback_data='Sellbotuser')
sel_b = InlineKeyboardMarkup().add(sell_button)

