from ProgressModel import ProgressModelClass

class ProgressClass(object):
    def __init__(self, connection_mysql):
        self.mysql_conn = connection_mysql

    def pregress_update(self, progress: ProgressModelClass):
        my_cursor = self.mysql_conn.cursor()
        progress = progress
        column_name = progress['column_name']
        column_value = progress[progress['column_name']]
        user_id = progress['user_id']
        query = f"UPDATE progress SET  {column_name} = {column_value} WHERE user_id = {user_id};"
        my_cursor.execute(query)
        self.mysql_conn.commit()
        return  True

    def pregress_set_row(self, user_id: int):
        my_cursor = self.mysql_conn.cursor()
        query = f"INSERT INTO progress (user_id,personal_info,pre_rating,post_rating,group_construction,decision_making,questionnaire) VALUES ({user_id}, false, false, false, false, false, false)"
        my_cursor.execute(query)
        self.mysql_conn.commit()
        return  True

    def get_progress(self, user_id: int):
        my_cursor = self.mysql_conn.cursor()
        query = f"SELECT * FROM progress WHERE user_id = {user_id}"
        my_cursor.execute(query)
        fetched = my_cursor.fetchall()
        pregress_result = {'personal_info':int(fetched[0][2]),
        'pre_rating':int(fetched[0][3]),
        'post_rating':int(fetched[0][4]),
        'group_construction':int(fetched[0][5]),
        'decision_making':int(fetched[0][6]),
        'questionnaire':int(fetched[0][7]),
        }
        self.mysql_conn.commit()
        return  pregress_result

