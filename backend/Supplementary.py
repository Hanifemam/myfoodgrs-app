import pickle

from ExtractFromPostgre import ExtractFromPostgre

class Supplementary(object):
    def __init__(self, connection_post, connection_mysql):
        self.connection_post = connection_post
        self.connection_mysql = connection_mysql
        self.mysql_conn = connection_mysql

    def foods_in_category(self):
        # category_set = ExtractFromPostgre(self.connection_post, self.connection_mysql).create_categories()
        category_set = {"PASTA",
        "CARNE",
        "RISO",
        "PIZZA",
        "PESCE",
        "FUNGHI",
        "VERDURE",
        "TORTELLINI",
        "FORMAGGI",
        "CROSTACEI_E_MOLLUSCHI",
        "GNOCCHI",
        "LEGUMI"}
        category_size = dict()
        cursor = self.mysql_conn.cursor()
        for category in category_set:
            query = f"SELECT COUNT(*) from foods WHERE {category.replace(' ','_')} = True"
            cursor.execute(query)
            category_size[category.replace(' ', '_')] = cursor.fetchone()[0]
        with open('supplementary/foods_category_counts.pkl', 'wb') as f:
            pickle.dump(category_size, f)

    def relevance_score(self, preference):
        restaurant_relevance_dict = dict()
        with open('supplementary/foods_category_counts.pkl', 'rb') as f:
            category_count_dict = pickle.load(f)
        # category_count_dict['CROSTACEI_E_MOLLUSCHI'] += 1
        my_cursor = self.mysql_conn.cursor(buffered=True)
        my_cursor_food = self.mysql_conn.cursor(buffered=True)
        restaurant_list = []
        query = "SELECT id FROM restaurants;"
        my_cursor.execute(query)
        for restaurant in my_cursor:
            restaurant_list.append(restaurant[0])
        for restaurant in restaurant_list:
            preference_counter = 0
            query = f"SELECT food_id FROM menu WHERE restaurant_id = {restaurant};"
            my_cursor.execute(query)
            food_counter = 0
            for food in my_cursor:
                food_counter += 1
                query = f"SELECT {preference} FROM foods WHERE id = {int(food[0])};"
                my_cursor_food.execute(query)
                result = my_cursor_food.fetchone()
                if int(result[0]):
                    preference_counter += 1
            # relevance_score = preference_counter / int(food_counter + 1)
            # restaurant_relevance_dict[restaurant] = relevance_score
            restaurant_relevance_dict[restaurant] = self.normalization(self.is_number_of_food_positive(preference_counter) * self.get_trip_score(restaurant) + self.variety_impact(preference_counter))
            # print(restaurant_relevance_dict)
        return restaurant_relevance_dict

    def relevance_score_for_recom(self, preference):
        restaurant_relevance_dict = dict()
        with open('supplementary/foods_category_counts.pkl', 'rb') as f:
            category_count_dict = pickle.load(f)
        # category_count_dict['CROSTACEI_E_MOLLUSCHI'] += 1
        my_cursor = self.mysql_conn.cursor(buffered=True)
        my_cursor_food = self.mysql_conn.cursor(buffered=True)
        restaurant_list = []
        query = "SELECT id FROM restaurants"
        my_cursor.execute(query)
        for restaurant in my_cursor:
            restaurant_list.append(restaurant[0])
        for restaurant in restaurant_list:
            restaurant_dish_counter = 0
            preference_counter = 0
            query = f"SELECT food_id FROM menu WHERE restaurant_id = {restaurant};"
            my_cursor.execute(query)
            for food in my_cursor:
                restaurant_dish_counter += 1
                query = f"SELECT {preference} FROM foods WHERE id = {int(food[0])};"
                my_cursor_food.execute(query)
                result = my_cursor_food.fetchone()
                if int(result[0]):
                    preference_counter += 1
            # relevance_score = preference_counter / int(category_count_dict[preference] + 1)
            # relevance_score = preference_counter / int(restaurant_dish_counter + 1)
            restaurant_relevance_dict[restaurant] = self.normalization(self.is_number_of_food_positive(preference_counter) * self.get_trip_score(restaurant) + self.variety_impact(preference_counter))
        return restaurant_relevance_dict
    
    def get_trip_score(self,restaurant_id):
        my_cursor = self.mysql_conn.cursor(buffered=True)
        query = f"SELECT rating FROM qualities WHERE id = {restaurant_id};"
        my_cursor.execute(query)
        result = my_cursor.fetchone()[0]
        return result
    
    def is_number_of_food_positive(self,number_of_foods):
        if number_of_foods == 0:
            return 0
        else:
            return 1
        
    def variety_impact(self, number_of_foods):
        return number_of_foods / 700
        
    def normalization(self, score):
        if score > 10:
            # return 1
            #For data prepration change it if you want to run app
            return 5
        else:
            # return score/10
            #For data prepration change it if you want to run app
            return float(f'{score/2:.1f}') 
        



