import json
import random

from GroupModel import GroupModel
from PreferenceModel import PreferenceModel
from PutInMysql import PutInMysql
from threading import Thread


class Preference(object):
    def __init__(self, connection_post, connection_mysql):
        self.mysql_conn = connection_mysql
        self.post_conn = connection_post

    def create_preference_table(self):
        my_cursor = self.mysql_conn.cursor()
        my_cursor.execute('DROP TABLE IF EXISTS preference;')
        query = 'CREATE TABLE preference (id int PRIMARY KEY UNIQUE auto_increment, user_id int, '
        category_set = PutInMysql(self.post_conn, self.mysql_conn).post_obj.create_categories()
        category_set_removed_space = set()
        for item in category_set:
            category_set_removed_space.add(item.replace(' ', '_'))
        for item in category_set_removed_space:
            query += str(item + ' ')
            query += 'BINARY, '
        query = query[:-2]
        query += ');'
        my_cursor.execute(query)

    def insert_preference(self, preference: PreferenceModel):
        new_preference = preference.dict()
        query = f'DELETE FROM preference WHERE user_id = {new_preference["user_id"]};'
        # my_cursor_delete = self.mysql_conn.cursor(buffered=True)
        my_cursor = self.mysql_conn.cursor(buffered=True)
        my_cursor.execute(query)
        query = "INSERT INTO preference (user_id, PASTA, CARNE, PIZZA, TORTELLINI, SALUMI, PESCE," \
                "LEGUMI, FUNGHI, CROSTACEI_E_MOLLUSCHI, VERDURE, GNOCCHI, INTERIORA, FORMAGGI, RISO) " \
                "VALUES (%(user_id)s, %(PASTA)s, %(CARNE)s, %(PIZZA)s, %(TORTELLINI)s, " \
                "%(SALUMI)s, %(PESCE)s, %(LEGUMI)s, %(FUNGHI)s, %(CROSTACEI_E_MOLLUSCHI)s, %(VERDURE)s," \
                "%(GNOCCHI)s, %(INTERIORA)s, %(FORMAGGI)s, %(RISO)s)"
        my_cursor.execute(query, new_preference)
        query = "SELECT last_insert_id();"
        my_cursor.execute(query)
        last_id = my_cursor.fetchone()
        self.mysql_conn.commit()
        # self.update_preference_count()
        # ToDo: this periodic
        # Thread(target=self.update_preference_count).start()
        return json.dumps({'preference_id': int(last_id[0])})

    def remove_preference(self, preference_id: int):
        my_cursor = self.mysql_conn.cursor()
        preference_to_delete = int(preference_id)
        query = f"DELETE FROM preference WHERE id={preference_to_delete};"
        my_cursor.execute(query)
        self.mysql_conn.commit()
        Thread(target=self.update_preference_count).start()
        return "DONE"

    def update_preference(self, preference: PreferenceModel, preference_id: int):
        my_cursor = self.mysql_conn.cursor()
        my_cursor_select = self.mysql_conn.cursor()
        new_preference = preference.dict()
        query = f"SELECT user_id, PASTA, CARNE, PIZZA, TORTELLINI, SALUMI, PESCE," \
                "LEGUMI, FUNGHI, CROSTACEI_E_MOLLUSCHI, VERDURE, GNOCCHI, INTERIORA, FORMAGGI, RISO " \
                f"FROM preference WHERE id = {preference_id};"
        my_cursor_select.execute(query)
        fetched = my_cursor_select.fetchone()
        if new_preference['user_id'] != fetched[0]:
            query = f"UPDATE preference SET user_id = {new_preference['user_id']} " \
                    f"WHERE id = {preference_id};"
            my_cursor.execute(query)
        if new_preference['PASTA'] != fetched[1]:
            query = f"UPDATE preference SET PASTA = {new_preference['PASTA']} " \
                    f"WHERE id = {preference_id};"
            my_cursor.execute(query)
        if new_preference['CARNE'] != fetched[2]:
            query = f"UPDATE preference SET CARNE = {new_preference['CARNE']} " \
                    f"WHERE id = {preference_id};"
            my_cursor.execute(query)
        if new_preference['TORTELLINI'] != fetched[3]:
            query = f"UPDATE preference SET TORTELLINI = {new_preference['TORTELLINI']} " \
                    f"WHERE id = {preference_id};"
            my_cursor.execute(query)
        if new_preference['SALUMI'] != fetched[4]:
            query = f"UPDATE preference SET SALUMI = {new_preference['SALUMI']} " \
                    f"WHERE id = {preference_id};"
            my_cursor.execute(query)
        if new_preference['SALUMI'] != fetched[5]:
            query = f"UPDATE preference SET PESCE = {new_preference['PESCE']} " \
                    f"WHERE id = {preference_id};"
            my_cursor.execute(query)
        if new_preference['LEGUMI'] != fetched[6]:
            query = f"UPDATE preference SET LEGUMI = {new_preference['LEGUMI']} " \
                    f"WHERE id = {preference_id};"
            my_cursor.execute(query)
        if new_preference['FUNGHI'] != fetched[7]:
            query = f"UPDATE preference SET FUNGHI = {new_preference['FUNGHI']} " \
                    f"WHERE id = {preference_id};"
            my_cursor.execute(query)
        if new_preference['CROSTACEI_E_MOLLUSCHI'] != fetched[8]:
            query = f"UPDATE preference SET CROSTACEI_E_MOLLUSCHI = {new_preference['CROSTACEI_E_MOLLUSCHI']} " \
                    f"WHERE id = {preference_id};"
            my_cursor.execute(query)
        if new_preference['VERDURE'] != fetched[9]:
            query = f"UPDATE preference SET VERDURE = {new_preference['VERDURE']} " \
                    f"WHERE id = {preference_id};"
            my_cursor.execute(query)
        if new_preference['GNOCCHI'] != fetched[10]:
            query = f"UPDATE preference SET GNOCCHI = {new_preference['GNOCCHI']} " \
                    f"WHERE id = {preference_id};"
            my_cursor.execute(query)
        if new_preference['INTERIORA'] != fetched[11]:
            query = f"UPDATE preference SET INTERIORA = {new_preference['INTERIORA']} " \
                    f"WHERE id = {preference_id};"
            my_cursor.execute(query)
        if new_preference['FORMAGGI'] != fetched[12]:
            query = f"UPDATE preference SET FORMAGGI = {new_preference['FORMAGGI']} " \
                    f"WHERE id = {preference_id};"
            my_cursor.execute(query)
        if new_preference['RISO'] != fetched[13]:
            query = f"UPDATE preference SET RISO = {new_preference['RISO']} " \
                    f"WHERE id = {preference_id};"
            my_cursor.execute(query)
        self.mysql_conn.commit()
        Thread(target=self.update_preference_count).start()
        return "Done"

    def get_preference(self, group_id):
        user_list = []
        member_preference_dict = dict()
        my_cursor_user = self.mysql_conn.cursor()
        query = f"SELECT id FROM user WHERE group_id={group_id};"
        my_cursor_user.execute(query)
        for user in my_cursor_user:
            user_list.append(user[0])
        for user in user_list:
            my_cursor = self.mysql_conn.cursor(buffered=True)
            user_preference = []
            query = f"SELECT id, PASTA, CARNE, PIZZA, TORTELLINI, SALUMI, PESCE, " \
                    f"LEGUMI, FUNGHI, CROSTACEI_E_MOLLUSCHI, VERDURE, GNOCCHI, " \
                    f"INTERIORA, FORMAGGI, RISO FROM preference WHERE user_id = {user};"
            my_cursor.execute(query)
            fetched = my_cursor.fetchone()
            if fetched is not None:
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
            else:
                member_preference_dict[user] = []
        return member_preference_dict

    def update_preference_group(self, preference: GroupModel, group_id):
        my_cursor_select = self.mysql_conn.cursor()
        new_preference = preference
        query = f"UPDATE mygroups SET distance = {new_preference['distance']}, " \
                f"price_eco = {new_preference['price_eco']}, " \
                f"price_mid = {new_preference['price_mid']}, " \
                f"price_expensive = {new_preference['price_expensive']}, " \
                f"service_home_delivery = {new_preference['service_home_delivery']} " \
                f"WHERE id = {group_id};"
        my_cursor_select.execute(query)
        self.mysql_conn.commit()
        return 1

    def update_preference_price_group(self, preference: GroupModel, group_id):
        my_cursor_select = self.mysql_conn.cursor()
        new_preference = preference
        query = f"UPDATE mygroups SET price_eco = {new_preference['price_eco']}, " \
                f"price_mid = {new_preference['price_mid']}, " \
                f"price_expensive = {new_preference['price_expensive']} " \
                f"WHERE id = {group_id};"
        my_cursor_select.execute(query)
        self.mysql_conn.commit()
        return "Done"

    def update_preference_distance_group(self, preference: GroupModel, group_id):
        my_cursor_select = self.mysql_conn.cursor()
        new_preference = preference
        query = f"UPDATE mygroups SET distance = {new_preference['distance']} " \
                f"WHERE id = {group_id};"
        my_cursor_select.execute(query)
        self.mysql_conn.commit()
        return 1

    def update_preference_delivery_group(self, preference: GroupModel, group_id):
        my_cursor_select = self.mysql_conn.cursor()
        new_preference = preference
        query = f"UPDATE mygroups SET service_home_delivery = " \
                f"{new_preference['service_home_delivery']} " \
                f"WHERE id = {group_id};"
        my_cursor_select.execute(query)
        self.mysql_conn.commit()
        return 1

    def preference_fake_data(self):
        user_list = []
        query = f"SELECT id FROM user"
        cursor = self.mysql_conn.cursor()
        cursor.execute(query)
        for user in cursor:
            user_list.append(int(user[0]))
        for user in user_list:
            preference_sample = random.choice(["PASTA", "CARNE", "PIZZA", "TORTELLINI", "PASTA", "PESCE",
                                               "LEGUMI", "FUNGHI", "CROSTACEI_E_MOLLUSCHI", "VERDURE", "GNOCCHI",
                                               "INTERIORA", "FORMAGGI", "RISO"])
            if preference_sample == "PASTA":
                self.insert_preference(PreferenceModel(user_id=user, PASTA=True))
            if preference_sample == "CARNE":
                self.insert_preference(PreferenceModel(user_id=user, CARNE=True))
            if preference_sample == "PIZZA":
                self.insert_preference(PreferenceModel(user_id=user, PIZZA=True))
            if preference_sample == "TORTELLINI":
                self.insert_preference(PreferenceModel(user_id=user, TORTELLINI=True))
            if preference_sample == "PASTA":
                self.insert_preference(PreferenceModel(user_id=user, PASTA=True))
            if preference_sample == "PESCE":
                self.insert_preference(PreferenceModel(user_id=user, PESCE=True))
            if preference_sample == "LEGUMI":
                self.insert_preference(PreferenceModel(user_id=user, LEGUMI=True))
            if preference_sample == "FUNGHI":
                self.insert_preference(PreferenceModel(user_id=user, FUNGHI=True))
            if preference_sample == "CROSTACEI_E_MOLLUSCHI":
                self.insert_preference(PreferenceModel(user_id=user, CROSTACEI_E_MOLLUSCHI=True))
            if preference_sample == "VERDURE":
                self.insert_preference(PreferenceModel(user_id=user, VERDURE=True))
            if preference_sample == "GNOCCHI":
                self.insert_preference(PreferenceModel(user_id=user, GNOCCHI=True))
            if preference_sample == "INTERIORA":
                self.insert_preference(PreferenceModel(user_id=user, INTERIORA=True))
            if preference_sample == "FORMAGGI":
                self.insert_preference(PreferenceModel(user_id=user, FORMAGGI=True))
            if preference_sample == "RISO":
                self.insert_preference(PreferenceModel(user_id=user, RISO=True))

    def update_preference_count(self):
        group_list = []
        query = f"SELECT id FROM mygroups;"
        my_cursor = self.mysql_conn.cursor(buffered=True)
        my_cursor.execute(query)
        for group in my_cursor:
            group_list.append(int(group[0]))
        user_preference = {"PASTA":0, "CARNE":0, "PIZZA":0, "TORTELLINI":0, "SALUMI":0, "PESCE":0, "LEGUMI":0, "FUNGHI":0, "CROSTACEI_E_MOLLUSCHI":0, "VERDURE":0, "GNOCCHI":0, "INTERIORA":0, "FORMAGGI":0, "RISO":0}
        group_counter = 0
        for group_id in group_list:
            user_list = []
            my_cursor = self.mysql_conn.cursor(buffered=True)
            query = f"SELECT id FROM user WHERE group_id = {group_id};"
            my_cursor.execute(query)
            user_preference_flag = {"PASTA":False, "CARNE":False, "PIZZA":False, "TORTELLINI":False, "SALUMI":False, "PESCE":False, "LEGUMI":False, "FUNGHI":False, "CROSTACEI_E_MOLLUSCHI":False, "VERDURE":False, "GNOCCHI":False, "INTERIORA":False, "FORMAGGI":False, "RISO":False}
            for user in my_cursor:
                user_list.append(int(user[0]))
                my_cursor = self.mysql_conn.cursor(buffered=True)
                query = f"SELECT id, PASTA, CARNE, PIZZA, TORTELLINI, SALUMI, PESCE, " \
                        f"LEGUMI, FUNGHI, CROSTACEI_E_MOLLUSCHI, VERDURE, GNOCCHI, " \
                        f"INTERIORA, FORMAGGI, RISO FROM preference WHERE user_id = {int(user[0])};"
                my_cursor.execute(query)
                fetched = my_cursor.fetchone()
                if fetched != None:
                    if int(fetched[1]):
                        if user_preference_flag["PASTA"] == False:
                            user_preference["PASTA"] = user_preference["PASTA"] + 1
                            user_preference_flag["PASTA"] = True
                    if int(fetched[2]):
                        if user_preference_flag["CARNE"] == False:
                            user_preference["CARNE"] = user_preference["CARNE"] + 1
                            user_preference_flag["CARNE"] = True
                    if int(fetched[3]):
                        if user_preference_flag["PIZZA"] == False:
                            user_preference["PIZZA"] = user_preference["PIZZA"] + 1
                            user_preference_flag["PIZZA"] = True
                    if int(fetched[4]):
                        if user_preference_flag["TORTELLINI"] == False:
                            user_preference["TORTELLINI"] = user_preference["TORTELLINI"] + 1
                            user_preference_flag["TORTELLINI"] = True
                    if int(fetched[5]):
                        if user_preference_flag["SALUMI"] == False:
                            user_preference["SALUMI"] = user_preference["SALUMI"] + 1
                            user_preference_flag["SALUMI"] = True
                    if int(fetched[6]):
                        if user_preference_flag["PESCE"] == False:
                            user_preference["PESCE"] = user_preference["PESCE"] + 1
                            user_preference_flag["PESCE"] = True
                    if int(fetched[7]):
                        if user_preference_flag["LEGUMI"] == False:
                            user_preference["LEGUMI"] = user_preference["LEGUMI"] + 1
                            user_preference_flag["LEGUMI"] = True
                    if int(fetched[8]):
                        if user_preference_flag["FUNGHI"] == False:
                            user_preference["FUNGHI"] = user_preference["FUNGHI"] + 1
                            user_preference_flag["FUNGHI"] = True
                    if int(fetched[9]):
                        if user_preference_flag["CROSTACEI_E_MOLLUSCHI"] == False:
                            user_preference["CROSTACEI_E_MOLLUSCHI"] = user_preference["CROSTACEI_E_MOLLUSCHI"] + 1
                            user_preference_flag["CROSTACEI_E_MOLLUSCHI"] = True
                    if int(fetched[10]):
                        if user_preference_flag["VERDURE"] == False:
                            user_preference["VERDURE"] = user_preference["VERDURE"] + 1
                            user_preference_flag["VERDURE"] = True
                    if int(fetched[11]):
                        if user_preference_flag["GNOCCHI"] == False:
                            user_preference["GNOCCHI"] = user_preference["GNOCCHI"] + 1
                            user_preference_flag["GNOCCHI"] = True
                    if int(fetched[12]):
                        if user_preference_flag["INTERIORA"] == False:
                            user_preference["INTERIORA"] = user_preference["INTERIORA"] + 1
                            user_preference_flag["INTERIORA"] = True
                    if int(fetched[13]):
                        if user_preference_flag["FORMAGGI"] == False:
                            user_preference["FORMAGGI"] = user_preference["FORMAGGI"] + 1
                            user_preference_flag["FORMAGGI"] = True
                    if int(fetched[14]):
                        if user_preference_flag["RISO"] == False:
                            user_preference["RISO"] = user_preference["RISO"] + 1
                            user_preference_flag["RISO"] = True
            if any(user_preference_flag.values()):
                group_counter += 1
        for key, element in user_preference.items():
            user_preference[key] = element / group_counter
        my_cursor = self.mysql_conn.cursor(buffered=True)
        my_cursor.execute(query)
        query = "DELETE FROM popularity_counter"
        my_cursor.execute(query)
        my_cursor = self.mysql_conn.cursor(buffered=True)
        my_cursor.execute(query)
        query = "INSERT INTO popularity_counter (PASTA, CARNE, PIZZA, TORTELLINI, SALUMI, PESCE," \
                "LEGUMI, FUNGHI, CROSTACEI_E_MOLLUSCHI, VERDURE, GNOCCHI, INTERIORA, FORMAGGI, RISO) " \
                "VALUES (%(PASTA)s, %(CARNE)s, %(PIZZA)s, %(TORTELLINI)s, %(SALUMI)s, %(PESCE)s, %(LEGUMI)s, %(FUNGHI)s, %(CROSTACEI_E_MOLLUSCHI)s, %(VERDURE)s, %(GNOCCHI)s, %(INTERIORA)s, %(FORMAGGI)s, %(RISO)s)"
        my_cursor.execute(query, user_preference) 
        self.mysql_conn.commit()
        
