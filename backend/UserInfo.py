from UserInfoModel import UserInfoModelClass
from UserInfoModel import UserSupportModelClass

class UserInfoClass(object):
    def __init__(self, connection_mysql):
        self.my_cursor = connection_mysql

    
    def get_info(self, user_info: UserInfoModelClass):
        pass

    def get_validity(self, user_info: UserInfoModelClass):
        my_cursor = self.my_cursor.cursor()
        user_info_dict = user_info
        query = f"SELECT COUNT(*) FROM user_info WHERE user_id = '{user_info_dict['user_id']}';"
        my_cursor.execute(query)
        fetched = my_cursor.fetchone()
        if fetched[0] == 0:
            return False
        else:
            return True



    def set_info(self, user_info: UserInfoModelClass):
        my_cursor = self.my_cursor.cursor()
        user_info_dict = user_info
        query = "INSERT INTO user_info (user_id,gender,nationality,age,TORTELLINI,PESCE,CARNE,GNOCCHI,PIZZA,RISO,FORMAGGI,LEGUMI,VERDURE,INTERIORA,FUNGHI,CROSTACEI_E_MOLLUSCHI,PASTA,SALUMI,french,chinese,jpan,italian,greek,indian,spain,lebanan,moroccan,turkish,thai) VALUES (%(user_id)s, %(gender)s, %(nationality)s, %(age)s, %(TORTELLINI)s, %(PESCE)s, %(CARNE)s, %(GNOCCHI)s, %(PIZZA)s, %(RISO)s, %(FORMAGGI)s, %(LEGUMI)s, %(VERDURE)s, %(INTERIORA)s, %(FUNGHI)s, %(CROSTACEI_E_MOLLUSCHI)s, %(PASTA)s, %(SALUMI)s, %(french)s, %(chinese)s, %(jpan)s, %(italian)s, %(greek)s, %(indian)s, %(spain)s, %(lebanan)s, %(moroccan)s, %(turkish)s, %(thai)s)"
        my_cursor.execute(query, user_info_dict)
        self.my_cursor.commit()
        return  True

    def set_supports(self, user_info: UserSupportModelClass):
        my_cursor = self.my_cursor.cursor()
        user_info_dict = user_info
        query = "INSERT INTO user_supports (user_id,info_level,expansion,contradiction) VALUES (%(user_id)s, %(info_level)s, %(expansion)s, %(contradiction)s)"
        my_cursor.execute(query, user_info_dict)
        self.my_cursor.commit()
        return  True
  





	
	





