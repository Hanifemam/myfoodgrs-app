import pickle

from ExtractFromPostgre import ExtractFromPostgre


class PutInMysql(object):
    """This class aims to store the data in Mysql.

        :param connectio_post: Connection to other database to fetch data.
        :param connection_mysql: Connection to Mysql database.

        """
    def __init__(self, connectio_post, connection_mysql):
        self.post_conn = connectio_post
        self.my_conn = connection_mysql
        self.post_obj = ExtractFromPostgre(connectio_post, connection_mysql)

    def create_food_table(self):
        """This function produces table for foods
            and save it in data base
            """
        my_cursor = self.my_conn.cursor()
        my_cursor.execute('DROP TABLE IF EXISTS foods;')
        query = 'CREATE TABLE foods (id numeric(21, 0) PRIMARY KEY UNIQUE, NAME VARCHAR(500), '
        category_set = self.post_obj.create_categories()
        category_set_removed_space = set()
        for item in category_set:
            category_set_removed_space.add(item.replace(' ', '_'))
        for item in category_set_removed_space:
            query += str(item + ' ')
            query += 'BINARY, '
        query = query[:-2]
        query += ');'
        my_cursor.execute(query)

    def create_full_food_table(self):
        category_set_extra = {'panini', 'dessert', 'appetizer', 'second_course', 'drink', 'wine',
                              'first_course', 'salad', 'side_dish', 'single_course'}
        my_cursor = self.my_conn.cursor()
        my_cursor.execute('DROP TABLE IF EXISTS foods_new;')
        query = 'CREATE TABLE foods_new (id numeric(21, 0) PRIMARY KEY UNIQUE, NAME VARCHAR(500), '
        category_set = self.post_obj.create_categories()
        category_set = category_set.union(category_set_extra)
        category_set_removed_space = set()
        for item in category_set:
            category_set_removed_space.add(item.replace(' ', '_'))
        for item in category_set_removed_space:
            query += str(item + ' ')
            query += 'BINARY, '
        query = query[:-2]
        query += ');'
        my_cursor.execute(query)

    def insert_to_full_foods_new(self):
        self.create_full_food_table()
        # food_dict = self.post_obj.foods_category_extraction()
        with open('supplementary/foods_category_new.pkl', 'rb') as f:
            food_dict = pickle.load(f)
        column_list = []
        mysql_cursor = self.my_conn.cursor(buffered=True)
        mysql_cursor.execute("SHOW columns FROM foods_new")
        query_table = "INSERT INTO foods_new ("
        for column in mysql_cursor:
            query_table = query_table + str(column[0]) + ', '
            column_list.append(column[0])
        query_table = query_table[:-2]
        query_table = query_table + ") VALUES (%s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s, %s, " \
                                    "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        for food_id, food_values in food_dict.items():
            query = [food_id, food_values[0]]
            if food_values[1] == None:
                continue
            if food_values[1] == column_list[2]:
                query.append(True)
            else:
                query.append(False)

            if food_values[1].replace(' ', '_') == column_list[3]:
                query.append(True)
            else:
                query.append(False)

            if food_values[1].replace(' ', '_') == column_list[4]:
                query.append(True)
            else:
                query.append(False)

            if food_values[1].replace(' ', '_') == column_list[5]:
                query.append(True)
            else:
                query.append(False)

            if food_values[1].replace(' ', '_') == column_list[6]:
                query.append(True)
            else:
                query.append(False)

            if food_values[1].replace(' ', '_') == column_list[7]:
                query.append(True)
            else:
                query.append(False)

            if food_values[1].replace(' ', '_') == column_list[8]:
                query.append(True)
            else:
                query.append(False)

            if food_values[1].replace(' ', '_') == column_list[9]:
                query.append(True)
            else:
                query.append(False)

            if food_values[1].replace(' ', '_') == column_list[10]:
                query.append(True)
            else:
                query.append(False)

            if food_values[1].replace(' ', '_') == column_list[11]:
                query.append(True)
            else:
                query.append(False)

            if food_values[1].replace(' ', '_') == column_list[12]:
                query.append(True)
            else:
                query.append(False)

            if food_values[1].replace(' ', '_') == column_list[13]:
                query.append(True)
            else:
                query.append(False)

            if food_values[1].replace(' ', '_') == column_list[14]:
                query.append(True)
            else:
                query.append(False)

            if food_values[1].replace(' ', '_') == column_list[15]:
                query.append(True)
            else:
                query.append(False)

            if food_values[1].replace(' ', '_') == column_list[16]:
                query.append(True)
            else:
                query.append(False)

            if food_values[1].replace(' ', '_') == column_list[17]:
                query.append(True)
            else:
                query.append(False)

            if food_values[1].replace(' ', '_') == column_list[18]:
                query.append(True)
            else:
                query.append(False)

            if food_values[1].replace(' ', '_') == column_list[19]:
                query.append(True)
            else:
                query.append(False)

            if food_values[1].replace(' ', '_') == column_list[20]:
                query.append(True)
            else:
                query.append(False)

            if food_values[1].replace(' ', '_') == column_list[21]:
                query.append(True)
            else:
                query.append(False)

            if food_values[1].replace(' ', '_') == column_list[22]:
                query.append(True)
            else:
                query.append(False)

            if food_values[1].replace(' ', '_') == column_list[23]:
                query.append(True)
            else:
                query.append(False)

            if food_values[1].replace(' ', '_') == column_list[24]:
                query.append(True)
            else:
                query.append(False)

            if food_values[1].replace(' ', '_') == column_list[25]:
                query.append(True)
            else:
                query.append(False)

            # if food_values[1].replace(' ', '_') == column_list[25]:
            #     query.append(True)
            # else:
            #     query.append(False)
            # print(query)
            # print(query_table)
            # input()
            mysql_cursor.execute(query_table, query)
            self.my_conn.commit()

    def insert_to_foods(self):
        self.create_food_table()
        # food_dict = self.post_obj.foods_category_extraction()
        with open('supplementary/foods_category_new.pkl', 'rb') as f:
            food_dict = pickle.load(f)
        column_list = []
        mysql_cursor = self.my_conn.cursor(buffered=True)
        mysql_cursor.execute("SHOW columns FROM foods")
        query_table = "INSERT INTO foods ("
        for column in mysql_cursor:
            query_table = query_table + str(column[0]) + ', '
            column_list.append(column[0])
        query_table = query_table[:-2]
        query_table = query_table + ") VALUES (%s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s, %s)"
        for food_id, food_values in food_dict.items():
            query = [food_id, food_values[0]]
            if food_values[1] is None:
                continue
            if food_values[1] == "side_dish" or food_values[1] == "salad" or food_values[1] == "dessert" \
                or food_values[1] == "wine" or food_values[1] == "drink" or food_values[1] == "appetizer" :
                continue
            if food_values[1] == column_list[2]:
                query.append(True)
            else:
                query.append(False)

            if food_values[1].replace(' ', '_') == column_list[3]:
                query.append(True)
            else:
                query.append(False)

            if food_values[1].replace(' ', '_') == column_list[4]:
                query.append(True)
            else:
                query.append(False)

            if food_values[1].replace(' ', '_') == column_list[5]:
                query.append(True)
            else:
                query.append(False)

            if food_values[1].replace(' ', '_') == column_list[6]:
                query.append(True)
            else:
                query.append(False)

            if food_values[1].replace(' ', '_') == column_list[7]:
                query.append(True)
            else:
                query.append(False)

            if food_values[1].replace(' ', '_') == column_list[8]:
                query.append(True)
            else:
                query.append(False)

            if food_values[1].replace(' ', '_') == column_list[9]:
                query.append(True)
            else:
                query.append(False)

            if food_values[1].replace(' ', '_') == column_list[10]:
                query.append(True)
            else:
                query.append(False)

            if food_values[1].replace(' ', '_') == column_list[11]:
                query.append(True)
            else:
                query.append(False)

            if food_values[1].replace(' ', '_') == column_list[12]:
                query.append(True)
            else:
                query.append(False)

            if food_values[1].replace(' ', '_') == column_list[13]:
                query.append(True)
            else:
                query.append(False)

            if food_values[1].replace(' ', '_') == column_list[14]:
                query.append(True)
            else:
                query.append(False)

            if food_values[1].replace(' ', '_') == column_list[15]:
                query.append(True)
            else:
                query.append(False)

            mysql_cursor.execute(query_table, query)
        self.my_conn.commit()

    def create_restaurant_table(self):
        my_cursor = self.post_obj.my_conn.cursor()
        my_cursor.execute('DROP TABLE IF EXISTS restaurants;')
        query = 'CREATE TABLE restaurants (id numeric(21, 0) PRIMARY KEY UNIQUE, ' \
                'name VARCHAR(500), ' \
                'price_eco BINARY, ' \
                'price_mid BINARY, ' \
                'price_expensive BINARY, ' \
                'service_home_delivery BINARY, ' \
                'latitude numeric(21, 0), ' \
                'longitude numeric(21, 0), ' \
                'address VARCHAR(500), ' \
                'city VARCHAR(500), '\
                'logo VARCHAR(500))'

        my_cursor.execute(query)

    def insert_to_restaurants(self):
        self.create_restaurant_table()
        restaurant_dict = self.post_obj.extract_restaurants_features()
        mysql_cursor = self.my_conn.cursor()
        query_table = "INSERT INTO restaurants (id, name, price_eco, price_mid, price_expensive, " \
                      "service_home_delivery, latitude, longitude, " \
                      "address, city, logo) " \
                      "VALUES (%(id)s, %(name)s, %(price_eco)s, %(price_mid)s, %(price_expensive)s," \
                      " %(service_home_delivery)s, " \
                      "%(latitude)s, %(longitude)s, %(address)s, %(city)s, %(logo)s)"
        for restaurant in restaurant_dict:
            mysql_cursor.execute(query_table, restaurant)

    def create_menu_table(self):
        my_cursor = self.post_obj.my_conn.cursor()
        my_cursor.execute('DROP TABLE IF EXISTS menu;')
        query = 'CREATE TABLE menu (id int PRIMARY KEY UNIQUE auto_increment, ' \
                'food_id numeric(21, 0), ' \
                'restaurant_id numeric(21, 0),' \
                'FOREIGN KEY (food_id) REFERENCES foods(id), ' \
                'FOREIGN KEY (restaurant_id) REFERENCES restaurants(id));'
        my_cursor.execute(query)
        self.post_obj.my_conn.commit()

    def insert_to_menu(self):
        self.create_menu_table()
        menu_dict = self.post_obj.menu_extraction()
        mysql_cursor = self.my_conn.cursor()
        foregin_key_foods = set()
        mysql_cursor.execute("SELECT id FROM foods")
        for foregin_key in mysql_cursor:
            foregin_key_foods.add(int(foregin_key[0]))
        query_table = "INSERT INTO menu (food_id, restaurant_id) " \
                      "VALUES (%(food_id)s, %(restaurant_id)s)"
        for food_id in menu_dict:
            if food_id['food_id'] in foregin_key_foods:
                mysql_cursor.execute(query_table, food_id)
        self.my_conn.commit()

    def create_full_menu_table(self):
        my_cursor = self.post_obj.my_conn.cursor()
        my_cursor.execute('DROP TABLE IF EXISTS menu_full;')
        query = 'CREATE TABLE menu_full (id int PRIMARY KEY UNIQUE auto_increment, ' \
                'food_id numeric(21, 0), ' \
                'restaurant_id numeric(21, 0));' \
                # 'FOREIGN KEY (food_id) REFERENCES foods(id), ' \
                # 'FOREIGN KEY (restaurant_id) REFERENCES restaurants(id));'
        my_cursor.execute(query)

    def insert_to_full_menu(self):
        self.create_full_menu_table()
        menu_dict = self.post_obj.menu_extraction()
        mysql_cursor = self.my_conn.cursor()
        foregin_key_foods = set()
        mysql_cursor.execute("SELECT id FROM foods_new")
        for foregin_key in mysql_cursor:
            foregin_key_foods.add(int(foregin_key[0]))
        query_table = "INSERT INTO menu_full (food_id, restaurant_id) " \
                      "VALUES (%(food_id)s, %(restaurant_id)s)"
        for food_id in menu_dict:
            if food_id['food_id'] in foregin_key_foods:
                mysql_cursor.execute(query_table, food_id)

        self.my_conn.commit()



