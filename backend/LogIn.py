from LoginModel import Login

class LogInClass(object):
    def __init__(self, connection_mysql):
        self.my_cursor = connection_mysql
    
    def user_login(self, user_info: Login): 
        my_cursor = self.my_cursor.cursor(buffered=True)
        my_cursor_email = self.my_cursor.cursor(buffered=True)
        user_info_dict = user_info
        query = f"SELECT user_id, name FROM singin WHERE email = '{user_info_dict['email']}' AND password = '{user_info_dict['password']}';"
        my_cursor.execute(query)
        fetched = my_cursor.fetchall()
        if len(fetched) == 0:
            query = f"SELECT COUNT(*) FROM singin WHERE email = '{user_info_dict['email']}';"
            my_cursor_email.execute(query)
            fetched_inner = my_cursor_email.fetchone()
            if fetched_inner[0] == 0:
                return "This email has not been registrated yet."
            else:
                return "Password is not correct."
        else:
            login_dict = {fetched[0][0]:fetched[0][1]}
            return login_dict