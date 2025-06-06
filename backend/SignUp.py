from SignupModel import SingUp
from GroupConstruction import GroupConstructionClass
import pandas as pd
from Progress import ProgressClass

class SingUpClass(object):
    def __init__(self, connection_mysql):
        self.my_cursor = connection_mysql
    
    def register_new_user(self, user_info: SingUp):
        my_cursor = self.my_cursor.cursor()
        user_info_dict = user_info
        query = f"SELECT COUNT(*) FROM singin WHERE email = '{user_info_dict['email']}';"
        my_cursor.execute(query)
        fetched = my_cursor.fetchone()
        if fetched[0] == 0:
            query = f"INSERT INTO singin (user_id, name, email,	password) VALUES ('{user_info_dict['id']}', '{user_info_dict['name']}', '{user_info_dict['email']}', '{user_info_dict['password']}')"
            my_cursor.execute(query)
            self.my_cursor.commit()
            my_cursor_membership = self.my_cursor.cursor()
            query = f"INSERT INTO user_membership_info (user_id, membership) VALUES ('{user_info_dict['id']}', false)"
            my_cursor_membership.execute(query)
            self.my_cursor.commit()
            GroupConstructionClass(self.my_cursor).group_construction(user_info_dict['id'])
            return  "Registration has been completed"
        else:
            return "You have previously submitted to the system with this email"

    def register_from_google_sheet(self):
        SHEET_ID = '1CYxWgVn2gApcP8x6EysAJSp3UhV6cS-gXzBvkXEeSIQ'
        SHEET_NAME = 'Ids'
        url = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}'
        df = pd.read_csv(url)
        df = df.sample(frac=1).reset_index(drop=True)
        user_id = 16000
        print(df)
        for row in df:
            print(row)
            user_id += 1
            name = str(row[1]) + 'A'
            password = str(row[1]) + 'A'
            user_info = {'id': user_id, 'name': row[0], 'email': name, 'password': password}
            self.register_new_user(user_info)
            ProgressClass(self.my_cursor).pregress_set_row(user_id)



