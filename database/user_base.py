import psycopg2
from psycopg2 import Error
from create_bot import DB_IP, DB_NAME, DB_PASS, DB_PORT, DB_USER


class Database:
    def __init__(self):
        try:
            # Connect to an existing database
            self.connect = psycopg2.connect(user=DB_USER,
                                            password=DB_PASS,
                                            host=DB_IP,
                                            port=DB_PORT,
                                            database=DB_NAME)

            self.cursor = self.connect.cursor()
            if self.connect:
                print('Data base connected OK')
        except (Exception, Error) as error:
            print("Error while connecting to PostgreSQL", error)
            self.connect.close()

    # def __init__(self, data):
    #     """Инициализация БД"""
    #     self.connect = sqlite3.connect(data)
    #     self.cursor = self.connect.cursor()
    #     if self.connect:
    #         print('Data base connected OK')

    def check_user(self, user_id):
        """Проверяем пользователя на наличиее"""
        try:
            self.cursor.execute('SELECT * FROM users WHERE user_id = %s', (user_id,))
            return bool(self.cursor.fetchone())
        except Exception as ex:
            print(f'Ошибка: {ex}, в функции :{"check_user"}')
            self.connect.rollback()

    def create_user(self, user_id):
        """Добавление пользователя в БД"""
        try:
            self.cursor.execute('INSERT INTO users (user_id) VALUES (%s)', (user_id,))
            self.connect.commit()
        except Exception as ex:
            print(f'Ошибка: {ex}, в функции :{"create_user"}')
            self.connect.rollback()

    def create_order(self, data):
        """Создаем ордер в таблице ордеров"""
        try:
            self.cursor.execute('INSERT INTO orders '
                                '(user_id,count_bots,costs) VALUES (%s,%s,%s)', (data['user_id'],
                                                                                 data['count'],
                                                                                 data['price']))
            self.connect.commit()
        except Exception as ex:
            print(f'Ошибка: {ex}, в функции :{"create_order"}')
            self.connect.rollback()

    def insert_image_db(self, data):
        """Добавление картинки в БД"""
        try:
            self.cursor.execute('INSERT INTO image (image_link) VALUES (%s)', (data,))
            self.connect.commit()
        except Exception as ex:
            print(f'Ошибка: {ex}, в функции :{"create_order"}')
            self.connect.rollback()

    def check_users_bot(self, user_id):
        """Получаем количестов ботов у пользователя"""
        try:
            self.cursor.execute("""SELECT user_bots FROM public.users WHERE user_id = %s""", (user_id,))
            return self.cursor.fetchone()[0]
        except Exception as ex:
            print(f'Ошибка: {ex}, в функции :{"check_users_bot"}')
            self.connect.rollback()

    def check_user_balance(self, user_id):
        """Проверяем баланс пользователя"""
        try:
            self.cursor.execute("""SELECT user_balance FROM users WHERE user_id = %s""", (user_id,))
            return self.cursor.fetchone()[0]
        except Exception as ex:
            print(f'Ошибка: {ex}, в функции :{"check_user_balance"}')
            self.connect.rollback()

    def get_users(self):
        """Получаем всех пользователей из базы"""
        try:
            self.cursor.execute("""SELECT user_id FROM users""")
            return self.cursor.fetchall()
        except Exception as ex:
            print(f'Ошибка: {ex}, в функции :{"get_users"}')
            self.connect.rollback()

    def get_images(self):
        """Получаем все картинки из базы"""
        try:
            self.cursor.execute("""SELECT image_link FROM image WHERE is_on = 1""")
            return self.cursor.fetchall()
        except Exception as ex:
            print(f'Ошибка: {ex}, в функции :{"get_images"}')
            self.connect.rollback()

    async def update_user_bots(self, count, user_id):
        """Убераем ботов при продаже ботов"""
        try:
            self.cursor.execute(f"""UPDATE users SET user_bots = user_bots - %s  WHERE user_id = %s""",
                                (count, user_id))
            self.connect.commit()
        except Exception as ex:
            print(f'Ошибка: {ex}, в функции :{"update_user_bots"}')
            self.connect.rollback()

    def get_buy_link(self, table):
        """Получение ссылки для оплаты"""
        try:
            self.cursor.execute(f'SELECT link FROM {table} WHERE is_on = 1')
            return self.cursor.fetchone()[0]
        except Exception as ex:
            print(f'Ошибка: {ex}, в функции :{"get_buy_link"}')
            self.connect.rollback()

    async def close_link(self, link, table):
        """Деактивация ссылки для оплаты"""
        try:
            self.cursor.execute(f"""UPDATE {table} SET is_on = 0 WHERE link = %s""", (link,))
            self.connect.commit()
        except Exception as ex:
            print(f'Ошибка: {ex}, в функции :{"close_link"}')
            self.connect.rollback()

    def take_values_user(self, user_id):
        """Получаем баланс и количестов ботов пользователя"""
        try:
            self.cursor.execute("""SELECT user_bots,user_balance FROM users WHERE user_id = %s""", (user_id,))
            return self.cursor.fetchone()
        except Exception as ex:
            print(f'Ошибка: {ex}, в функции :{"take_values_user"}')
            self.connect.rollback()

    def take_income_value(self):
        """Получаем количестов денег в инкоме"""
        try:
            self.cursor.execute("""SELECT money FROM income """)
            return self.cursor.fetchone()[0]
        except Exception as ex:
            print(f'Ошибка: {ex}, в функции :{"take_income_value"}')
            self.connect.rollback()

    def update_income(self, res):
        """Обновляем файл инкам при рассылке"""
        try:
            self.cursor.execute(f"""UPDATE income SET money = money -  %s""", (res,))
            self.connect.commit()
        except Exception as ex:
            print(f'Ошибка: {ex}, в функции :{"update_income"}')
            self.connect.rollback()

    def update_incom_comision(self, count):
        try:
            self.cursor.execute(f"""UPDATE income SET money = money +  %s""", (count,))
            self.connect.commit()
        except Exception as ex:
            print(f'Ошибка: {ex}, в функции :{"update_income"}')
            self.connect.rollback()

    def update_user_balnce(self, user_id, res):
        """Обновлеям баланс пользователя при рассылке"""
        try:
            self.cursor.execute("""UPDATE users SET user_balance = user_balance + %s WHERE user_id = %s""",
                                (res, user_id))
            self.connect.commit()
        except Exception as ex:
            print(f'Ошибка: {ex}, в функции :{"update_user_balnce"}')
            self.connect.rollback()

    def update_user_balnce_commision(self, user_id, res):
        """Обновлеям баланс пользователя"""
        try:
            self.cursor.execute("""UPDATE users SET user_balance = user_balance - %s WHERE user_id = %s""",
                                (res, user_id))
            self.connect.commit()
        except Exception as ex:
            print(f'Ошибка: {ex}, в функции :{"update_user_balnce"}')
            self.connect.rollback()

    def update_image(self, res):
        """Обновляем файлы картинок"""
        try:
            self.cursor.execute(f"""UPDATE image SET is_on = 0 WHERE image_link = %s""", (res,))
            self.connect.commit()
        except Exception as ex:
            print(f'Ошибка: {ex}, в функции :{"update_image"}')
            self.connect.rollback()

    def get_user_orders(self, user_id):
        """Получаем список ордеров для пользователя из БД"""
        try:
            self.cursor.execute("""SELECT order_id,count_bots,costs FROM orders 
            WHERE user_id = %s AND is_on = 1""", (user_id,))
            return self.cursor.fetchall()
        except Exception as ex:
            print(f'Ошибка: {ex}, в функции :{"get_user_orders"}')
            self.connect.rollback()

    def get_all_orders(self):
        """Получаем список всех ордеров """
        try:
            self.cursor.execute("""SELECT order_id,count_bots,costs 
            FROM orders WHERE is_on = 1""")
            return self.cursor.fetchall()
        except Exception as ex:
            print(f'Ошибка: {ex}, в функции :{"get_all_orders"}')
            self.connect.rollback()

    def check_order(self, order_id):
        """Проверка наличияя ордера для покупки"""
        try:
            self.cursor.execute("""SELECT user_id,count_bots,costs FROM orders 
            WHERE order_id = %s AND is_on = 1""", (order_id,))
            return self.cursor.fetchone()
        except Exception as ex:
            print(f'Ошибка: {ex}, в функции :{"check_order"}')
            self.connect.rollback()

    def add_buy_bots(self, data):
        """Добавление в БД к купившемк пользователю ботов и снятие денег"""
        try:
            self.cursor.execute("""UPDATE users SET
                                    user_balance = user_balance + %s,
                                    user_bots = user_bots - %s 
                                    WHERE user_id = %s""",
                                (data['price'],data['count'], data['user_id_sell']))
            # self.cursor.execute("""UPDATE users SET user_bots = user_bots - %s WHERE user_id = %s""",
            #                     (data['count'], data['user_id_sell']))
            self.connect.commit()
        except Exception as ex:
            print(f'Ошибка: {ex}, в функции :{"add_buy_bots"}')
            self.connect.rollback()

    def add_bots_for_order(self, data):
        """Зачислем средства на счет пользовтеля выставишего ордер"""
        try:
            self.cursor.execute("""UPDATE users SET user_bots = user_bots + %s 
            WHERE user_id = %s""", (data['count'], data['user_id_buy']))
            self.connect.commit()
        except Exception as ex:
            print(f'Ошибка: {ex}, в функции :{"add_money_for_order"}')
            self.connect.rollback()

    def deactivate_order(self, order_id):
        """Деактивация ордера"""
        try:
            self.cursor.execute(f"""UPDATE orders SET is_on = 0 WHERE order_id = %s""", (order_id,))
            self.connect.commit()
        except Exception as ex:
            print(f'Ошибка: {ex}, в функции :{"deactivate_order"}')
            self.connect.rollback()

    def update_user_balance_money(self, data):
        """Обновляем баланс пользователя в блоке рассылки"""
        try:
            self.cursor.execute(f"""UPDATE users SET user_balance = user_balance - %s 
            WHERE user_id = %s""", (data['value'], data['user_id']))
            self.connect.commit()
        except Exception as ex:
            print(f'Ошибка: {ex}, в функции :{"update_user_balance"}')
            self.connect.rollback()

    def update_user_balance_commision(self, data):
        """Обновляем баланс пользователя в блоке ордеров"""
        try:
            self.cursor.execute(f"""UPDATE users SET user_balance = user_balance - %s 
            WHERE user_id = %s""", (data['total_price'], data['user_id']))
            self.connect.commit()
        except Exception as ex:
            print(f'Ошибка: {ex}, в функции :{"update_user_balance"}')
            self.connect.rollback()


db = Database()
