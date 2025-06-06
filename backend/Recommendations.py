import decimal
import json
import pickle
from geopy.distance import geodesic
from Explanations import Explanations
from GroupModel import GroupModel
from Supplementary import Supplementary
from Users import Users
import collections
import math


class Recommendations(object):
    def __init__(self, connection_post, connection_mysql):
        self.mysql_conn = connection_mysql
        self.post_conn = connection_post

    def popularity(self, group_id):
        restaurant_json = []
        popularity_dict = dict()
        my_cursor = self.mysql_conn.cursor()
        query = "SELECT restaurant_id, COUNT(restaurant_id) FROM bookmarks GROUP BY restaurant_id;"
        my_cursor.execute(query)
        for restaurant in my_cursor:
            popularity_dict[restaurant[0]] = restaurant[1]
        popularity_dict = dict(sorted(popularity_dict.items(), key=lambda item: item[1], reverse=True))
        for restaurant_id, popularity in popularity_dict.items():
            query = f"SELECT * FROM restaurants WHERE  id = {int(restaurant_id)};"
            my_cursor.execute(query)
            row_headers = [x[0] for x in my_cursor.description]
            restaurant_info = my_cursor.fetchone()
            restaurant_info_list = []
            if restaurant_info is not None:
                for item in restaurant_info:
                    if isinstance(item, bytearray) or isinstance(item, decimal.Decimal):
                        restaurant_info_list.append(int(item))
                    else:
                        restaurant_info_list.append(item)
            restaurant_json.append(json.dumps(dict(zip(row_headers, restaurant_info_list))))
        restaurant_json_filtered = self.recomm_filtering(group_id, restaurant_json)
        return restaurant_json_filtered
    
    def popularity_without_filtering(self, group_id):
        restaurant_json = []
        popularity_dict = dict()
        my_cursor = self.mysql_conn.cursor()
        query = "SELECT restaurant_id, COUNT(restaurant_id) FROM bookmarks GROUP BY restaurant_id;"
        my_cursor.execute(query)
        for restaurant in my_cursor:
            popularity_dict[restaurant[0]] = restaurant[1]
        popularity_dict = dict(sorted(popularity_dict.items(), key=lambda item: item[1], reverse=True))
        for restaurant_id, popularity in popularity_dict.items():
            query = f"SELECT * FROM restaurants WHERE  id = {int(restaurant_id)};"
            my_cursor.execute(query)
            row_headers = [x[0] for x in my_cursor.description]
            restaurant_info = my_cursor.fetchone()
            restaurant_info_list = []
            if restaurant_info is not None:
                for item in restaurant_info:
                    if isinstance(item, bytearray) or isinstance(item, decimal.Decimal):
                        restaurant_info_list.append(int(item))
                    else:
                        restaurant_info_list.append(item)
            restaurant_json.append(json.dumps(dict(zip(row_headers, restaurant_info_list))))
        return restaurant_json

    def relevance(self, group_id):
        flag = True
        restaurant_ids = []
        restaurant_json = []
        user_list = []
        member_preference_dict = dict()
        user_relevance_dict = dict()
        my_cursor = self.mysql_conn.cursor(buffered=True)
        query = f"SELECT id FROM user WHERE group_id = {group_id};"
        my_cursor.execute(query)
        for user in my_cursor:
            user_list.append(int(user[0]))
        my_cursor = self.mysql_conn.cursor(buffered=True)
        for user in user_list:
            user_preference = []
            query = f"SELECT id, PASTA, CARNE, PIZZA, TORTELLINI, SALUMI, PESCE, " \
                    f"LEGUMI, FUNGHI, CROSTACEI_E_MOLLUSCHI, VERDURE, GNOCCHI, " \
                    f"INTERIORA, FORMAGGI, RISO FROM preference WHERE user_id = {user};"
            my_cursor.execute(query)
            fetched = my_cursor.fetchone()
            if fetched != None:
                if int(fetched[1]):
                    user_preference.append("PASTA")
                if int(fetched[2]):
                    user_preference.append("CARNE")
                if int(fetched[3]):
                    user_preference.append("PIZZA")
                if int(fetched[4]):
                    user_preference.append("TORTELLINI")
                if int(fetched[5]):
                    user_preference.append("SALUMI")
                if int(fetched[6]):
                    user_preference.append("PESCE")
                if int(fetched[7]):
                    user_preference.append("LEGUMI")
                if int(fetched[8]):
                    user_preference.append("FUNGHI")
                if int(fetched[9]):
                    user_preference.append("CROSTACEI_E_MOLLUSCHI")
                if int(fetched[10]):
                    user_preference.append("VERDURE")
                if int(fetched[11]):
                    user_preference.append("GNOCCHI")
                if int(fetched[12]):
                    user_preference.append("INTERIORA")
                if int(fetched[13]):
                    user_preference.append("FORMAGGI")
                if int(fetched[14]):
                    user_preference.append("RISO")
                member_preference_dict[user] = user_preference
        for user, preference in member_preference_dict.items():
            relevance_score = dict()
            if len(preference) > 0:
                preference_counter = 0
                for item in preference:
                    preference_counter +=  1
                    if len(relevance_score)  == 0:
                        relevance_score = Supplementary(self.post_conn, self.mysql_conn).relevance_score_for_recom(preference=item)
                    else:
                        a_counter = Supplementary(self.post_conn, self.mysql_conn).relevance_score_for_recom(preference=item)
                        b_counter = relevance_score
                        for key, value in a_counter.items():
                            relevance_score[key] = max(value, b_counter[key])
                            b_counter[key] = relevance_score[key]
                restaurant_ids = list(relevance_score.keys())
                temp_dict = dict()
                for key, value in relevance_score.items():
                    # temp_dict[key] = value / preference_counter
                    temp_dict[key] = value
                    # temp_dict[key] = math.log10(value * 9 + 1)  #Maping between [1,10] and using log10
                user_relevance_dict[user] = temp_dict
            else:
                continue
        # user_relevance = Explanations(self.mysql_conn).attractiveness(user_relevance_dict)
        if flag:
            group_relevance_dict = dict.fromkeys(restaurant_ids, 0)
            flag = False
        for key, item in group_relevance_dict.items():
            for user_key, user_value in user_relevance_dict.items():
                group_relevance_dict[key] = group_relevance_dict[key] + user_value[key]
        group_relevance_sorted = dict(sorted(group_relevance_dict.items(), key=lambda item: item[1], reverse=True))
        for index, user_relevance_loop in group_relevance_sorted.items():
            query = f"SELECT * FROM restaurants WHERE  id = {int(index)};"
            my_cursor.execute(query)
            row_headers = [x[0] for x in my_cursor.description]
            restaurant_info = my_cursor.fetchone()
            restaurant_info_list = []
            if restaurant_info is not None:
                for item in restaurant_info:
                    if isinstance(item, bytearray) or isinstance(item, decimal.Decimal):
                        restaurant_info_list.append(int(item))
                    else:
                        restaurant_info_list.append(item)
                restaurant_json.append(json.dumps(dict(zip(row_headers, restaurant_info_list))))
        restaurant_json_filtered = self.recomm_filtering(group_id, restaurant_json)
        return restaurant_json_filtered

    def relevance_without_filtering(self, group_id):
        flag = True
        restaurant_ids = []
        restaurant_json = []
        user_list = []
        member_preference_dict = dict()
        user_relevance_dict = dict()
        my_cursor = self.mysql_conn.cursor(buffered=True)
        query = f"SELECT id FROM user WHERE group_id = {group_id};"
        my_cursor.execute(query)
        for user in my_cursor:
            user_list.append(int(user[0]))
        my_cursor = self.mysql_conn.cursor(buffered=True)
        for user in user_list:
            user_preference = []
            query = f"SELECT id, PASTA, CARNE, PIZZA, TORTELLINI, SALUMI, PESCE, " \
                    f"LEGUMI, FUNGHI, CROSTACEI_E_MOLLUSCHI, VERDURE, GNOCCHI, " \
                    f"INTERIORA, FORMAGGI, RISO FROM preference WHERE user_id = {user};"
            my_cursor.execute(query)
            fetched = my_cursor.fetchone()
            if fetched != None:
                if int(fetched[1]):
                    user_preference.append("PASTA")
                if int(fetched[2]):
                    user_preference.append("CARNE")
                if int(fetched[3]):
                    user_preference.append("PIZZA")
                if int(fetched[4]):
                    user_preference.append("TORTELLINI")
                if int(fetched[5]):
                    user_preference.append("SALUMI")
                if int(fetched[6]):
                    user_preference.append("PESCE")
                if int(fetched[7]):
                    user_preference.append("LEGUMI")
                if int(fetched[8]):
                    user_preference.append("FUNGHI")
                if int(fetched[9]):
                    user_preference.append("CROSTACEI_E_MOLLUSCHI")
                if int(fetched[10]):
                    user_preference.append("VERDURE")
                if int(fetched[11]):
                    user_preference.append("GNOCCHI")
                if int(fetched[12]):
                    user_preference.append("INTERIORA")
                if int(fetched[13]):
                    user_preference.append("FORMAGGI")
                if int(fetched[14]):
                    user_preference.append("RISO")
                member_preference_dict[user] = user_preference
        for user, preference in member_preference_dict.items():
            relevance_score = dict()
            if len(preference) > 0:
                preference_counter = 0
                for item in preference:
                    preference_counter +=  1
                    if len(relevance_score)  == 0:
                        relevance_score = Supplementary(self.post_conn, self.mysql_conn).relevance_score_for_recom(preference=item)
                    else:
                        a_counter = Supplementary(self.post_conn, self.mysql_conn).relevance_score_for_recom(preference=item)
                        b_counter = relevance_score
                        for key, value in a_counter.items():
                            relevance_score[key] = max(value, b_counter[key])
                            b_counter[key] = relevance_score[key]
                restaurant_ids = list(relevance_score.keys())
                temp_dict = dict()
                for key, value in relevance_score.items():
                    # temp_dict[key] = value / preference_counter
                    temp_dict[key] = value
                    # temp_dict[key] = math.log10(value * 9 + 1)  #Maping between [1,10] and using log10
                user_relevance_dict[user] = temp_dict
            else:
                continue
        # user_relevance = Explanations(self.mysql_conn).attractiveness(user_relevance_dict)
        if flag:
            group_relevance_dict = dict.fromkeys(restaurant_ids, 0)
            flag = False
        for key, item in group_relevance_dict.items():
            for user_key, user_value in user_relevance_dict.items():
                group_relevance_dict[key] = group_relevance_dict[key] + user_value[key]
        group_relevance_sorted = dict(sorted(group_relevance_dict.items(), key=lambda item: item[1], reverse=True))
        for index, user_relevance_loop in group_relevance_sorted.items():
            query = f"SELECT * FROM restaurants WHERE  id = {int(index)};"
            my_cursor.execute(query)
            row_headers = [x[0] for x in my_cursor.description]
            restaurant_info = my_cursor.fetchone()
            restaurant_info_list = []
            if restaurant_info is not None:
                for item in restaurant_info:
                    if isinstance(item, bytearray) or isinstance(item, decimal.Decimal):
                        restaurant_info_list.append(int(item))
                    else:
                        restaurant_info_list.append(item)
                restaurant_json.append(json.dumps(dict(zip(row_headers, restaurant_info_list))))
        return restaurant_json


    def critiquing(self, group_model: GroupModel, group_id):
        group_dict = group_model.dict()
        relevance_restaurant = self.relevance(group_id)
        sucessful_restaurants = dict()
        for restaurant in relevance_restaurant.keys():
            query = f"SELECT * FROM restaurant WHERE id = {restaurant}"
            mysql_cursor = self.mysql_conn.cursor()
            mysql_cursor.execute(query)
            fetched = mysql_cursor.fetchone()
            if int(group_dict["price_expensive"]) == int(fetched[4]):
                if int(group_dict["service_home_delivery"]) == int(fetched[0]):
                    if int(group_dict["distance"]) > int(fetched[1]):
                        sucessful_restaurants[restaurant] = group_dict[restaurant]
            if int(group_dict["price_mid"]) == int(fetched[3]):
                if int(group_dict["service_home_delivery"]) == int(fetched[0]):
                    if int(group_dict["distance"]) > fetched[1]:
                        sucessful_restaurants[restaurant] = group_dict[restaurant]
            if int(group_dict["price_mid"]) == int(fetched[2]):
                if int(group_dict["service_home_delivery"]) == int(fetched[0]):
                    if int(group_dict["distance"]) > int(fetched[1]):
                        sucessful_restaurants[restaurant] = group_dict[restaurant]
        return sucessful_restaurants

    def recomm_filtering(self, group_id, recomms):
        user_loc_dict = self.get_members_location(group_id)
        if int(group_id) < 1:
            return recomms
        filtered_list = []
        query = f"SELECT distance, " \
                f"price_eco, " \
                f"price_mid, " \
                f"price_expensive, " \
                f"service_home_delivery " \
                f"FROM mygroups WHERE id = {group_id}"
        mysql_cursor = self.mysql_conn.cursor()
        mysql_cursor.execute(query)
        fetched = mysql_cursor.fetchone()
        user_location = Users.get_users_location(self, group_id)
        counter = 0
        for rest in recomms:
            counter +=1
            dist_sum = 0
            counter = 0
            rest_dict = json.loads(rest)
            if len(rest_dict) == 0:
                continue
            coordination_rest = [rest_dict['latitude'], rest_dict['longitude']]
            user_distance_dict = dict()
            user_distance_list = []
            for item in user_loc_dict.items():
                user_distance_dict[item[0]] = geodesic(coordination_rest, item[1]).meters
                user_distance_list.append(geodesic(coordination_rest, item[1]).meters)
            for single_user_location in user_location:
                lat = float(single_user_location['latitude'])
                log = float(single_user_location['longitude'])
                coordination_user = [lat, log]
                dist_sum = dist_sum + geodesic(coordination_rest, coordination_user).meters
                counter += 1
            if counter != 0:
                avrage_distance = dist_sum / counter
            else:
                avrage_distance = dist_sum
            if fetched[4] is not None and int(fetched[4]) == 1:
                # if avrage_distance < fetched[0]: for group average
                if all(x < fetched[0] for x in user_distance_list): #for all of the users
                    if rest_dict['service_home_delivery'] == 1:
                        if int(fetched[1]) == 1:
                            if rest_dict['price_eco'] == 1:
                                filtered_list.append(rest)
                        if int(fetched[2]) == 1:
                            if rest_dict['price_mid'] == 1:
                                filtered_list.append(rest)
                        if int(fetched[3]) == 1:
                            if rest_dict['price_expensive'] == 1:
                                filtered_list.append(rest)

            else:
                # if avrage_distance < fetched[0]: for group average
                if all(x < fetched[0] for x in user_distance_list): #for all of the users
                    if int(fetched[1]) == 1:
                        if rest_dict['price_eco'] == 1:
                            filtered_list.append(rest)
                    if int(fetched[2]) == 1:
                        if rest_dict['price_mid'] == 1:
                            filtered_list.append(rest)
                    if int(fetched[3]) == 1:
                        if rest_dict['price_expensive'] == 1:
                            filtered_list.append(rest)
            # filter_set = set(filtered_list)
            # filtered_list = list(filter_set)
        return filtered_list

    def group_choice(self, group_id):
        pass

    def get_members_location(self, group_id):
        user_distance_dict = dict()
        query = f"SELECT id, latitude, longitude FROM user WHERE group_id = {group_id};"
        mysql_cursor = self.mysql_conn.cursor()
        mysql_cursor.execute(query)
        for user in mysql_cursor:
            temp_list = [float(user[1]), float(user[2])]
            user_distance_dict[user[0]] = temp_list
        return user_distance_dict

        
        

