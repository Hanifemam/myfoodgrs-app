import json

from geopy.geocoders import Nominatim

import UserModel
from UserModel import Organizer, Companion


class Users(object):

    def __init__(self, connection_mysql):
        self.mysql_conn = connection_mysql

    def create_user_table(self):
        """This function create a table for users
            and save it in data base
            """
        my_cursor = self.mysql_conn.cursor()
        my_cursor.execute('DROP TABLE IF EXISTS user;')
        query = 'CREATE TABLE user ' \
                '(id int PRIMARY KEY UNIQUE auto_increment, ' \
                'first_name VARCHAR(500), ' \
                'last_name VARCHAR(500),' \
                'email  VARCHAR(500),' \
                'latitude DECIMAL(8,6), ' \
                'longitude DECIMAL(8,6),' \
                'role_organizer Enum("organizer", "companion"),' \
                'group_id int' \
                ')'
        # 'FOREIGN KEY (group_id) REFERENCES mygroups(id)' \
        my_cursor.execute(query)
        self.mysql_conn.commit()

    def insert_organizer(self, organizer: Organizer):
        # input()
        my_cursor = self.mysql_conn.cursor()
        new_user = organizer
        query = "INSERT INTO user (first_name, last_name, email, latitude, longitude, role, group_id) " \
                "VALUES (%(first_name)s, %(last_name)s, %(email)s, %(latitude)s, %(longitude)s, " \
                "%(role)s, %(group_id)s)"
        my_cursor.execute(query, new_user)
        query = "SELECT last_insert_id();"
        my_cursor.execute(query)
        last_id = my_cursor.fetchone()
        self.mysql_conn.commit()
        return json.dumps({'user_id':int(last_id[0])})

    def update_organizer(self, organizer: Organizer, user_id):
        my_cursor = self.mysql_conn.cursor(buffered=True)
        new_user = organizer.dict()
        query = f"UPDATE user SET first_name = '{new_user['first_name']}' " \
                f"WHERE id = {user_id};"
        my_cursor.execute(query)
        self.mysql_conn.commit()
        return user_id
    
    def update_organizer_group_id(self, organizer: Organizer, user_id):
        my_cursor = self.mysql_conn.cursor(buffered=True)
        new_user = organizer.dict()
        query = f"UPDATE user SET first_name = '{new_user['first_name']}', group_id = '{new_user['group_id']}' WHERE id = {user_id};"
        my_cursor.execute(query)
        self.mysql_conn.commit()
        return user_id

    def insert_companion(self, companion: Companion):
        my_cursor = self.mysql_conn.cursor()
        new_user = companion.dict()
        query = "INSERT INTO user (first_name, last_name, email, latitude, longitude, role, group_id) " \
                "VALUES (%(first_name)s, %(last_name)s, %(email)s, %(latitude)s, %(longitude)s, " \
                "%(role)s, %(group_id)s)"
        my_cursor.execute(query, new_user)
        query = "SELECT last_insert_id();"
        my_cursor.execute(query)
        last_id = my_cursor.fetchone()
        self.mysql_conn.commit()
        return json.dumps({'user_id': int(last_id[0])})

    def update_companion(self, companion: Companion):
        my_cursor = self.mysql_conn.cursor()
        new_user = companion.dict()
        query = "INSERT INTO user (first_name, last_name, email, latitude, longitude, role, group_id) " \
                "VALUES (%(first_name)s, %(last_name)s, %(email)s, %(latitude)s, %(longitude)s, " \
                "%(role)s, %(group_id)s)"
        my_cursor.execute(query, new_user)
        self.mysql_conn.commit()

    def update_location(self, user: Companion, user_id: str):
        my_cursor = self.mysql_conn.cursor(buffered=True)
        new_user = user.dict()
        query = f"UPDATE user SET latitude = '{new_user['latitude']}', " \
                f"longitude = '{new_user['longitude']}' " \
                f"WHERE id = {user_id};"
        my_cursor.execute(query)
        self.mysql_conn.commit()
        return user_id

    def update_location_by_address(self, address: UserModel.Address, user_id: int):
        my_cursor = self.mysql_conn.cursor(buffered=True)
        user_dict = dict()
        coordination_dict = dict()
        geolocator = Nominatim(user_agent="AIzaSyBVKguW-Fc_dQM2CmrmKFQw4FtTTlw6mdw")
        geo_row = geolocator.geocode(address['address']).raw
        coordination_dict['lat'] = geo_row['lat']
        coordination_dict['lon'] = geo_row['lon']
        query = f"UPDATE user SET latitude = '{coordination_dict['lat']}', " \
                f"longitude = '{coordination_dict['lon']}' " \
                f"WHERE id = {user_id};"
        my_cursor.execute(query)
        self.mysql_conn.commit()
        user_dict[user_id] = coordination_dict
        return json.dumps(user_dict)

    def remove_member_companion(self, user_id: int):
        my_cursor = self.mysql_conn.cursor()
        user_to_delete = int(user_id)
        my_cursor.execute(f"SELECT role FROM user WHERE id={user_to_delete};")
        fetched_row = my_cursor.fetchone()[0]
        if fetched_row == "companion":
            query = f"DELETE FROM user WHERE id={user_to_delete};"
            my_cursor.execute(query)
            self.mysql_conn.commit()
            return "Done"
        else:
            return "Unable to delete"
    
    def remove_member_organizer(self, user_id: int):
        my_cursor = self.mysql_conn.cursor()
        user_to_delete = int(user_id)
        query = f"DELETE FROM user WHERE id={user_to_delete};"
        my_cursor.execute(query)
        self.mysql_conn.commit()
            
    def get_users(self, group_id):
        members_dict = []
        query = f"SELECT first_name, last_name, role FROM user WHERE group_id = {group_id}"
        my_cursor = self.mysql_conn.cursor()
        my_cursor.execute(query)
        for user in my_cursor:
            user_dict = dict()
            user_dict["first_name"] = user[0]
            user_dict["last_name"] = user[1]
            user_dict["role"] = user[2]
            members_dict.append(user_dict)
        return members_dict

    def get_users_location(self, group_id):
        members_dict = [] #uncomment for the last version
        # members_dict = dict()
        query = f"SELECT latitude, longitude FROM user WHERE group_id = {group_id}"
        my_cursor = self.mysql_conn.cursor()
        my_cursor.execute(query)
        for user in my_cursor:
            user_dict = dict()
            user_dict["latitude"] = user[0]
            user_dict["longitude"] = user[1]
            members_dict.append(user_dict) #uncomment for the new version
            # members_dict[user] = user_dict
        return members_dict

    def get_users_location_front(self, group_id):
        # members_dict = {} #uncomment for the last version
        members_dict = dict()
        query = f"SELECT latitude, longitude, id FROM user WHERE group_id = {group_id}"
        my_cursor = self.mysql_conn.cursor()
        my_cursor.execute(query)
        for user in my_cursor:
            user_dict = dict()
            user_dict["latitude"] = float(user[0])
            user_dict["longitude"] = float(user[1])
            # members_dict.append(user_dict) #uncomment for the new version
            members_dict[user[2]] = user_dict
        return json.dumps(members_dict)

