import numpy as np
class PrePostRatingClass(object):

    def __init__(self, connection):
        self.mysql_conn = connection
    
    def get_group_member(self,user_id):
        my_cursor = self.mysql_conn.cursor(buffered=True)
        query = f"SELECT member_id FROM user_group_membership WHERE user_id = {int(user_id)};"
        my_cursor.execute(query)
        first_user =  my_cursor.fetchone()
        if first_user == None:
            return "Wait for your group."
        members = [first_user[0]]
        for user in my_cursor:
            members.append(user[0])
        return members
    
    def get_individual_rating(self, user_id):
        group_members = self.get_group_member(user_id)
        individual_restaurants = []
        my_cursor = self.mysql_conn.cursor(buffered=True)
        query = f"SELECT restaurant_id FROM user_restaurant_rating_pre WHERE user_id = {int(user_id)};"
        my_cursor.execute(query)
        for restaurant in my_cursor:
            individual_restaurants.append(restaurant[0])
        group_restaurants = self.get_group_rating(user_id)
        individual_restaurants_set = set(individual_restaurants)
        group_restaurants_set = set (group_restaurants)
        individual_difference = individual_restaurants_set.difference(group_restaurants_set)
        group_difference = group_restaurants_set.difference(individual_restaurants_set)
        final_list = list(individual_difference.union(group_difference))
        return final_list

    def get_waiting_check(self, user_id):
        flag = True
        group_members = self.get_group_member(user_id)
        restaurants = []
        for member_id in group_members:
            my_cursor = self.mysql_conn.cursor(buffered=True)
            query = f"SELECT choice FROM user_group_info WHERE user_id = {int(member_id)};"
            my_cursor.execute(query)
            restaurant =  my_cursor.fetchone()
            if ( restaurant is None):
                flag = False
        return flag
    
    def get_group_rating(self, user_id):
        group_members = self.get_group_member(user_id)
        group_members.append(user_id)
        restaurants = []
        for member_id in group_members:
            my_cursor = self.mysql_conn.cursor(buffered=True)
            query = f"SELECT choice FROM user_group_info WHERE user_id = {int(member_id)};"
            my_cursor.execute(query)
            restaurant =  my_cursor.fetchone()
            if (not restaurant is None):
                restaurants.append(restaurant[0])
        if len(restaurants) > 0:
            restaurants_set = set(restaurants)
            restaurants = list(restaurants_set)
        else: 
            restaurants = []
        return restaurants
        
