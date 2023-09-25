from enum import StrEnum


class Erorrs(StrEnum):
    @staticmethod
    def error_buy(ex):
        return (f'Ошибка: {ex}, в блоке покупки ботов пользователем\n'
                f'добавь ссылки для оплаты')

    @staticmethod
    def error_logic(ex):
        return (f'Ошибка: {ex}, в блоке логики для отправки доходов пользователю\n'
                f'Посмотри логи')

    @staticmethod
    def error_logic_image(ex):
        return (f'Ошибка: {ex}, в блоке логики для отправки картинок пользователю\n'
                f'Посмотри логи')

    @staticmethod
    def error_orders_add(ex):
        return (f'Ошибка: {ex}, в блоке добавления ордера пользователем\n'
                f'Посмотри логи')

    @staticmethod
    def error_show(ex):
        return (f'Ошибка: {ex}, в блоке оторажения ордеров\n'
                f'Посмотри логи БД')

    @staticmethod
    def error_buy_order(ex):
        return (f'Ошибка: {ex}, в блоке покупки ордера\n'
                f'Посмотри логи БД')

    ERR_ADD = '<code>Что-то пошло не так,пожалуйста попробуйте позже.</code>'

    ER_COUNT_BOTS = ('<code>У Вас недостаточно ботов для продажи\n'
                     'Укажите меньшее количество</code>')

    ER_MONEY = ('<code>У Вас недостаточно ботов на балансе для продажи данного ордера. '
                'Поплните Ваш баланс ботов либо выберите другой ордер</code>')

    ER_MONEY_WANT = ('<code>У Вас недостаточно средств на балансе '
                     'либо баланс менее 500 руб.\n'
                     '\n'
                     'Проверьте свой баланс!</code>')

    ER_COUNT_VAL = ('<code>Указано неверное значение.\n'
                    'Укажите значение заново</code>')
    ER_BALANCE_VAL = ('<code>На ваешм счету недостаточно средств для создание ордера\n'
                      '\n'
                      'Введите меньшую сумму за 1 бота.</code>')
