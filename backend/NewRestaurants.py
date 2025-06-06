from geopy.geocoders import Nominatim

from ExtractFromPostgre import ExtractFromPostgre


class CreateNewDB(object):
    def __init__(self, connectio_post, connection_mysql):
        self.my_conn = connection_mysql
        self.post_obj = ExtractFromPostgre(connectio_post, connection_mysql)

    def create_food_table(self):
        my_cursor = self.my_conn.cursor()
        my_cursor.execute('DROP TABLE IF EXISTS foods;')
        query = 'CREATE TABLE foods (id int PRIMARY KEY UNIQUE auto_increment, NAME VARCHAR(500), '
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
        self.my_conn.commit()


    def create_restaurant_table(self):
        my_cursor = self.my_conn.cursor()
        my_cursor.execute('DROP TABLE IF EXISTS restaurants;')
        query = 'CREATE TABLE restaurants (id int PRIMARY KEY UNIQUE auto_increment, ' \
                'name VARCHAR(500), ' \
                'price_eco BINARY, ' \
                'price_mid BINARY, ' \
                'price_expensive BINARY, ' \
                'service_home_delivery BINARY, ' \
                'latitude FLOAT, ' \
                'longitude FLOAT, ' \
                'address VARCHAR(500), ' \
                'city VARCHAR(500), '\
                'logo VARCHAR(500))'
        my_cursor.execute(query)
        self.my_conn.commit()

    def create_menu_table(self):
        my_cursor = self.my_conn.cursor()
        my_cursor.execute('DROP TABLE IF EXISTS menu;')
        query = 'CREATE TABLE menu (id int PRIMARY KEY UNIQUE auto_increment, ' \
                'food_id int, ' \
                'restaurant_id int,' \
                'FOREIGN KEY (food_id) REFERENCES foods(id), ' \
                'FOREIGN KEY (restaurant_id) REFERENCES restaurants(id));'
        my_cursor.execute(query)
        self.my_conn.commit()

    def add_new_info(self):
        restaurant = dict()
        rest_name = input("Add Restaurant Name: ")
        restaurant['name'] = rest_name
        city = 'Bolzano'
        restaurant['city'] = city
        logo = input("Input logo name: ")
        restaurant['logo'] = logo
        address = input("Input address: ")
        address = address + ', Bolzano' + ', Italy'
        restaurant['address'] = address
        price = input("Insert min Price: ")
        if int(price) < 14:
            restaurant['price_eco'] = True
            restaurant['price_mid'] = False
            restaurant['price_expensive'] = False
        elif 14 < int(price) < 24:
            restaurant['price_eco'] = False
            restaurant['price_mid'] = True
            restaurant['price_expensive'] = False
        else:
            restaurant['price_eco'] = False
            restaurant['price_mid'] = False
            restaurant['price_expensive'] = True
        home_delivery = input("Insert 1 if contains home delivery service: ")
        if int(home_delivery) == 1:
            restaurant['service_home_delivery'] = True
        else:
            restaurant['service_home_delivery'] = False
        location = self.update_location_by_address(address)
        restaurant['latitude'] = location['lat']
        restaurant['longitude'] = location['lon']
        rest_id = self.insert_to_restaurants(restaurant)
        food_name = ''
        food_name_dict = {}
        while food_name != 'done':
            category_name = None
            food_name = input("Insert new food name: ")
            print(food_name)
            if food_name == 'done':
                continue
            category_number = input("Insert the number for category: 1.PIZZA, \n 2.PESCE, \n 3. INTERIORA, \n 4. LEGUMI, \n "
                                    "5.VERDURE, \n 6.TORTELLINI, \n 7.FORMAGGI, \n 8.PASTA, \n 9.GNOCCHI, \n 10.FUNGHI, \n "
                                    "11.CARNE, \n 12.RISO, \n 13. CROSTACEI_E_MOLLUSCHI, \n 14.SALUMI \n")
            if int(category_number) == 1:
                category_name = 'PIZZA'
            elif int(category_number) == 2:
                category_name = 'PESCE'
            elif int(category_number) == 3:
                category_name = 'INTERIORA'
            elif int(category_number) == 4:
                category_name = 'LEGUMI'
            elif int(category_number) == 5:
                category_name = 'VERDURE'
            elif int(category_number) == 6:
                category_name = 'TORTELLINI'
            elif int(category_number) == 7:
                category_name = 'FORMAGGI'
            elif int(category_number) == 8:
                category_name = 'PASTA'
            elif int(category_number) == 9:
                category_name = 'PASTA'
            elif int(category_number) == 10:
                category_name = 'GNOCCHI'
            elif int(category_number) == 11:
                category_name = 'CARNE'
            elif int(category_number) == 12:
                category_name = 'RISO'
            elif int(category_number) == 13:
                category_name = 'CROSTACEI_E_MOLLUSCHI'
            elif int(category_number) == 14:
                category_name = 'SALUMI'
            food_name_dict = dict()
            food_name_dict[food_name] = category_name
            food_id = self.add_food(food_name_dict)
            menu_dict = dict()
            menu_dict['food_id'] = food_id[0]
            menu_dict['restaurant_id'] = rest_id[0]
            self.add_to_menu(menu_dict)


    def update_location_by_address(self, address):
        coordination_dict = dict()
        geolocator = Nominatim(user_agent="AIzaSyBVKguW-Fc_dQM2CmrmKFQw4FtTTlw6mdw")
        pre_lic = geolocator.geocode(address)
        if pre_lic is not None:
            geo_row = pre_lic.raw
            coordination_dict['lat'] = geo_row['lat']
            coordination_dict['lon'] = geo_row['lon']
        else:
            coordination_dict['lat'] = 46.4985
            coordination_dict['lon'] = 11.3507
        return coordination_dict

    def add_to_menu(self, food):
        mysql_cursor = self.my_conn.cursor()
        query_table = "INSERT INTO menu (food_id, restaurant_id) " \
                      "VALUES (%(food_id)s, %(restaurant_id)s)"
        mysql_cursor.execute(query_table, food)
        self.my_conn.commit()

    def insert_to_restaurants(self, restaurant):
        mysql_cursor = self.my_conn.cursor()
        query = "SELECT name FROM restaurants"
        mysql_cursor.execute(query)
        rest_name_set = set()
        for rest in mysql_cursor:
            rest_name_set.add(rest[0])
        if restaurant['name'] not in rest_name_set:
            mysql_cursor = self.my_conn.cursor()
            query_table = "INSERT INTO restaurants (name, price_eco, price_mid, price_expensive, " \
                          "service_home_delivery, latitude, longitude, " \
                          "address, city, logo) " \
                          "VALUES (%(name)s, %(price_eco)s, %(price_mid)s, %(price_expensive)s," \
                          " %(service_home_delivery)s, " \
                          "%(latitude)s, %(longitude)s, %(address)s, %(city)s, %(logo)s)"
            mysql_cursor.execute(query_table, restaurant)
            query = "SELECT last_insert_id();"
            mysql_cursor.execute(query)
            last_id = mysql_cursor.fetchone()
            self.my_conn.commit()
        else:
            name_to_check = restaurant['name']
            mysql_cursor_id = self.my_conn.cursor()
            query = f"SELECT id, name FROM restaurants;"
            mysql_cursor_id.execute(query)
            for rest_loop in mysql_cursor_id:
                if rest_loop[1] == name_to_check:
                    last_id = [rest_loop[0]]
        return last_id


    def add_food(self, food):
        food_info = {"NAME": 0, "PASTA": False, "CARNE": False, "PIZZA": False, "TORTELLINI": False, "SALUMI": False,
                     "PESCE": False, "LEGUMI": False, "FUNGHI": False, "CROSTACEI_E_MOLLUSCHI": False, "VERDURE": False,
                     "GNOCCHI": False, "INTERIORA": False, "FORMAGGI": False, "RISO": False}
        food_info['NAME'] = list(food.keys())[0]
        food_info[list(food.values())[0]] = True
        mysql_cursor = self.my_conn.cursor()
        query = "INSERT INTO foods (NAME, PASTA, CARNE, PIZZA, TORTELLINI, SALUMI, PESCE," \
                "LEGUMI, FUNGHI, CROSTACEI_E_MOLLUSCHI, VERDURE, GNOCCHI, INTERIORA, FORMAGGI, RISO) " \
                "VALUES (%(NAME)s, %(PASTA)s, %(CARNE)s, %(PIZZA)s, %(TORTELLINI)s, " \
                "%(SALUMI)s, %(PESCE)s, %(LEGUMI)s, %(FUNGHI)s, %(CROSTACEI_E_MOLLUSCHI)s, %(VERDURE)s," \
                "%(GNOCCHI)s, %(INTERIORA)s, %(FORMAGGI)s, %(RISO)s)"
        mysql_cursor.execute(query, food_info)
        query = "SELECT last_insert_id();"
        mysql_cursor.execute(query)
        last_id = mysql_cursor.fetchone()
        self.my_conn.commit()
        return last_id
