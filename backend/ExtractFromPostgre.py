import pickle
from uuid import UUID, uuid1, uuid4


class ExtractFromPostgre(object):
    def __init__(self, connection_post, connection_mysql):
        self.post_conn = connection_post
        self.my_conn = connection_mysql

    def create_categories(self):
        category_set = set()
        category_set.add('PIZZA')
        post_cursor = self.post_conn.cursor()
        post_cursor.execute('SELECT DISTINCT dishingredientcategory_key '
                            'FROM prepared_food_product_ingredient_category;')
        for category_type in post_cursor:
            category_set.add(category_type[0])
        return category_set

    def get_foods_id(self):
        food_id_nameid_dict = dict()
        food_id_dish_class_dict = dict()
        post_cursor_id = self.post_conn.cursor()
        post_cursor_id.execute('SELECT id, name_id, dishclass FROM prepared_food_product;')
        for food_id_nameId in post_cursor_id:
            food_id_nameid_dict[food_id_nameId[0]] = food_id_nameId[1]
            food_id_dish_class_dict[food_id_nameId[0]] = food_id_nameId[2]
        return food_id_nameid_dict, food_id_dish_class_dict

    def get_foods_name(self):
        foods_ids = self.get_foods_id()[0]
        food_id_dish_class_dict = self.get_foods_id()[1]
        food_id_dict = dict()
        post_cursor = self.post_conn.cursor()
        for food_id, name_id in foods_ids.items():
            query = 'SELECT value FROM translation WHERE lang_id = 2 AND rows_group =' + str(name_id) + ';'
            post_cursor.execute(query)
            for name in post_cursor:
                food_id_dict[food_id] = name[0]
        return food_id_dict, food_id_dish_class_dict

    def foods_category_extraction(self):
        food_id_dict = self.get_foods_name()[0]
        food_id_dish_class_dict = self.get_foods_name()[1]
        food_category_dict = dict()
        food_id_set = set()
        extra_category_set = set()
        post_cursor = self.post_conn.cursor()
        for food_id, food_name in food_id_dict.items():
            if food_id_dish_class_dict[food_id] == "pizza":
                food_id_set.add(food_id)
                food_category_dict[food_id] = [food_name, "PIZZA"]
            else:
                query = 'SELECT DISTINCT dishingredientcategory_key FROM prepared_food_product_ingredient_category ' \
                        'WHERE pfp_id = ' + str(food_id) + ';'
                post_cursor.execute(query)
                for pfp_name in post_cursor:
                    food_id_set.add(food_id)
                    food_category_dict[food_id] = [food_name, pfp_name[0]]
        for food_id, food_name in food_id_dict.items():
            if food_id not in food_id_set:
                food_category_dict[food_id] = [food_name, food_id_dish_class_dict[food_id]]
                extra_category_set.add(food_id_dish_class_dict[food_id])
        with open('supplementary/foods_category_new.pkl', 'wb') as f:
            pickle.dump(food_category_dict, f)
        return food_category_dict

    def extract_restaurants_features(self):
        post_cursor = self.post_conn.cursor()
        result_dict_send = []
        query_get = "SELECT id, name, logo FROM food_service;"
        post_cursor.execute(query_get)
        for result in post_cursor:
            result_dict = dict()
            result_dict['id'] = result[0]
            result_dict['name'] = result[1]
            post_cursor_price = self.post_conn.cursor()
            query_get_price = "SELECT price_range FROM food_service_additional_info WHERE food_service_id = " + str(result[0])
            post_cursor_price.execute(query_get_price)
            for delivery_type in post_cursor_price:
                if delivery_type[0] < 0.33:
                    result_dict['price_eco'] = True
                    result_dict['price_mid'] = False
                    result_dict['price_expensive'] = False
                elif 0.33 < delivery_type[0] < 0.66:
                    result_dict['price_eco'] = False
                    result_dict['price_mid'] = True
                    result_dict['price_expensive'] = False
                elif 0.66 < delivery_type[0]:
                    result_dict['price_eco'] = False
                    result_dict['price_mid'] = False
                    result_dict['price_expensive'] = True
            post_cursor_service = self.post_conn.cursor()
            query_get_services = "SELECT delivery FROM food_service_info WHERE food_service_id = " + str(result[0])
            post_cursor_service.execute(query_get_services)
            for delivery_type in post_cursor_service:
                result_dict['service_home_delivery'] = delivery_type[0]
            post_cursor_location = self.post_conn.cursor()
            query_get_location = "SELECT address, city, latitude, longitude " \
                                 "FROM food_service_location WHERE food_service_id = " + str(result[0])
            post_cursor_location.execute(query_get_location)
            for delivery_type in post_cursor_location:
                result_dict['latitude'] = delivery_type[2]
                result_dict['longitude'] = delivery_type[3]
                result_dict['address'] = delivery_type[0]
                result_dict['city'] = delivery_type[1]
            result_dict['logo'] = result[2]
            result_dict_send.append(result_dict)
        return result_dict_send

    def menu_extraction(self):
        foods_menu_list = []
        post_cursor = self.post_conn.cursor()
        query = 'SELECT id, food_service_id FROM prepared_food_product;'
        post_cursor.execute(query)
        for results in post_cursor:
            food_menu_dict = dict()
            food_menu_dict['food_id'] = results[0]
            food_menu_dict['restaurant_id'] = results[1]
            foods_menu_list.append(food_menu_dict)
        return foods_menu_list




