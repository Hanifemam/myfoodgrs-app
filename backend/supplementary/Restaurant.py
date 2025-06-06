import matplotlib.pyplot as plt

class Restaurant(object):
    def __init__(self, connection):
        self.mysql_conn = connection

    def get_restaurant(self, restaurant_id):
        rest_dict = dict()
        my_cursor_select = self.mysql_conn.cursor(buffered=True)
        query = f"SELECT * FROM restaurants WHERE id = {restaurant_id};"
        my_cursor_select.execute(query)
        fetched = my_cursor_select.fetchone()
        rest_dict['id'] = int(fetched[0])
        rest_dict['name'] = fetched[1]
        rest_dict['price_eco'] = int(fetched[2])
        rest_dict['price_mid'] = int(fetched[3])
        rest_dict['price_expensive'] = int(fetched[4])
        if fetched[5] != None:
            rest_dict['service_home_delivery'] = int(fetched[5])
        else:
            rest_dict['service_home_delivery'] = 0
        rest_dict['latitude'] = float(fetched[6])
        rest_dict['longitude'] = float(fetched[7])
        rest_dict['address'] = fetched[8]
        rest_dict['city'] = fetched[9]
        rest_dict['logo'] = fetched[10]
        return rest_dict

    def get_restaurant_menu(self, restaurant_id):
        food_dictionary = dict()
        PIZZA = []
        PESCE = []
        INTERIORA = []
        LEGUMI = []
        VERDURE = []
        TORTELLINI = []
        FORMAGGI = []
        PASTA = []
        GNOCCHI = []
        FUNGHI = []
        CARNE = []
        RISO = []
        CROSTACEI_E_MOLLUSCHI = []
        SALUMI = []
        OTHERS = []
        my_cursor_select = self.mysql_conn.cursor(buffered=True)
        query = f"SELECT food_id FROM menu WHERE restaurant_id = {restaurant_id};"
        my_cursor_select.execute(query)
        for food_id in my_cursor_select:
            my_cursor = self.mysql_conn.cursor(buffered=True)
            query = f"SELECT id, NAME, PIZZA, PESCE, INTERIORA, LEGUMI, VERDURE, " \
                    f"TORTELLINI, FORMAGGI, PASTA, GNOCCHI, FUNGHI, CARNE, RISO, " \
                    f"CROSTACEI_E_MOLLUSCHI, SALUMI FROM foods WHERE id = {int(food_id[0])};"
            my_cursor.execute(query)
            fetched_food = my_cursor.fetchone()
            if int(fetched_food[2]) == 1:
                PIZZA.append(fetched_food[1])
            if int(fetched_food[3]) == 1:
                PESCE.append(fetched_food[1])
            if int(fetched_food[4]) == 1:
                INTERIORA.append(fetched_food[1])
            if int(fetched_food[5]) == 1:
                LEGUMI.append(fetched_food[1])
            if int(fetched_food[6]) == 1:
                VERDURE.append(fetched_food[1])
            if int(fetched_food[7]) == 1:
                TORTELLINI.append(fetched_food[1])
            if int(fetched_food[8]) == 1:
                FORMAGGI.append(fetched_food[1])
            if int(fetched_food[9]) == 1:
                PASTA.append(fetched_food[1])
            if int(fetched_food[10]) == 1:
                GNOCCHI.append(fetched_food[1])
            if int(fetched_food[11]) == 1:
                FUNGHI.append(fetched_food[1])
            if int(fetched_food[12]) == 1:
                CARNE.append(fetched_food[1])
            if int(fetched_food[13]) == 1:
                RISO.append(fetched_food[1])
            if int(fetched_food[14]) == 1:
                CROSTACEI_E_MOLLUSCHI.append(fetched_food[1])
            if int(fetched_food[15]) == 1:
                SALUMI.append(fetched_food[1])
            # else:
            #     OTHERS.append(fetched_food[1])
        food_dictionary['PIZZA'] = PIZZA
        food_dictionary['PESCE'] = PESCE
        food_dictionary['INTERIORA'] = INTERIORA
        food_dictionary['LEGUMI'] = LEGUMI
        food_dictionary['VERDURE'] = VERDURE
        food_dictionary['TORTELLINI'] = TORTELLINI
        food_dictionary['FORMAGGI'] = FORMAGGI
        food_dictionary['PASTA'] = PASTA
        food_dictionary['GNOCCHI'] = GNOCCHI
        food_dictionary['FUNGHI'] = FUNGHI
        food_dictionary['CARNE'] = CARNE
        food_dictionary['RISO'] = RISO
        food_dictionary['CROSTACEI_E_MOLLUSCHI'] = CROSTACEI_E_MOLLUSCHI
        food_dictionary['SALUMI'] = SALUMI
        return food_dictionary

    def get_restaurant_menu_id(self, restaurant_id):
        food_dictionary = dict()
        food_dictionary['id'] = restaurant_id
        PIZZA = []
        PESCE = []
        INTERIORA = []
        LEGUMI = []
        VERDURE = []
        TORTELLINI = []
        FORMAGGI = []
        PASTA = []
        GNOCCHI = []
        FUNGHI = []
        CARNE = []
        RISO = []
        CROSTACEI_E_MOLLUSCHI = []
        SALUMI = []
        OTHERS = []
        my_cursor_select = self.mysql_conn.cursor(buffered=True)
        query = f"SELECT food_id FROM menu WHERE restaurant_id = {restaurant_id};"
        my_cursor_select.execute(query)
        for food_id in my_cursor_select:
            my_cursor = self.mysql_conn.cursor(buffered=True)
            query = f"SELECT id, NAME, PIZZA, PESCE, INTERIORA, LEGUMI, VERDURE, " \
                    f"TORTELLINI, FORMAGGI, PASTA, GNOCCHI, FUNGHI, CARNE, RISO, " \
                    f"CROSTACEI_E_MOLLUSCHI, SALUMI FROM foods WHERE id = {int(food_id[0])};"
            my_cursor.execute(query)
            fetched_food = my_cursor.fetchone()
            if int(fetched_food[2]) == 1:
                PIZZA.append(fetched_food[1])
            if int(fetched_food[3]) == 1:
                PESCE.append(fetched_food[1])
            if int(fetched_food[4]) == 1:
                INTERIORA.append(fetched_food[1])
            if int(fetched_food[5]) == 1:
                LEGUMI.append(fetched_food[1])
            if int(fetched_food[6]) == 1:
                VERDURE.append(fetched_food[1])
            if int(fetched_food[7]) == 1:
                TORTELLINI.append(fetched_food[1])
            if int(fetched_food[8]) == 1:
                FORMAGGI.append(fetched_food[1])
            if int(fetched_food[9]) == 1:
                PASTA.append(fetched_food[1])
            if int(fetched_food[10]) == 1:
                GNOCCHI.append(fetched_food[1])
            if int(fetched_food[11]) == 1:
                FUNGHI.append(fetched_food[1])
            if int(fetched_food[12]) == 1:
                CARNE.append(fetched_food[1])
            if int(fetched_food[13]) == 1:
                RISO.append(fetched_food[1])
            if int(fetched_food[14]) == 1:
                CROSTACEI_E_MOLLUSCHI.append(fetched_food[1])
            if int(fetched_food[15]) == 1:
                SALUMI.append(fetched_food[1])
            # else:
            #     OTHERS.append(fetched_food[1])
        food_dictionary['PIZZA'] = PIZZA
        food_dictionary['PESCE'] = PESCE
        food_dictionary['INTERIORA'] = INTERIORA
        food_dictionary['LEGUMI'] = LEGUMI
        food_dictionary['VERDURE'] = VERDURE
        food_dictionary['TORTELLINI'] = TORTELLINI
        food_dictionary['FORMAGGI'] = FORMAGGI
        food_dictionary['PASTA'] = PASTA
        food_dictionary['GNOCCHI'] = GNOCCHI
        food_dictionary['FUNGHI'] = FUNGHI
        food_dictionary['CARNE'] = CARNE
        food_dictionary['RISO'] = RISO
        food_dictionary['CROSTACEI_E_MOLLUSCHI'] = CROSTACEI_E_MOLLUSCHI
        food_dictionary['SALUMI'] = SALUMI
        return food_dictionary


    def get_count_menu(self):
        my_cursor_select = self.mysql_conn.cursor(buffered=True)
        query = f"SELECT id FROM restaurants;"
        my_cursor_select.execute(query)
        fetched = my_cursor_select.fetchall()
        food_dictionary = dict()
        restaurant_ids = []
        for item in fetched:
            restaurant_ids.append(item[0])
        restaurant_category_dict = dict()
        for restaurant_id in restaurant_ids:
            PIZZA = []
            PESCE = []
            INTERIORA = []
            LEGUMI = []
            VERDURE = []
            TORTELLINI = []
            FORMAGGI = []
            PASTA = []
            GNOCCHI = []
            FUNGHI = []
            CARNE = []
            RISO = []
            CROSTACEI_E_MOLLUSCHI = []
            SALUMI = []
            OTHERS = []
            food_dictionary.clear()
            my_cursor_select = self.mysql_conn.cursor(buffered=True)
            query = f"SELECT food_id FROM menu WHERE restaurant_id = {restaurant_id};"
            my_cursor_select.execute(query)
            for food_id in my_cursor_select:
                my_cursor = self.mysql_conn.cursor(buffered=True)
                query = f"SELECT id, NAME, PIZZA, PESCE, INTERIORA, LEGUMI, VERDURE, " \
                        f"TORTELLINI, FORMAGGI, PASTA, GNOCCHI, FUNGHI, CARNE, RISO, " \
                        f"CROSTACEI_E_MOLLUSCHI, SALUMI FROM foods WHERE id = {int(food_id[0])};"
                my_cursor.execute(query)
                fetched_food = my_cursor.fetchone()
                if int(fetched_food[2]) == 1:
                    PIZZA.append(fetched_food[1])
                if int(fetched_food[3]) == 1:
                    PESCE.append(fetched_food[1])
                if int(fetched_food[4]) == 1:
                    INTERIORA.append(fetched_food[1])
                if int(fetched_food[5]) == 1:
                    LEGUMI.append(fetched_food[1])
                if int(fetched_food[6]) == 1:
                    VERDURE.append(fetched_food[1])
                if int(fetched_food[7]) == 1:
                    TORTELLINI.append(fetched_food[1])
                if int(fetched_food[8]) == 1:
                    FORMAGGI.append(fetched_food[1])
                if int(fetched_food[9]) == 1:
                    PASTA.append(fetched_food[1])
                if int(fetched_food[10]) == 1:
                    GNOCCHI.append(fetched_food[1])
                if int(fetched_food[11]) == 1:
                    FUNGHI.append(fetched_food[1])
                if int(fetched_food[12]) == 1:
                    CARNE.append(fetched_food[1])
                if int(fetched_food[13]) == 1:
                    RISO.append(fetched_food[1])
                if int(fetched_food[14]) == 1:
                    CROSTACEI_E_MOLLUSCHI.append(fetched_food[1])
                if int(fetched_food[15]) == 1:
                    SALUMI.append(fetched_food[1])
                # else:
                #     OTHERS.append(fetched_food[1])
            food_dictionary['PIZZA'] = PIZZA
            food_dictionary['PESCE'] = PESCE
            food_dictionary['INTERIORA'] = INTERIORA
            food_dictionary['LEGUMI'] = LEGUMI
            food_dictionary['VERDURE'] = VERDURE
            food_dictionary['TORTELLINI'] = TORTELLINI
            food_dictionary['FORMAGGI'] = FORMAGGI
            food_dictionary['PASTA'] = PASTA
            food_dictionary['GNOCCHI'] = GNOCCHI
            food_dictionary['FUNGHI'] = FUNGHI
            food_dictionary['CARNE'] = CARNE
            food_dictionary['RISO'] = RISO
            food_dictionary['CROSTACEI_E_MOLLUSCHI'] = CROSTACEI_E_MOLLUSCHI
            food_dictionary['SALUMI'] = SALUMI
            dish_counter = {}
            for category, count in food_dictionary.items():
                if len(count) == 0: 
                    continue
                if category == "FORMAGGI":
                    dish_counter["CHEESE"] = len(count)
                elif (category == "VERDURE"):
                    dish_counter["SALAD"] = len(count)
                elif (category == "FUNGHI"):
                    dish_counter["MASHROOM"] = len(count)
                elif (category == "PESCE"):
                    dish_counter["FISH"] = len(count)
                elif (category == "RISO"):
                    dish_counter["RICE"] = len(count)
                elif (category == "CARNE"):
                    dish_counter["REDMEAT"] = len(count)
                elif (category == "CROSTACEI_E_MOLLUSCHI"):
                    dish_counter["BURGER"] = len(count)
                elif (category == "GNOCCHI"):
                    dish_counter["SOUP"] = len(count)
                elif (category == "TORTELLINI"):
                    dish_counter["WHITEMEAT"] = len(count)
                elif (category == "LEGUMI"):
                    dish_counter["CHINESENOODLE"] = len(count)
                    
                # dish_counter[category] = len(count)
                
            sorted_dict = dict(sorted(dish_counter.items(), key=lambda x:x[1]))
            names = list(sorted_dict.keys())
            values = list(sorted_dict.values())
            plt.clf()
            print(names)
            print(values)
            print(len(sorted_dict))
            plt.bar(range(len(sorted_dict)), values, tick_label=names)
            plt.xticks(rotation = 90)
            plot_name = str(restaurant_id) + ".png"
            path = "./supplementary/plots/" + plot_name
            plt.savefig(path)
            plt.clf()
            category_counter = 0
            if len(food_dictionary['PIZZA']) > 0:
                        category_counter += 1
            if len(food_dictionary['PESCE']) > 0:
                        category_counter += 1
            if len(food_dictionary['INTERIORA']) > 0:
                        category_counter += 1
            if len(food_dictionary['LEGUMI']) > 0:
                        category_counter += 1
            if len(food_dictionary['VERDURE']) > 0:
                        category_counter += 1
            if len(food_dictionary['TORTELLINI']) > 0:
                        category_counter += 1
            if len(food_dictionary['FORMAGGI']) > 0:
                        category_counter += 1
            if len(food_dictionary['PASTA']) > 0:
                        category_counter += 1
            if len(food_dictionary['GNOCCHI']) > 0:
                        category_counter += 1
            if len(food_dictionary['FUNGHI']) > 0:
                        category_counter += 1
            if len(food_dictionary['CARNE']) > 0:
                        category_counter += 1
            if len(food_dictionary['RISO']) > 0:
                        category_counter += 1
            if len(food_dictionary['CROSTACEI_E_MOLLUSCHI']) > 0:
                        category_counter += 1
            if len(food_dictionary['SALUMI']) > 0:
                        category_counter += 1
            restaurant_category_dict[restaurant_id] = category_counter
        rest_counter = 0
        existing_category_counter = 0
        print(restaurant_category_dict)
        for restaurant, category_number in restaurant_category_dict.items():
            rest_counter += 1
            existing_category_counter = existing_category_counter + category_number
        print(existing_category_counter / rest_counter)
        return existing_category_counter / rest_counter

    def get_top_categories_menu(self):
        my_cursor_select = self.mysql_conn.cursor(buffered=True)
        query = f"SELECT id FROM restaurants;"
        my_cursor_select.execute(query)
        fetched = my_cursor_select.fetchall()
        food_dictionary = dict()
        restaurant_ids = []
        for item in fetched:
            restaurant_ids.append(item[0])
        restaurant_category_dict = dict()
        for restaurant_id in restaurant_ids:
            PIZZA = []
            PESCE = []
            INTERIORA = []
            LEGUMI = []
            VERDURE = []
            TORTELLINI = []
            FORMAGGI = []
            PASTA = []
            GNOCCHI = []
            FUNGHI = []
            CARNE = []
            RISO = []
            CROSTACEI_E_MOLLUSCHI = []
            SALUMI = []
            OTHERS = []
            food_dictionary.clear()
            my_cursor_select = self.mysql_conn.cursor(buffered=True)
            query = f"SELECT food_id FROM menu WHERE restaurant_id = {restaurant_id};"
            my_cursor_select.execute(query)
            for food_id in my_cursor_select:
                my_cursor = self.mysql_conn.cursor(buffered=True)
                query = f"SELECT id, NAME, PIZZA, PESCE, INTERIORA, LEGUMI, VERDURE, " \
                        f"TORTELLINI, FORMAGGI, PASTA, GNOCCHI, FUNGHI, CARNE, RISO, " \
                        f"CROSTACEI_E_MOLLUSCHI, SALUMI FROM foods WHERE id = {int(food_id[0])};"
                my_cursor.execute(query)
                fetched_food = my_cursor.fetchone()
                if int(fetched_food[2]) == 1:
                    PIZZA.append(fetched_food[1])
                if int(fetched_food[3]) == 1:
                    PESCE.append(fetched_food[1])
                if int(fetched_food[4]) == 1:
                    INTERIORA.append(fetched_food[1])
                if int(fetched_food[5]) == 1:
                    LEGUMI.append(fetched_food[1])
                if int(fetched_food[6]) == 1:
                    VERDURE.append(fetched_food[1])
                if int(fetched_food[7]) == 1:
                    TORTELLINI.append(fetched_food[1])
                if int(fetched_food[8]) == 1:
                    FORMAGGI.append(fetched_food[1])
                if int(fetched_food[9]) == 1:
                    PASTA.append(fetched_food[1])
                if int(fetched_food[10]) == 1:
                    GNOCCHI.append(fetched_food[1])
                if int(fetched_food[11]) == 1:
                    FUNGHI.append(fetched_food[1])
                if int(fetched_food[12]) == 1:
                    CARNE.append(fetched_food[1])
                if int(fetched_food[13]) == 1:
                    RISO.append(fetched_food[1])
                if int(fetched_food[14]) == 1:
                    CROSTACEI_E_MOLLUSCHI.append(fetched_food[1])
                if int(fetched_food[15]) == 1:
                    SALUMI.append(fetched_food[1])
                # else:
                #     OTHERS.append(fetched_food[1])
            food_dictionary['PIZZA'] = PIZZA
            food_dictionary['PESCE'] = PESCE
            food_dictionary['INTERIORA'] = INTERIORA
            food_dictionary['LEGUMI'] = LEGUMI
            food_dictionary['VERDURE'] = VERDURE
            food_dictionary['TORTELLINI'] = TORTELLINI
            food_dictionary['FORMAGGI'] = FORMAGGI
            food_dictionary['PASTA'] = PASTA
            food_dictionary['GNOCCHI'] = GNOCCHI
            food_dictionary['FUNGHI'] = FUNGHI
            food_dictionary['CARNE'] = CARNE
            food_dictionary['RISO'] = RISO
            food_dictionary['CROSTACEI_E_MOLLUSCHI'] = CROSTACEI_E_MOLLUSCHI
            food_dictionary['SALUMI'] = SALUMI
            category_counter = 0
            #Finding Maximum
            max_category = 0
            if len(food_dictionary['PIZZA']) > max_category:
                        max_category = len(food_dictionary['PIZZA'])
            if len(food_dictionary['PESCE'])  > max_category:
                        max_category = len(food_dictionary['PESCE'])
            if len(food_dictionary['INTERIORA'])  > max_category:
                        max_category = len(food_dictionary['INTERIORA'])
            if len(food_dictionary['LEGUMI'])  > max_category:
                        max_category = len(food_dictionary['LEGUMI'])
            if len(food_dictionary['VERDURE'])  > max_category:
                        max_category = len(food_dictionary['VERDURE'])
            if len(food_dictionary['TORTELLINI'])  > max_category:
                        max_category = len(food_dictionary['TORTELLINI'])
            if len(food_dictionary['FORMAGGI'])  > max_category:
                        max_category = len(food_dictionary['FORMAGGI'])
            if len(food_dictionary['PASTA'])  > max_category:
                        max_category = len(food_dictionary['PASTA'])
            if len(food_dictionary['GNOCCHI'])  > max_category:
                        max_category = len(food_dictionary['GNOCCHI'])
            if len(food_dictionary['FUNGHI'])  > max_category:
                        max_category = len(food_dictionary['FUNGHI'])
            if len(food_dictionary['CARNE'])  > max_category:
                        max_category = len(food_dictionary['CARNE'])
            if len(food_dictionary['RISO'])  > max_category:
                        max_category = len(food_dictionary['RISO'])
            if len(food_dictionary['CROSTACEI_E_MOLLUSCHI']) > max_category:
                        max_category = len(food_dictionary['CROSTACEI_E_MOLLUSCHI'])
            if len(food_dictionary['SALUMI']) > max_category:
                        max_category = len(food_dictionary['SALUMI'])
            #Finding top categories
            if len(food_dictionary['PIZZA']) == max_category:
                        category_counter += 1
            if len(food_dictionary['PESCE']) == max_category:
                        category_counter += 1
            if len(food_dictionary['INTERIORA'])  == max_category:
                        category_counter += 1
            if len(food_dictionary['LEGUMI'])  == max_category:
                        category_counter += 1
            if len(food_dictionary['VERDURE'])  == max_category:
                        category_counter += 1
            if len(food_dictionary['TORTELLINI'])  == max_category:
                        category_counter += 1
            if len(food_dictionary['FORMAGGI'])  == max_category:
                        category_counter += 1
            if len(food_dictionary['PASTA'])  == max_category:
                        category_counter += 1
            if len(food_dictionary['GNOCCHI'])  == max_category:
                        category_counter += 1
            if len(food_dictionary['FUNGHI'])  == max_category:
                        category_counter += 1
            if len(food_dictionary['CARNE'])  == max_category:
                        category_counter += 1
            if len(food_dictionary['RISO'])  == max_category:
                        category_counter += 1
            if len(food_dictionary['CROSTACEI_E_MOLLUSCHI'])  == max_category:
                        category_counter += 1
            if len(food_dictionary['SALUMI'])  == max_category:
                        category_counter += 1
            restaurant_category_dict[restaurant_id] = category_counter
        rest_counter = 0
        existing_category_counter = 0
        print(restaurant_category_dict)
        for restaurant, category_number in restaurant_category_dict.items():
            rest_counter += 1
            existing_category_counter = existing_category_counter + category_number
        print(existing_category_counter / rest_counter)
        return food_dictionary

    def get_least_categories_menu(self):
        my_cursor_select = self.mysql_conn.cursor(buffered=True)
        query = f"SELECT id FROM restaurants;"
        my_cursor_select.execute(query)
        fetched = my_cursor_select.fetchall()
        food_dictionary = dict()
        restaurant_ids = []
        for item in fetched:
            restaurant_ids.append(item[0])
        restaurant_category_dict = dict()
        for restaurant_id in restaurant_ids:
            PIZZA = []
            PESCE = []
            INTERIORA = []
            LEGUMI = []
            VERDURE = []
            TORTELLINI = []
            FORMAGGI = []
            PASTA = []
            GNOCCHI = []
            FUNGHI = []
            CARNE = []
            RISO = []
            CROSTACEI_E_MOLLUSCHI = []
            SALUMI = []
            OTHERS = []
            food_dictionary.clear()
            my_cursor_select = self.mysql_conn.cursor(buffered=True)
            query = f"SELECT food_id FROM menu WHERE restaurant_id = {restaurant_id};"
            my_cursor_select.execute(query)
            for food_id in my_cursor_select:
                my_cursor = self.mysql_conn.cursor(buffered=True)
                query = f"SELECT id, NAME, PIZZA, PESCE, INTERIORA, LEGUMI, VERDURE, " \
                        f"TORTELLINI, FORMAGGI, PASTA, GNOCCHI, FUNGHI, CARNE, RISO, " \
                        f"CROSTACEI_E_MOLLUSCHI, SALUMI FROM foods WHERE id = {int(food_id[0])};"
                my_cursor.execute(query)
                fetched_food = my_cursor.fetchone()
                if int(fetched_food[2]) == 1:
                    PIZZA.append(fetched_food[1])
                if int(fetched_food[3]) == 1:
                        category_counter += 1
                if int(fetched_food[4]) == 1:
                    INTERIORA.append(fetched_food[1])
                if int(fetched_food[5]) == 1:
                    LEGUMI.append(fetched_food[1])
                if int(fetched_food[6]) == 1:
                    VERDURE.append(fetched_food[1])
                if int(fetched_food[7]) == 1:
                    TORTELLINI.append(fetched_food[1])
                if int(fetched_food[8]) == 1:
                    FORMAGGI.append(fetched_food[1])
                if int(fetched_food[9]) == 1:
                    PASTA.append(fetched_food[1])
                if int(fetched_food[10]) == 1:
                    GNOCCHI.append(fetched_food[1])
                if int(fetched_food[11]) == 1:
                    FUNGHI.append(fetched_food[1])
                if int(fetched_food[12]) == 1:
                    CARNE.append(fetched_food[1])
                if int(fetched_food[13]) == 1:
                    RISO.append(fetched_food[1])
                if int(fetched_food[14]) == 1:
                    CROSTACEI_E_MOLLUSCHI.append(fetched_food[1])
                if int(fetched_food[15]) == 1:
                    SALUMI.append(fetched_food[1])
                # else:
                #     OTHERS.append(fetched_food[1])
            food_dictionary['PIZZA'] = PIZZA
            food_dictionary['PESCE'] = PESCE
            food_dictionary['INTERIORA'] = INTERIORA
            food_dictionary['LEGUMI'] = LEGUMI
            food_dictionary['VERDURE'] = VERDURE
            food_dictionary['TORTELLINI'] = TORTELLINI
            food_dictionary['FORMAGGI'] = FORMAGGI
            food_dictionary['PASTA'] = PASTA
            food_dictionary['GNOCCHI'] = GNOCCHI
            food_dictionary['FUNGHI'] = FUNGHI
            food_dictionary['CARNE'] = CARNE
            food_dictionary['RISO'] = RISO
            food_dictionary['CROSTACEI_E_MOLLUSCHI'] = CROSTACEI_E_MOLLUSCHI
            food_dictionary['SALUMI'] = SALUMI
            category_counter = 0
            #Finding Maximum
            min_category = 1000
            if 0 < len(food_dictionary['PIZZA']) < min_category:
                        min_category = len(food_dictionary['PIZZA'])
            if 0 < len(food_dictionary['PESCE'])  < min_category:
                        min_category = len(food_dictionary['PESCE'])
            if 0 < len(food_dictionary['INTERIORA'])  < min_category:
                        min_category = len(food_dictionary['INTERIORA'])
            if 0 < len(food_dictionary['LEGUMI'])  < min_category:
                        min_category = len(food_dictionary['LEGUMI'])
            if 0 < len(food_dictionary['VERDURE'])  < min_category:
                        min_category = len(food_dictionary['VERDURE'])
            if 0 < len(food_dictionary['TORTELLINI'])  < min_category:
                        min_category = len(food_dictionary['TORTELLINI'])
            if 0 < len(food_dictionary['FORMAGGI'])  < min_category:
                        min_category = len(food_dictionary['FORMAGGI'])
            if 0 < len(food_dictionary['PASTA'])  < min_category:
                        min_category = len(food_dictionary['PASTA'])
            if 0 < len(food_dictionary['GNOCCHI'])  < min_category:
                        min_category = len(food_dictionary['GNOCCHI'])
            if 0 < len(food_dictionary['FUNGHI'])  < min_category:
                        min_category = len(food_dictionary['FUNGHI'])
            if 0 < len(food_dictionary['CARNE'])  < min_category:
                        min_category = len(food_dictionary['CARNE'])
            if 0 < len(food_dictionary['RISO'])  < min_category:
                        min_category = len(food_dictionary['RISO'])
            if 0 < len(food_dictionary['CROSTACEI_E_MOLLUSCHI']) < min_category:
                        min_category = len(food_dictionary['CROSTACEI_E_MOLLUSCHI'])
            if 0 < len(food_dictionary['SALUMI']) < min_category:
                        min_category = len(food_dictionary['SALUMI'])
            #Finding top categories
            if len(food_dictionary['PIZZA']) == min_category:
                        category_counter += 1
            if len(food_dictionary['PESCE']) == min_category:
                        category_counter += 1
            if len(food_dictionary['INTERIORA'])  == min_category:
                        category_counter += 1
            if len(food_dictionary['LEGUMI'])  == min_category:
                        category_counter += 1
            if len(food_dictionary['VERDURE'])  == min_category:
                        category_counter += 1
            if len(food_dictionary['TORTELLINI'])  == min_category:
                        category_counter += 1
            if len(food_dictionary['FORMAGGI'])  == min_category:
                        category_counter += 1
            if len(food_dictionary['PASTA'])  == min_category:
                        category_counter += 1
            if len(food_dictionary['GNOCCHI'])  == min_category:
                        category_counter += 1
            if len(food_dictionary['FUNGHI'])  == min_category:
                        category_counter += 1
            if len(food_dictionary['CARNE'])  == min_category:
                        category_counter += 1
            if len(food_dictionary['RISO'])  == min_category:
                        category_counter += 1
            if len(food_dictionary['CROSTACEI_E_MOLLUSCHI'])  == min_category:
                        category_counter += 1
            if len(food_dictionary['SALUMI'])  == min_category:
                        category_counter += 1
            restaurant_category_dict[restaurant_id] = category_counter
        rest_counter = 0
        existing_category_counter = 0
        print(restaurant_category_dict)
        for restaurant, category_number in restaurant_category_dict.items():
            rest_counter += 1
            existing_category_counter = existing_category_counter + category_number
        print(existing_category_counter / rest_counter)
        return food_dictionary













