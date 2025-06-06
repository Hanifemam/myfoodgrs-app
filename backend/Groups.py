import json

from GroupModel import GroupModel
from GroupModel import GroupResults
from GroupModel import Selected
from GroupModel import SUS
from GroupModel import SelectedOrganizer


class Groups(object):

    def __init__(self, connection):
        self.mysql_conn = connection

    def create_group_table(self):
        my_cursor = self.mysql_conn.cursor()
        my_cursor.execute('DROP TABLE IF EXISTS gro;')
        query = 'CREATE TABLE mygroups ' \
                '(id int PRIMARY KEY UNIQUE auto_increment, ' \
                'distance int, ' \
                'price_eco BINARY,' \
                'price_mid BINARY,' \
                'price_expensive BINARY, ' \
                'service_home_delivery BINARY)'
        my_cursor.execute(query)
        self.mysql_conn.commit()

    def insert_group(self):
        new_group = {'distance': 1000000000,
                    'price_eco': True,
                    'price_mid': True,
                    'price_expensive': True,
                    'service_home_delivery': False}
        my_cursor = self.mysql_conn.cursor(buffered=True)
        query = "INSERT INTO mygroups (distance, price_eco, price_mid, price_expensive, service_home_delivery) " \
                "VALUES (%(distance)s, %(price_eco)s, %(price_mid)s, %(price_expensive)s, %(service_home_delivery)s)"
        my_cursor.execute(query, new_group)
        query="SELECT last_insert_id();"
        my_cursor.execute(query)
        last_id = my_cursor.fetchone()
        self.mysql_conn.commit()
        return json.dumps({'group_id':int(last_id[0])})

    def update_preference(self, group: GroupModel, group_id:int, restaurant_id: int):
        query_long = f"SELECT longitude FROM restaurants WHERE id = {restaurant_id}"
        query_alt = f"SELECT latitude FROM restaurants WHERE id = {restaurant_id}"
        my_cursor_long = self.mysql_conn.cursor(buffered=True)
        my_cursor_alt = self.mysql_conn.cursor(buffered=True)
        my_cursor_long.execute(query_long)
        my_cursor_alt.execute(query_alt)
        restaurant_long = int(my_cursor_long.fetchone()[0])
        restaurant_alt = int(my_cursor_alt.fetchone()[0])
        my_cursor = self.mysql_conn.cursor()
        my_cursor_select = self.mysql_conn.cursor()
        new_group = group.dict()
        query = f"SELECT distance, price_eco, price_mid, price_expensive, service_home_delivery " \
                f"FROM mygroups WHERE id = {group_id};"
        my_cursor_select.execute(query)
        fetched = my_cursor_select.fetchone()
        if new_group['distance'] != fetched[0]:
            query = f"UPDATE mygroups SET distance = {new_group['distance']} " \
                    f"WHERE id = {group_id};"
            my_cursor.execute(query)
        if new_group['price_eco'] != fetched[1]:
            query = f"UPDATE mygroups SET price_eco = {new_group['price_eco']} " \
                    f"WHERE id = {group_id};"
            my_cursor.execute(query)
        if new_group['price_mid'] != fetched[2]:
            query = f"UPDATE mygroups SET price_mid = {new_group['price_mid']} " \
                    f"WHERE id = {group_id};"
            my_cursor.execute(query)
        if new_group['price_expensive'] != fetched[3]:
            query = f"UPDATE mygroups SET price_expensive = {new_group['price_expensive']} " \
                    f"WHERE id = {group_id};"
            my_cursor.execute(query)
        if new_group['service_home_delivery'] != fetched[4]:
            query = f"UPDATE mygroups SET service_home_delivery = {new_group['service_home_delivery']} " \
                    f"WHERE id = {group_id};"
            my_cursor.execute(query)
        self.mysql_conn.commit()

    def get_group(self, group_id: int):
        fetch_list = []
        column_list = ["id", "distance", "price_eco", "price_mid", "price_expensive", "service_home_delivery"]
        my_cursor_select = self.mysql_conn.cursor()
        query = f"SELECT * FROM mygroups WHERE id = {group_id};"
        my_cursor_select.execute(query)
        fetched = my_cursor_select.fetchone()
        for item in fetched:
            if item == None:
                fetch_list.append(0)
            else:
                fetch_list.append(int(item))
        group_dictionary = dict(zip(column_list, fetch_list))
        return group_dictionary

    def insert_group_result(self, reuslt: GroupResults):
        query = "INSERT INTO results (groupId, description) VALUES (%(groupId)s,%(description)s)"
        # query = f"INSERT INTO results (groupId, description) VALUES ({reuslt['groupId']},{reuslt['description']})"
        my_cursor = self.mysql_conn.cursor()
        # my_cursor_select.execute(query)
        my_cursor.execute(query, reuslt)
        self.mysql_conn.commit()
        return True

    def insert_to_selected(self, selected: Selected):
        query = "INSERT INTO selected (group_id, restaurant_id) VALUES (%(group_id)s,%(restaurant_id)s)"
        my_cursor = self.mysql_conn.cursor()
        my_cursor.execute(query, selected)
        self.mysql_conn.commit()
        return True

    def insert_to_selected_organizer(self, selected: SelectedOrganizer):
        query = "INSERT INTO user_group_info (user_id,organizer,member,choice) VALUES (%(user_id)s,%(organizer)s,%(member)s,%(restaurant_id)s)"
        my_cursor = self.mysql_conn.cursor()
        my_cursor.execute(query, selected)
        self.mysql_conn.commit()
        return True
    
    def insert_to_SUS(self, sus: SUS):
        query = "INSERT INTO sus (group_id, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, f1, f2, f3, f4, f5, f6, f7, f8, f9, f10, f11, f12, f13, f14, f15, c1, name, email) VALUES (%(group_id)s,%(q1)s,%(q2)s,%(q3)s,%(q4)s,%(q5)s,%(q6)s,%(q7)s,%(q8)s,%(q9)s,%(q10)s,%(f1)s,%(f2)s,%(f3)s,%(f4)s,%(f5)s,%(f6)s,%(f7)s,%(f8)s,%(f9)s,%(f10)s,%(f11)s,%(f12)s,%(f13)s,%(f14)s,%(f15)s,%(c1)s, %(name)s, %(email)s)"
        
        my_cursor = self.mysql_conn.cursor()
        my_cursor.execute(query, sus)
        self.mysql_conn.commit()
        return True

    def get_distance(self, group_id: int):
        my_cursor_select = self.mysql_conn.cursor()
        query = f"SELECT distance FROM mygroups WHERE id = {group_id};"
        my_cursor_select.execute(query)
        fetched = my_cursor_select.fetchone()
        return fetched[0]
