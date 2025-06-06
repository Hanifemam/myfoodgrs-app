import numpy as np
from Supplementary import Supplementary
import collections
import math
import json
import PreferenceModel

class Explanations(object):
    def __init__(self, connection_post, connection_mysql):
        self.mysql_conn = connection_mysql
        self.post_conn = connection_post

    def attractiveness(self, group_id):
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
        relevance_score = 0
        for user, preference in member_preference_dict.items():
            relevance_score_normalized = dict()
            if (len(preference) > 0):
                relevance_score = dict()
                for item in preference:
                    if len(relevance_score)  == 0:
                        relevance_score = Supplementary(self.post_conn, self.mysql_conn).relevance_score(preference=item)
                    else:
                        a_counter = Supplementary(self.post_conn, self.mysql_conn).relevance_score(preference=item)
                        b_counter = relevance_score
                        for key, value in a_counter.items():
                            # relevance_score[key] = value + b_counter[key]
                            relevance_score[key] = max(value, b_counter[key])
                            b_counter[key] = relevance_score[key]
                    # relevance_score = relevance_score + Supplementary(self.post_conn, self.mysql_conn).relevance_score(preference=item)
                # user_relevance_dict[user] = relevance_score
                max_val = relevance_score[max(relevance_score, key=relevance_score.get)]
                min_val = relevance_score[min(relevance_score, key=relevance_score.get)]
                for k, value in relevance_score.items():
                    if max_val - min_val == 0:
                        relevance_score_normalized[k] = value
                        # relevance_score_normalized[k] = math.log10(1 * 9 + 1)  #Maping between [1,10] and using log10
                    else:
                        # relevance_score_normalized[k] = math.log10(((value - min_val) / (max_val - min_val) * 9) + 1)  #Maping between [1,10] and using log10
                        # relevance_score_normalized[k] = (value - min_val) / (max_val - min_val)
                        relevance_score_normalized[k] = value
                relevance_score_normalized = dict(sorted(relevance_score_normalized.items(), key=lambda item: item[1], reverse=True))
                user_relevance_dict[user] = relevance_score_normalized
        return user_relevance_dict

    def get_similarity_explanation(self, group_rest_info):
        query = f"SELECT sim FROM similarity_explan WHERE group_id = {group_rest_info['groupId']} AND restaurant_id = {group_rest_info['restaurantId']}"
        cursor = self.mysql_conn.cursor(buffered=True)
        cursor.execute(query)
        fetch = cursor.fetchone()
        return json.loads(fetch[0])

    def similarity(self, group_rest_info):
        query_delete = f"DELETE FROM similarity_explan WHERE group_id = {group_rest_info['groupId']} AND restaurant_id = {group_rest_info['restaurantId']}"
        cursor_user_delete = self.mysql_conn.cursor(buffered=True)
        cursor_user_delete.execute(query_delete)
        group_id = group_rest_info['groupId']
        restaurant_id = group_rest_info['restaurantId']
        similarity_list = []
        user_preference_current = []
        user_list_current = []
        query_user = f"SELECT id FROM user WHERE group_id = {group_id}"
        cursor_user = self.mysql_conn.cursor(buffered=True)
        cursor_user.execute(query_user)
        group_preference_dict = dict()
        number_of_liked_group = 0
        for user in cursor_user:
            user_list_current.append(int(user[0]))
        for user in user_list_current:
            my_cursor = self.mysql_conn.cursor(buffered=True)
            query = f"SELECT id, PASTA, CARNE, PIZZA, TORTELLINI, SALUMI, PESCE, " \
                    f"LEGUMI, FUNGHI, CROSTACEI_E_MOLLUSCHI, VERDURE, GNOCCHI, " \
                    f"INTERIORA, FORMAGGI, RISO FROM preference WHERE user_id = {user};"
            my_cursor.execute(query)
            fetched = my_cursor.fetchone()
            if fetched != None:
                if int(fetched[1]):
                    group_preference_dict["PASTA"] = 0
                    user_preference_current.append("PASTA")
                if int(fetched[2]):
                    group_preference_dict["CARNE"] = 0
                    user_preference_current.append("CARNE")
                if int(fetched[3]):
                    group_preference_dict["PIZZA"] = 0
                    user_preference_current.append("PIZZA")
                if int(fetched[4]):
                    group_preference_dict["TORTELLINI"] = 0
                    user_preference_current.append("TORTELLINI")
                if int(fetched[5]):
                    group_preference_dict["SALUMI"] = 0
                    user_preference_current.append("SALUMI")
                if int(fetched[6]):
                    group_preference_dict["PESCE"] = 0
                    user_preference_current.append("PESCE")
                if int(fetched[7]):
                    group_preference_dict["LEGUMI"] = 0
                    user_preference_current.append("LEGUMI")
                if int(fetched[8]):
                    group_preference_dict["FUNGHI"] = 0
                    user_preference_current.append("FUNGHI")
                if int(fetched[9]):
                    group_preference_dict["CROSTACEI_E_MOLLUSCHI"] = 0
                    user_preference_current.append("CROSTACEI_E_MOLLUSCHI")
                if int(fetched[10]):
                    group_preference_dict["VERDURE"] = 0
                    user_preference_current.append("VERDURE")
                if int(fetched[11]):
                    group_preference_dict["GNOCCHI"] = 0
                    user_preference_current.append("GNOCCHI")
                if int(fetched[12]):
                    group_preference_dict["INTERIORA"] = 0
                    user_preference_current.append("INTERIORA")
                if int(fetched[13]):
                    group_preference_dict["FORMAGGI"] = 0
                    user_preference_current.append("FORMAGGI")
                if int(fetched[14]):
                    group_preference_dict["RISO"] = 0
                    user_preference_current.append("RISO")
        query = f"SELECT group_id FROM bookmarks WHERE restaurant_id = {restaurant_id} AND group_id != {group_id} ORDER BY id DESC LIMIT 30 "
        # ToDo Remove for slower but more percise
        cursor = self.mysql_conn.cursor(buffered=True)
        cursor.execute(query)
        for group in cursor:
            number_of_liked_group += 1
            user_list = []
            bookmarked_group_id = int(group[0])
            query_user = f"SELECT id FROM user WHERE group_id = {bookmarked_group_id}"
            cursor_user_others = self.mysql_conn.cursor(buffered=True)
            cursor_user_others.execute(query_user)
            for user in cursor_user_others:
                user_list.append(int(user[0]))
            user_preference_others = []
            for user in user_list:
                my_cursor = self.mysql_conn.cursor(buffered=True)
                query = f"SELECT id, PASTA, CARNE, PIZZA, TORTELLINI, SALUMI, PESCE, " \
                        f"LEGUMI, FUNGHI, CROSTACEI_E_MOLLUSCHI, VERDURE, GNOCCHI, " \
                        f"INTERIORA, FORMAGGI, RISO FROM preference WHERE user_id = {user};"
                my_cursor.execute(query)
                fetched = my_cursor.fetchone()
                if fetched != None:
                    if int(fetched[1]):
                        user_preference_others.append("PASTA")
                    if int(fetched[2]):
                        user_preference_others.append("CARNE")
                    if int(fetched[3]):
                        user_preference_others.append("PIZZA")
                    if int(fetched[4]):
                        user_preference_others.append("TORTELLINI")
                    if int(fetched[5]):
                        user_preference_others.append("SALUMI")
                    if int(fetched[6]):
                        user_preference_others.append("PESCE")
                    if int(fetched[7]):
                        user_preference_others.append("LEGUMI")
                    if int(fetched[8]):
                        user_preference_others.append("FUNGHI")
                    if int(fetched[9]):
                        user_preference_others.append("CROSTACEI_E_MOLLUSCHI")
                    if int(fetched[10]):
                        user_preference_others.append("VERDURE")
                    if int(fetched[11]):
                        user_preference_others.append("GNOCCHI")
                    if int(fetched[12]):
                        user_preference_others.append("INTERIORA")
                    if int(fetched[13]):
                        user_preference_others.append("FORMAGGI")
                    if int(fetched[14]):
                        user_preference_others.append("RISO")
            for item in set(user_preference_others):
                if item in set(group_preference_dict.keys()):
                    group_preference_dict[item] += 1
            user_preference_others_set = user_preference_others
            user_preference_current_set = user_preference_current
            intersection = len(list(set(user_preference_others_set).intersection(user_preference_current_set)))
            union = (len(set(user_preference_others_set)) + len(set(user_preference_current_set))) - intersection
            if union != 0:
                if float(intersection) / union > 0.6:
                    similarity_list.append(float(intersection) / union)
                # similarity_list.append(float(intersection) / union)
            else:
                similarity_list.append(0)
        for key in group_preference_dict.keys():
            group_preference_dict[key] = group_preference_dict[key] / number_of_liked_group
        json_object = str(json.dumps(group_preference_dict))
        group_id_int = int(group_rest_info['groupId'])
        group_rest_int = int(group_rest_info["restaurantId"])
        query_submit = f"INSERT INTO similarity_explan (group_id, sim, restaurant_id) VALUES ({group_id_int}," + f"'{json_object}'" + f", { group_rest_int})"
        cursor_user_submit = self.mysql_conn.cursor(buffered=True)
        cursor_user_submit.execute(query_submit)
        if(len(similarity_list) == 0):
            return 0
        else: 
            return np.sum(similarity_list) / number_of_liked_group
        
    def similarity_group(self, group_rest_info):
        print("similarity_group")
        rest_similarity_dict = dict()
        for rest in group_rest_info['restaurantId']:
            query_delete = f"DELETE FROM similarity_explan WHERE group_id = {group_rest_info['groupId']} AND restaurant_id = {rest}"
            cursor_user_delete = self.mysql_conn.cursor(buffered=True)
            cursor_user_delete.execute(query_delete)
            group_id = group_rest_info['groupId']
            restaurant_id = rest
            similarity_list = []
            user_preference_current = []
            user_list_current = []
            query_user = f"SELECT id FROM user WHERE group_id = {group_id}"
            cursor_user = self.mysql_conn.cursor(buffered=True)
            cursor_user.execute(query_user)
            group_preference_dict = dict()
            number_of_liked_group = 0
            for user in cursor_user:
                user_list_current.append(int(user[0]))
            for user in user_list_current:
                my_cursor = self.mysql_conn.cursor(buffered=True)
                query = f"SELECT id, PASTA, CARNE, PIZZA, TORTELLINI, SALUMI, PESCE, " \
                        f"LEGUMI, FUNGHI, CROSTACEI_E_MOLLUSCHI, VERDURE, GNOCCHI, " \
                        f"INTERIORA, FORMAGGI, RISO FROM preference WHERE user_id = {user};"
                my_cursor.execute(query)
                fetched = my_cursor.fetchone()
                if fetched != None:
                    if int(fetched[1]):
                        group_preference_dict["PASTA"] = 0
                        user_preference_current.append("PASTA")
                    if int(fetched[2]):
                        group_preference_dict["CARNE"] = 0
                        user_preference_current.append("CARNE")
                    if int(fetched[3]):
                        group_preference_dict["PIZZA"] = 0
                        user_preference_current.append("PIZZA")
                    if int(fetched[4]):
                        group_preference_dict["TORTELLINI"] = 0
                        user_preference_current.append("TORTELLINI")
                    if int(fetched[5]):
                        group_preference_dict["SALUMI"] = 0
                        user_preference_current.append("SALUMI")
                    if int(fetched[6]):
                        group_preference_dict["PESCE"] = 0
                        user_preference_current.append("PESCE")
                    if int(fetched[7]):
                        group_preference_dict["LEGUMI"] = 0
                        user_preference_current.append("LEGUMI")
                    if int(fetched[8]):
                        group_preference_dict["FUNGHI"] = 0
                        user_preference_current.append("FUNGHI")
                    if int(fetched[9]):
                        group_preference_dict["CROSTACEI_E_MOLLUSCHI"] = 0
                        user_preference_current.append("CROSTACEI_E_MOLLUSCHI")
                    if int(fetched[10]):
                        group_preference_dict["VERDURE"] = 0
                        user_preference_current.append("VERDURE")
                    if int(fetched[11]):
                        group_preference_dict["GNOCCHI"] = 0
                        user_preference_current.append("GNOCCHI")
                    if int(fetched[12]):
                        group_preference_dict["INTERIORA"] = 0
                        user_preference_current.append("INTERIORA")
                    if int(fetched[13]):
                        group_preference_dict["FORMAGGI"] = 0
                        user_preference_current.append("FORMAGGI")
                    if int(fetched[14]):
                        group_preference_dict["RISO"] = 0
                        user_preference_current.append("RISO")
            query = f"SELECT group_id FROM bookmarks WHERE restaurant_id = {restaurant_id} AND group_id != {group_id} ORDER BY id DESC LIMIT 30 "
            # ToDo Remove for slower but more percise
            cursor = self.mysql_conn.cursor(buffered=True)
            cursor.execute(query)
            for group in cursor:
                number_of_liked_group += 1
                user_list = []
                bookmarked_group_id = int(group[0])
                query_user = f"SELECT id FROM user WHERE group_id = {bookmarked_group_id}"
                cursor_user_others = self.mysql_conn.cursor(buffered=True)
                cursor_user_others.execute(query_user)
                for user in cursor_user_others:
                    user_list.append(int(user[0]))
                user_preference_others = []
                for user in user_list:
                    my_cursor = self.mysql_conn.cursor(buffered=True)
                    query = f"SELECT id, PASTA, CARNE, PIZZA, TORTELLINI, SALUMI, PESCE, " \
                            f"LEGUMI, FUNGHI, CROSTACEI_E_MOLLUSCHI, VERDURE, GNOCCHI, " \
                            f"INTERIORA, FORMAGGI, RISO FROM preference WHERE user_id = {user};"
                    my_cursor.execute(query)
                    fetched = my_cursor.fetchone()
                    if fetched != None:
                        if int(fetched[1]):
                            user_preference_others.append("PASTA")
                        if int(fetched[2]):
                            user_preference_others.append("CARNE")
                        if int(fetched[3]):
                            user_preference_others.append("PIZZA")
                        if int(fetched[4]):
                            user_preference_others.append("TORTELLINI")
                        if int(fetched[5]):
                            user_preference_others.append("SALUMI")
                        if int(fetched[6]):
                            user_preference_others.append("PESCE")
                        if int(fetched[7]):
                            user_preference_others.append("LEGUMI")
                        if int(fetched[8]):
                            user_preference_others.append("FUNGHI")
                        if int(fetched[9]):
                            user_preference_others.append("CROSTACEI_E_MOLLUSCHI")
                        if int(fetched[10]):
                            user_preference_others.append("VERDURE")
                        if int(fetched[11]):
                            user_preference_others.append("GNOCCHI")
                        if int(fetched[12]):
                            user_preference_others.append("INTERIORA")
                        if int(fetched[13]):
                            user_preference_others.append("FORMAGGI")
                        if int(fetched[14]):
                            user_preference_others.append("RISO")
                for item in set(user_preference_others):
                    if item in set(group_preference_dict.keys()):
                        group_preference_dict[item] += 1
                user_preference_others_set = user_preference_others
                user_preference_current_set = user_preference_current
                intersection = len(list(set(user_preference_others_set).intersection(user_preference_current_set)))
                union = (len(set(user_preference_others_set)) + len(set(user_preference_current_set))) - intersection
                if union != 0:
                    similarity_list.append(float(intersection) / union)
                else:
                    similarity_list.append(0)
            for key in group_preference_dict.keys():
                group_preference_dict[key] = group_preference_dict[key] / number_of_liked_group
            json_object = str(json.dumps(group_preference_dict))
            group_id_int = int(group_rest_info['groupId'])
            group_rest_int = int(rest)
            query_submit = f"INSERT INTO similarity_explan (group_id, sim, restaurant_id) VALUES ({group_id_int}," + f"'{json_object}'" + f", { group_rest_int})"
            cursor_user_submit = self.mysql_conn.cursor(buffered=True)
            cursor_user_submit.execute(query_submit)
            
            if(len(similarity_list) == 0):
                rest_similarity_dict[rest] = 0

            else: 
                rest_similarity_dict[rest] = np.mean(similarity_list)
                
        return rest_similarity_dict
        
    def pupularity_dict(self, rest_id):
        restaurant_id = rest_id
        popularity_counter = 0
        max_popularity = 0
        min_popularity = 100000000
        query_user = f"SELECT COUNT(*) FROM bookmarks WHERE restaurant_id = {rest_id};"
        cursor_user = self.mysql_conn.cursor()
        cursor_user.execute(query_user)
        popularaty_of_restaurant = cursor_user.fetchone()[0]
        query_user = "SELECT DISTINCT restaurant_id FROM bookmarks;"
        cursor_user = self.mysql_conn.cursor(buffered=True)
        cursor_user.execute(query_user)
        for rest_id in cursor_user:
            query_user = f"SELECT COUNT(*) FROM bookmarks WHERE restaurant_id = {rest_id[0]};"
            cursor_user_in = self.mysql_conn.cursor(buffered=True)
            cursor_user_in.execute(query_user)
            temp_fetched = cursor_user_in.fetchone()[0]
            popularity_counter = popularity_counter + temp_fetched
            if max_popularity < temp_fetched:
                max_popularity = temp_fetched
            if min_popularity > temp_fetched:
                min_popularity = temp_fetched
        if max_popularity - min_popularity == 0:
            return popularaty_of_restaurant / max_popularity
        elif (popularaty_of_restaurant == 0):
            result_temp = dict()
            result_temp[restaurant_id] = 0
            return result_temp
        else:
            # return (popularaty_of_restaurant - min_popularity) / (max_popularity - min_popularity)
            result_temp = dict()
            result_temp[restaurant_id] = popularaty_of_restaurant / popularity_counter
            return result_temp
   
    def pupularity(self, rest_id):
        popularity_counter = 0
        max_popularity = 0
        min_popularity = 100000000
        query_user = f"SELECT COUNT(*) FROM bookmarks WHERE restaurant_id = {rest_id};"
        cursor_user = self.mysql_conn.cursor()
        cursor_user.execute(query_user)
        popularaty_of_restaurant = cursor_user.fetchone()[0]
        query_user = "SELECT DISTINCT restaurant_id FROM bookmarks;"
        cursor_user = self.mysql_conn.cursor(buffered=True)
        cursor_user.execute(query_user)
        for rest_id in cursor_user:
            query_user = f"SELECT COUNT(*) FROM bookmarks WHERE restaurant_id = {rest_id[0]};"
            cursor_user_in = self.mysql_conn.cursor(buffered=True)
            cursor_user_in.execute(query_user)
            temp_fetched = cursor_user_in.fetchone()[0]
            popularity_counter = popularity_counter + temp_fetched
            if max_popularity < temp_fetched:
                max_popularity = temp_fetched
            if min_popularity > temp_fetched:
                min_popularity = temp_fetched
        if max_popularity - min_popularity == 0:
            return popularaty_of_restaurant / max_popularity
        elif (popularaty_of_restaurant == 0):
            return 0
        else:
            # return (popularaty_of_restaurant - min_popularity) / (max_popularity - min_popularity)
            return popularaty_of_restaurant / popularity_counter

    def select_popularity(self, rest_id):
        max_popularity = 0
        min_popularity = 100000000
        query_user = f"SELECT COUNT(*) FROM selected WHERE restaurant_id = {rest_id};"
        cursor_user = self.mysql_conn.cursor()
        cursor_user.execute(query_user)
        popularaty_of_restaurant = cursor_user.fetchone()[0]
        query_user = "SELECT DISTINCT restaurant_id FROM selected;"
        cursor_user = self.mysql_conn.cursor(buffered=True)
        cursor_user.execute(query_user)
        for rest_id in cursor_user:
            query_user = f"SELECT COUNT(*) FROM selected WHERE restaurant_id = {rest_id[0]};"
            cursor_user_in = self.mysql_conn.cursor(buffered=True)
            cursor_user_in.execute(query_user)
            temp_fetched = cursor_user_in.fetchone()[0]
            if max_popularity < temp_fetched:
                max_popularity = temp_fetched
            if min_popularity > temp_fetched:
                min_popularity = temp_fetched
        if max_popularity - min_popularity == 0:
            return popularaty_of_restaurant / max_popularity
        elif (popularaty_of_restaurant == 0):
            return 0
        else:
            return (popularaty_of_restaurant - min_popularity) / (max_popularity - min_popularity)

    def get_popularity_count(self):
        query = f"SELECT * FROM popularity_counter;"
        my_cursor = self.mysql_conn.cursor(buffered=True, dictionary=True)
        my_cursor.execute(query)
        row = my_cursor.fetchone()
        del row["id"]
        return(row)