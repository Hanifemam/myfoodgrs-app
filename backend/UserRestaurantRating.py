from UserRestaurantRatingModel import UserRatingoModelClass

class UserRestaurantRatingClass(object):
    def __init__(self, connection_mysql):
        self.mysql_conn = connection_mysql

    def insert_pre_rating(self, user_rating: UserRatingoModelClass):
        my_cursor = self.mysql_conn.cursor()
        user_rating_dict = user_rating
        query = "INSERT INTO user_restaurant_rating_pre (user_id,restaurant_id,rating) VALUES (%(user_id)s, %(restaurant_id)s, %(rating)s)"
        my_cursor.execute(query, user_rating_dict)
        self.mysql_conn.commit()
        return  True
    
    def insert_post_rating(self, user_rating: UserRatingoModelClass):
        my_cursor = self.mysql_conn.cursor()
        user_rating_dict = user_rating
        query = "INSERT INTO user_restaurant_rating_post (user_id,restaurant_id,rating,group_check) VALUES (%(user_id)s, %(restaurant_id)s, %(rating)s, %(group)s)"
        my_cursor.execute(query, user_rating_dict)
        self.mysql_conn.commit()
        return  True
