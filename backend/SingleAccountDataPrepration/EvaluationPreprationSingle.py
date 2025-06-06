import csv
from typing import get_type_hints
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
from datetime import datetime
from Supplementary import Supplementary
from supplementary.Restaurant import Restaurant

class DataPreprationSingle(object):
    
    def __init__(self,connection_mysql):
        self.mysql_conn = connection_mysql
        
    def fetch_groups(self):
        query = "SELECT DISTINCT(user_id) FROM  user_group_membership"
        my_cursor = self.mysql_conn.cursor(buffered=True)
        my_cursor.execute(query)
        groups_list = list()
        groups_set = set()
        for organizer in my_cursor:
            group_set = set()
            group_set.add(organizer[0])
            query = f"SELECT member_id FROM  user_group_membership WHERE user_id = {organizer[0]}"
            if 14912 >= organizer[0] >= 14639 or 20798 >= organizer[0] >= 20734:
                my_cursor = self.mysql_conn.cursor(buffered=True)
                my_cursor.execute(query)
                for members in my_cursor:
                    group_set.add(members[0])
                groups_list.append(group_set)
                groups_set.add(frozenset(group_set))
        print(groups_set)
        print(len(groups_set))
        # with open("OutPuts/groups_single.csv", 'w') as file:
        with open("OutPuts/Revised/groups_single_Revised.csv", 'w') as file:
            writer = csv.writer(file)
            writer.writerow(['group', 'member'])
            group_counter = 0
            for group in groups_list:
                group_counter += 1
                for member in group:
                    writer.writerow([group_counter, member])
            file.close()
            
    def fetch_groups_members(self):
        query = "SELECT DISTINCT(user_id) FROM  user_group_membership"
        my_cursor = self.mysql_conn.cursor(buffered=True)
        my_cursor.execute(query)
        groups_list = list()
        for organizer in my_cursor:
            group_set = set()
            group_set.add(organizer[0])
            query = f"SELECT member_id FROM  user_group_membership WHERE user_id = {organizer[0]}"
            if 14912 >= organizer[0] >= 14639 or 20798 >= organizer[0] >= 20734:
                my_cursor = self.mysql_conn.cursor(buffered=True)
                my_cursor.execute(query)
                for members in my_cursor:
                    group_set.add(members[0])
                groups_list.append(group_set)
        # with open("OutPuts/groups_members_single.csv", 'w') as file:
        with open("OutPuts/Revised/groups_members_single.csv", 'w') as file:
            writer = csv.writer(file)
            writer.writerow(['group', 'member1','member2','member3','member4','member5',])
            group_counter = 0
            for group in groups_list:
                group_counter += 1
                group_list = list(group)
                group_list.insert(0,group_counter)
                writer.writerow(group_list)
            file.close()
    
    def get_individual_ratings(self):
        # with open("OutPuts/individual_ratings_single.csv", 'w') as file:
        with open("OutPuts/Revised/individual_ratings_single.csv", 'w') as file:        
            writer = csv.writer(file)
            writer.writerow(['user', 'restaurant','rating'])
            query = "SELECT DISTINCT(user_id) FROM  user_restaurant_rating_post"
            my_cursor = self.mysql_conn.cursor(buffered=True)
            my_cursor.execute(query)
            for user in my_cursor:
                choice_list = self.extract_group_choice(self.user_group_members(user[0]))
                if 14912 >= user[0] >= 14639  or 20798 >= user[0] >= 20734:
                    query = f"SELECT restaurant_id, rating FROM  user_restaurant_rating_pre WHERE user_id = {user[0]}"
                    my_cursor = self.mysql_conn.cursor(buffered=True)
                    my_cursor.execute(query)
                    for ratings in my_cursor:
                        if ratings[0] in choice_list:
                            writer.writerow([user[0], ratings[0],ratings[1]])
                    query = f"SELECT restaurant_id, rating FROM  user_restaurant_rating_post WHERE user_id = {user[0]} AND group_check != 1 "
                    my_cursor = self.mysql_conn.cursor(buffered=True)
                    my_cursor.execute(query)
                    for ratings in my_cursor:
                        if ratings[0] in choice_list:
                            writer.writerow([user[0], ratings[0],ratings[1]])
            file.close()
            
    def user_group_members(self, user_id):
        df_groups = pd.read_csv("./OutPuts/groups_members.csv")
        group_list = []
        for index,group in df_groups.iterrows():
            if ((group['member1'] == user_id) 
                or (group['member2'] == user_id) 
                or (group['member3'] == user_id) 
                or (group['member4'] == user_id) 
                or (group['member5'] == user_id)):
                if not math.isnan(group['member1']):
                    group_list.append(int(group['member1']))
                if not math.isnan(group['member2']):
                    group_list.append(int(group['member2']))
                if not math.isnan(group['member3']):
                    group_list.append(int(group['member3']))
                if not math.isnan(group['member4']):
                    group_list.append(int(group['member4']))
                if not math.isnan(group['member5']):
                    group_list.append(int(group['member5']))
                return group_list
            
    def extract_group_choice(self, group_list):
        # df_choices = pd.read_csv("./OutPuts/Selected_first.csv")
        df_choices = pd.read_csv("./OutPuts/Selected_first_Revised.csv")
        choice_list = []
        if group_list is not None:
            for member in group_list:
                if len(df_choices.loc[df_choices['user_id'] == member]['choice']) > 0:
                    choice_list.append(df_choices.loc[df_choices['user_id'] == member]['choice'].values[0])
        # print(choice_list)
        return choice_list
    
    def get_group_choices(self):
        with open("OutPuts/organizer_choice.csv", 'w') as file:
            writer = csv.writer(file)
            writer.writerow(['user', 'restaurant','rating'])
            query = "SELECT DISTINCT(user_id) FROM  user_group_membership"
            my_cursor = self.mysql_conn.cursor(buffered=True)
            my_cursor.execute(query)
            groups_list = list()
            groups_set = set()
            for organizer in my_cursor:
                group_set = set()
                group_set.add(organizer[0])
                query = f"SELECT user_id, choice FROM  user_group_info WHERE user_id = {organizer[0]}"
                if 14912 >= organizer[0] >= 14639 or 20798 >= organizer[0] >= 20734:
                    my_cursor = self.mysql_conn.cursor(buffered=True)
                    my_cursor.execute(query)
                    for members in my_cursor:
                        writer.writerow([members[0], members[1]])
    
    def get_group_ratings(self):
        # with open("OutPuts/group_ratings_single.csv", 'w') as file:
        with open("OutPuts/Revised/group_ratings_single.csv", 'w') as file:
            writer = csv.writer(file)
            writer.writerow(['user', 'restaurant','rating'])
            query = "SELECT DISTINCT(user_id) FROM  user_restaurant_rating_post"
            my_cursor = self.mysql_conn.cursor(buffered=True)
            my_cursor.execute(query)
            non_participants = [14733, 14736, 14737, 14739, 14740, 14752, 14755, 14759, 14765, 14766, 14768, 14776, 14787, 14790, 14794, 14796, 14907, 14908, 14924, 14930, 14933, 14912, 14649, 14764]
            for user in my_cursor:
                choice_list = self.extract_group_choice(self.user_group_members(user[0]))
                if int(user[0]) not in non_participants and int(user[0]) >= 14639:
                    query = f"SELECT restaurant_id, rating FROM  user_restaurant_rating_post WHERE user_id = {user[0]} AND group_check = 1 "
                    my_cursor = self.mysql_conn.cursor(buffered=True)
                    my_cursor.execute(query)
                    for ratings in my_cursor:
                        if ratings[0] in choice_list:
                            writer.writerow([user[0], ratings[0],ratings[1]])
            file.close()
    
    def get_user_support(self):
        with open("OutPuts/support_type_single.csv", 'w') as file:
            writer = csv.writer(file)
            writer.writerow(['user', 'info', 'expansion', 'contradiction'])
            query = "SELECT DISTINCT(user_id) FROM  user_group_membership"
            my_cursor = self.mysql_conn.cursor(buffered=True)
            my_cursor.execute(query)
            first_account_id_set = self.get_first_account_id()
            for user in my_cursor:
                if user[0] in first_account_id_set and (14912 >= user[0] >= 14639   or 20798 >= user[0] >= 20734):
                    query = f"SELECT info_level,expansion,contradiction FROM  user_supports WHERE user_id = {user[0]}"
                    my_cursor = self.mysql_conn.cursor(buffered=True)
                    my_cursor.execute(query)
                    for supports in my_cursor:
                        support_list = list(supports)
                        support_list.insert(0,user[0])
                        writer.writerow(support_list)
            file.close()
    
    def get_first_account_id(self):
        # df_choices = pd.read_csv("./OutPuts/Selected_first.csv")
        df_choices = pd.read_csv("./OutPuts/Selected_first_Revised.csv")
        choice_list = set(list(df_choices["user_id"].values[:]))
        return choice_list
    
    def get_all_users_for_first_accounts(self):
        all_users_for_first_accounts = set()
        organizers_set = self.get_first_account_id()
        for organizer in organizers_set:
            group_members = []
            user_group_member = self.user_group_members(organizer)
            if user_group_member is not None:
                group_members.extend(user_group_member)
                group_members.append(organizer)
                for member in group_members:
                    all_users_for_first_accounts.add(member)
        return all_users_for_first_accounts
    
    def group_organizer_type(self):
        with open("OutPuts/group_organizer_type_single.csv", 'w') as file:
            writer = csv.writer(file)
            writer.writerow(['organizer', 'type'])
            query = "SELECT DISTINCT(user_id) FROM user_group_membership"
            my_cursor_read = self.mysql_conn.cursor(buffered=True)
            my_cursor_read.execute(query)
            first_account_id_set = self.get_first_account_id()
            for organizer in my_cursor_read:
                if organizer[0] in first_account_id_set and (14912 >= organizer[0] >= 14639 or 20798 >= organizer[0] >= 20734):
                    query = f"SELECT info_level,expansion,contradiction FROM  user_supports WHERE user_id = {organizer[0]}"
                    my_cursor = self.mysql_conn.cursor(buffered=True)
                    my_cursor.execute(query)
                    for supports in my_cursor:
                        if (supports[0] == 1 and supports[1] == 0 and supports[2] == 0):
                            writer.writerow([organizer[0], 'G1'])
                        if (supports[0] == 1 and supports[1] == 1 and supports[2] == 0):
                            writer.writerow([organizer[0], 'G2'])
                        if (supports[0] == 1 and supports[1] == 0 and supports[2] == 1):
                            writer.writerow([organizer[0], 'G3'])
                        if (supports[0] == 1 and supports[1] == 1 and supports[2] == 1):
                            writer.writerow([organizer[0], 'G4'])
                        if (supports[0] == 2 and supports[1] == 0 and supports[2] == 0):
                            writer.writerow([organizer[0], 'G5'])
                        if (supports[0] == 2 and supports[1] == 1 and supports[2] == 0):
                            writer.writerow([organizer[0], 'G6'])
                        if (supports[0] == 2 and supports[1] == 0 and supports[2] == 1):
                            writer.writerow([organizer[0], 'G7'])
                        if (supports[0] == 2 and supports[1] == 1 and supports[2] == 1):
                            writer.writerow([organizer[0], 'G8'])
                        if (supports[0] == 3 and supports[1] == 0 and supports[2] == 0):
                            writer.writerow([organizer[0], 'G9'])
                        if (supports[0] == 3 and supports[1] == 1 and supports[2] == 0):
                            writer.writerow([organizer[0], 'G10'])
                        if (supports[0] == 3 and supports[1] == 0 and supports[2] == 1):
                            writer.writerow([organizer[0], 'G11'])
                        if (supports[0] == 3 and supports[1] == 1 and supports[2] == 1):
                            writer.writerow([organizer[0], 'G12'])
            file.close()
            df_groups_type = pd.read_csv("OutPuts/group_organizer_type.csv")
            df_groups_type = df_groups_type.drop_duplicates().reindex()
            df_groups_type.to_csv("OutPuts/group_organizer_type.csv")
        
    def get_organizer_choice(self, organizer):
        query = f"SELECT choice FROM user_group_info WHERE user_id = {organizer}"
        my_cursor = self.mysql_conn.cursor(buffered=True)
        my_cursor.execute(query)
        choices_list = []
        for choice in my_cursor:
            choices_list.append(choice[0])
        return choices_list
    
    def get_organizer_visited_rest(self):
        with open("OutPuts/organizer_visiting_single.csv", 'w') as file:
            writer = csv.writer(file)
            writer.writerow(['user_id','group_id','rest_id','avialble_rest','sort_pop','sort_fit','sort_sim','fit_score','sim_score','c1_fit','c2_fit','c3_fit','c4_fit','c5_fit','fit_rank','sim_rank','pop_rank','tip','category','dish','price','time'])
            query = "SELECT DISTINCT(user_id) FROM  user_group_info"
            my_cursor = self.mysql_conn.cursor(buffered=True)
            my_cursor.execute(query)
            first_account_id_set = self.get_first_account_id()
            for user in my_cursor:
                if user[0] in first_account_id_set and (14912 >= user[0] >= 14639  or 20798 >= user[0] >= 20734):
                    query = f"SELECT user_id,rest_id,avialble_rest,sort_pop,sort_fit,sort_sim,fit_score,sim_score,c1_fit,c2_fit,c3_fit,c4_fit,c5_fit,fit_rank,sim_rank,pop_rank,tip,category,dish,price,time, group_id FROM log_visited_rest WHERE user_id = {user[0]} "
                    my_cursor = self.mysql_conn.cursor(buffered=True)
                    my_cursor.execute(query)
                    for rest in my_cursor:
                        writer.writerow([int(user[0]), int(rest[21]),int(rest[1]),int(rest[2]),int(rest[3]),int(rest[4]),int(rest[5]),int(rest[6]),int(rest[7]),int(rest[8]),int(rest[9]),int(rest[10]),int(rest[11]),int(rest[12]),int(rest[13]),int(rest[14]),int(rest[15]),int(rest[16]),int(rest[17]),int(rest[18]),rest[19],rest[20]])
            file.close()
    
    def get_organizer_booked_rest(self):
        with open("OutPuts/organizer_booked_single.csv", 'w') as file:
            writer = csv.writer(file)
            writer.writerow(['user_id', 'group_id','rest_id','avialble_rest','sort_pop','sort_fit','sort_sim','fit_score','sim_score','c1_fit','c2_fit','c3_fit','c4_fit','c5_fit','fit_rank','sim_rank','pop_rank','tip','category','dish','price','time'])
            query = "SELECT DISTINCT(user_id) FROM  user_group_info"
            my_cursor = self.mysql_conn.cursor(buffered=True)
            my_cursor.execute(query)
            first_account_id_set = self.get_first_account_id()
            for user in my_cursor:
                if user[0] in first_account_id_set and (14912 >= user[0] >= 14639  or 20798 >= user[0] >= 20734):
                    query = f"SELECT user_id,rest_id,avialble_rest,sort_pop,sort_fit,sort_sim,fit_score,sim_score,c1_fit,c2_fit,c3_fit,c4_fit,c5_fit,fit_rank,sim_rank,pop_rank,tip,category,dish,price,time, group_id FROM log_booked WHERE user_id = {user[0]} "
                    my_cursor = self.mysql_conn.cursor(buffered=True)
                    my_cursor.execute(query)
                    for rest in my_cursor:
                        writer.writerow([user[0],int(rest[21]) ,int(rest[1]),int(rest[12]),int(rest[3]),int(rest[4]),int(rest[5]),int(rest[6]),int(rest[7]),int(rest[8]),int(rest[9]),int(rest[10]),int(rest[11]),int(rest[12]),int(rest[13]),int(rest[14]),int(rest[15]),int(rest[16]),int(rest[17]),int(rest[18]),rest[19],rest[20]])
            file.close()
            
    def get_organizer_used_sorting(self):
        with open("OutPuts/organizer_sorting_single.csv", 'w') as file:
            writer = csv.writer(file)
            writer.writerow(['user_id', 'group_id' , 'type', 'time'])
            query = "SELECT DISTINCT(user_id) FROM  user_group_info"
            my_cursor = self.mysql_conn.cursor(buffered=True)
            my_cursor.execute(query)
            counter = 0
            first_account_id_set = self.get_first_account_id()
            for user in my_cursor:
                if user[0] in first_account_id_set and (14912 >= user[0] >= 14639  or 20798 >= user[0] >= 20734):
                    query = f"SELECT sorting_book,sorting_fit,sorting_sim, time, group_id FROM log_sorting_type WHERE user_id = {user[0]} "
                    my_cursor = self.mysql_conn.cursor(buffered=True)
                    my_cursor.execute(query)
                    for sorting in my_cursor:
                        counter += 1
                        if counter != 1:
                            temp_list = [user[0]]
                            temp_list.append(sorting[4])
                            if int(sorting[0]) == 1:
                                temp_list.append('pop')
                            elif int(sorting[1]) == 1:
                                temp_list.append('fit')
                            elif int(sorting[2]) == 1:
                                temp_list.append('sim')
                            temp_list.append(sorting[3])
                            writer.writerow(temp_list)
            file.close()
            
    def get_organizer_used_explanasion(self):
        with open("OutPuts/organizer_explanasions_single.csv", 'w') as file:
            writer = csv.writer(file)
            writer.writerow(['user_id', 'type', 'time'])
            query = "SELECT DISTINCT(user_id) FROM  user_group_info"
            my_cursor = self.mysql_conn.cursor(buffered=True)
            my_cursor.execute(query)
            first_account_id_set = self.get_first_account_id()
            for user in my_cursor:
                if user[0] in first_account_id_set and (14912 >= user[0] >= 14639  or 20798 >= user[0] >= 20734):
                    query = f"SELECT popularity,fitness,sim,trip,category,dish,time_enter FROM log_explanasion_type WHERE user_id = {user[0]} "
                    my_cursor = self.mysql_conn.cursor(buffered=True)
                    my_cursor.execute(query)
                    for sorting in my_cursor:
                        temp_list = [user[0]]
                        if int(sorting[0]) == 1:
                            temp_list.append('pop')
                        elif int(sorting[1]) == 1:
                            temp_list.append('fit')
                        elif int(sorting[2]) == 1:
                            temp_list.append('sim')
                        elif int(sorting[3]) == 1:
                            temp_list.append('trip')
                        elif int(sorting[4]) == 1:
                            temp_list.append('category')
                        elif int(sorting[5]) == 1:
                            temp_list.append('dish')
                        temp_list.append(sorting[6])
                        writer.writerow(temp_list)
            file.close()
            
    def get_organizer_conflict(self):
        with open("OutPuts/organizer_conflict_single.csv", 'w') as file:
            writer = csv.writer(file)
            writer.writerow(['user_id', 'for_user', 'time'])
            query = "SELECT DISTINCT(user_id) FROM  user_group_info"
            my_cursor = self.mysql_conn.cursor(buffered=True)
            my_cursor.execute(query)
            first_account_id_set = self.get_first_account_id()
            for user in my_cursor:
                if user[0] in first_account_id_set and (14912 >= user[0] >= 14639  or 20798 >= user[0] >= 20734):
                    query = f"SELECT user_to_add_id,time FROM log_conflict WHERE user_id = {user[0]} "
                    my_cursor = self.mysql_conn.cursor(buffered=True)
                    my_cursor.execute(query)
                    for conflict in my_cursor:
                        temp_list = [user[0], conflict[0], conflict[1]]
                        writer.writerow(temp_list)
            file.close()
             
    def get_organizer_usage_conflict(self):
        with open("OutPuts/organizer_usage_conflict_single.csv", 'w') as file:
            writer = csv.writer(file)
            writer.writerow(['user_id', 'for_user','limiting_member','CROSTACEI_E_MOLLUSCHI','FUNGHI','FORMAGGI','VERDURE','PESCE','RISO','PASTA','INTERIORA','LEGUMI','TORTELLINI','GNOCCHI','CARNE','PIZZA','SALUMI','revision_number','avialble_before','avialble_after','user_available_before','user_available_after','time'])
            query = "SELECT DISTINCT(user_id) FROM  user_group_info"
            my_cursor = self.mysql_conn.cursor(buffered=True)
            my_cursor.execute(query)
            first_account_id_set = self.get_first_account_id()
            for user in my_cursor:
                if user[0] in first_account_id_set and (14912 >= user[0] >= 14639  or 20798 >= user[0] >= 20734):
                    query = f"SELECT vconflict_id,limiting_member,CROSTACEI_E_MOLLUSCHI,FUNGHI,FORMAGGI,VERDURE,PESCE,RISO,PASTA,INTERIORA,LEGUMI,TORTELLINI,GNOCCHI,CARNE,PIZZA,SALUMI,revision_number,avialble_before,avialble_after,user_available_before,user_available_after,time FROM log_conflict_usage WHERE user_id = {user[0]} "
                    my_cursor = self.mysql_conn.cursor(buffered=True)
                    my_cursor.execute(query)
                    for conflict in my_cursor:
                        temp_list = [user[0], conflict[0], conflict[1], int(conflict[2]), int(conflict[3]), int(conflict[4]), int(conflict[5]), int(conflict[6]), int(conflict[7]), int(conflict[8]), int(conflict[9]), int(conflict[10]), int(conflict[11]), int(conflict[12]), int(conflict[13]), int(conflict[14]), int(conflict[15]), conflict[16], conflict[17], conflict[18], conflict[19], conflict[20], conflict[21]]
                        writer.writerow(temp_list)
            file.close()
            
    def get_organizer_remember(self):
        with open("OutPuts/organizer_remeber_single.csv", 'w') as file:
            writer = csv.writer(file)
            writer.writerow(['user_id', 'for_user', 'type', 'time'])
            query = "SELECT DISTINCT(user_id) FROM  user_group_info"
            my_cursor = self.mysql_conn.cursor(buffered=True)
            my_cursor.execute(query)
            first_account_id_set = self.get_first_account_id()
            for user in my_cursor:
                if user[0] in first_account_id_set and (14912 >= user[0] >= 14639  or 20798 >= user[0] >= 20734):
                    query = f"SELECT remebr_user_id,remembring_pop,remembring_detialed,time FROM log_rembering WHERE user_id = {user[0]} "
                    my_cursor = self.mysql_conn.cursor(buffered=True)
                    my_cursor.execute(query)
                    for remeber in my_cursor:
                        temp_list = [user[0], remeber[0]]
                        if int(remeber[1]) == 1:
                            temp_list.append('pop')
                        elif int(remeber[2]) == 1:
                            temp_list.append('info')
                        temp_list.append(remeber[3])
                        writer.writerow(temp_list)
            file.close()
            
    def get_organizer_usage_remember(self):
        with open("OutPuts/organizer_usage_remeber_single_time_added.csv", 'w') as file:
            writer = csv.writer(file)
            writer.writerow(['user_id', 'for_user','CROSTACEI_E_MOLLUSCHI','FUNGHI','FORMAGGI','VERDURE','PESCE','RISO','PASTA','INTERIORA','LEGUMI','TORTELLINI','GNOCCHI','CARNE','PIZZA','SALUMI','avialble_before','avialble_after','user_available_before','user_available_after','time'])
            query = "SELECT DISTINCT(user_id) FROM  user_group_info"
            my_cursor = self.mysql_conn.cursor(buffered=True)
            my_cursor.execute(query)
            first_account_id_set = self.get_first_account_id()
            for user in my_cursor:
                if user[0] in first_account_id_set and (14912 >= user[0] >= 14639  or 20798 >= user[0] >= 20734):
                    query = f"SELECT rembering_id,CROSTACEI_E_MOLLUSCHI,FUNGHI,FORMAGGI,VERDURE,PESCE,RISO,PASTA,INTERIORA,LEGUMI,TORTELLINI,GNOCCHI,CARNE,PIZZA,SALUMI,avialble_before,avialble_after,user_available_before,user_available_after,time FROM log_rembering_usage WHERE user_id = {user[0]} "
                    my_cursor = self.mysql_conn.cursor(buffered=True)
                    my_cursor.execute(query)
                    for remeber in my_cursor:
                        temp_list = [user[0], remeber[0], int(remeber[1]), int(remeber[2]), int(remeber[3]), int(remeber[4]), int(remeber[5]), int(remeber[6]), int(remeber[7]), int(remeber[8]), int(remeber[9]), int(remeber[10]), int(remeber[11]), int(remeber[12]), int(remeber[13]), int(remeber[14]), remeber[15], remeber[16], remeber[17], remeber[18], remeber[19]]
                        writer.writerow(temp_list)
            file.close()
            
    def extrac_preference_insertion(self):
         with open("OutPuts/preference_insertion_table_single.csv", 'w') as file:
            writer = csv.writer(file)
            writer.writerow(['user_id', 'group_id','preference','time', 'delete'])
            query = "SELECT group_id,interaction,ts FROM interaction"
            my_cursor = self.mysql_conn.cursor(buffered=True)
            my_cursor.execute(query)
            first_account_id_set = self.get_first_account_id()
            for row in my_cursor:
                temp_list = []
                interaction_string_list = row[1].split(" ")
                if (interaction_string_list[0] == "Preference"):
                    if str(interaction_string_list[-1]) != 'undefined' and (21734 >= int(interaction_string_list[-1]) >= 14639 ):
                        temp_list.append(interaction_string_list[-1])
                        temp_list.append(row[0])
                        temp_list.append(interaction_string_list[1])
                        temp_list.append(row[2].strftime("%Y-%m-%d %H:%M:%S"))
                        temp_list.append(0)
                        writer.writerow(temp_list)
            file.close()
            df_preferenc = pd.read_csv("OutPuts/preference_insertion_table_single.csv")
            # df_duplicated = df_preferenc[df_preferenc[['user_id', 'group_id','preference']].duplicated()]
            # print(df_preferenc.drop_duplicates(subset=['user_id', 'group_id','preference'], keep='last'))
            for duplicated_rows in df_preferenc[df_preferenc[['user_id', 'group_id','preference']].duplicated(keep='last')].to_dict(orient="records"):
                df_repition = df_preferenc.loc[(df_preferenc["user_id"] == duplicated_rows['user_id'])  & (df_preferenc["group_id"] == duplicated_rows['group_id'])  & (df_preferenc["preference"] == duplicated_rows['preference'])]
                indexing = 0
                for repition in df_repition.values:
                    if indexing % 2 == 1:
                        df_preferenc.loc[(df_preferenc["user_id"] == duplicated_rows['user_id'])  & (df_preferenc["group_id"] == duplicated_rows['group_id'])  & (df_preferenc["preference"] == duplicated_rows['preference']) & (df_preferenc["time"] == repition[3]) ,'delete'] = 1
                    indexing += 1
            df_preferenc.to_csv("OutPuts/preference_insertion_deleted_table_single.csv")
                             
    def update_individual_scores(self):
        df_preferenc = pd.read_csv("OutPuts/organizer_visiting_single.csv").reindex()
        for index, row in df_preferenc.iterrows():
            print(index)
            max_member_size = 5
            group_id = row['group_id']
            rest_id = row['rest_id']
            visiting_time = row['time']
            relevance_scores = self.attractiveness(group_id, visiting_time)
            counter = 0
            scores_sum = 0
            for key,value in relevance_scores.items():
                counter += 1
                if counter <= max_member_size:
                    setting_position = 'c' + str(counter) + '_fit'
                    df_preferenc.iloc[index, df_preferenc.columns.get_loc(setting_position)] = value[rest_id]
                    scores_sum += value[rest_id]
            if counter > 0:
                df_preferenc.iloc[index, df_preferenc.columns.get_loc('fit_score')] = scores_sum / counter
            df_preferenc.iloc[index, df_preferenc.columns.get_loc('sim_score')] = self.similarity(group_id,rest_id , visiting_time)
        df_preferenc.to_csv("OutPuts/organizer_visiting_cleaned_single.csv")
        print("First Done")
        df_preferenc = pd.read_csv("OutPuts/organizer_booked_single.csv").reindex()
        for index, row in df_preferenc.iterrows():
            print(index)
            max_member_size = 5
            group_id = row['group_id']
            rest_id = row['rest_id']
            visiting_time = row['time']
            relevance_scores = self.attractiveness(group_id, visiting_time)
            counter = 0
            scores_sum = 0
            for key,value in relevance_scores.items():
                counter += 1
                if counter <= max_member_size:
                    setting_position = 'c' + str(counter) + '_fit'
                    df_preferenc.iloc[index, df_preferenc.columns.get_loc(setting_position)] = value[rest_id]
                    scores_sum += value[rest_id]
            if counter > 0:
                df_preferenc.iloc[index, df_preferenc.columns.get_loc('fit_score')] = scores_sum / counter
            df_preferenc.iloc[index, df_preferenc.columns.get_loc('sim_score')] = self.similarity(group_id,rest_id , visiting_time)
        df_preferenc.to_csv("OutPuts/organizer_booked_cleaned_single.csv")
                
    def update_rest_info(self):
        df_preferenc = pd.read_csv("OutPuts/organizer_visiting_cleaned_single.csv").reindex()
        for index, row in df_preferenc.iterrows():
            rest_id = row['rest_id']
            menu = Restaurant(self.mysql_conn).get_restaurant_menu_id(rest_id)
            del menu['id']
            category_counter = 0
            for key in menu.keys():
                if len(menu[key]):
                    category_counter += 1
            df_preferenc.iloc[index, df_preferenc.columns.get_loc('category')] = category_counter
        df_preferenc.to_csv("OutPuts/organizer_visiting_cleaned_single.csv")
        
        df_preferenc = pd.read_csv("OutPuts/organizer_booked_cleaned_single.csv").reindex()
        for index, row in df_preferenc.iterrows():
            rest_id = row['rest_id']
            menu = Restaurant(self.mysql_conn).get_restaurant_menu_id(rest_id)
            del menu['id']
            category_counter = 0
            for key in menu.keys():
                if len(menu[key]):
                    category_counter += 1
            df_preferenc.iloc[index, df_preferenc.columns.get_loc('category')] = category_counter
        df_preferenc.to_csv("OutPuts/organizer_booked_cleaned_single.csv")
            
    def attractiveness(self, group_id, visiting_time):
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
                member_preference_dict[user] = self.get_list_of_preferences(user, group_id, visiting_time, user_preference)
        relevance_score = 0
        for user, preference in member_preference_dict.items():
            relevance_score_normalized = dict()
            if (len(preference) > 0):
                relevance_score = dict()
                for item in preference:
                    if len(relevance_score)  == 0:
                        relevance_score = Supplementary(None, self.mysql_conn).relevance_score(preference=item)
                    else:
                        a_counter = Supplementary(None, self.mysql_conn).relevance_score(preference=item)
                        b_counter = relevance_score
                        for key, value in a_counter.items():
                            # relevance_score[key] = value + b_counter[key]
                            relevance_score[key] = max(value, b_counter[key])
                            b_counter[key] = relevance_score[key]
                    # relevance_score = relevance_score + Supplementary(self.post_conn, self.mysql_conn).relevance_score(preference=item)
                # user_relevance_dict[user] = relevance_score
                # max_val = relevance_score[max(relevance_score, key=relevance_score.get)]
                # min_val = relevance_score[min(relevance_score, key=relevance_score.get)]
                for k, value in relevance_score.items():
                    # if max_val - min_val == 0:
                    relevance_score_normalized[k] = value
                        # relevance_score_normalized[k] = math.log10(1 * 9 + 1)  #Maping between [1,10] and using log10
                    # else:
                        # relevance_score_normalized[k] = math.log10(((value - min_val) / (max_val - min_val) * 9) + 1)  #Maping between [1,10] and using log10
                        # relevance_score_normalized[k] = (value - min_val) / (max_val - min_val)
                        # relevance_score_normalized[k] = value
                relevance_score_normalized = dict(sorted(relevance_score_normalized.items(), key=lambda item: item[1], reverse=True))
                user_relevance_dict[user] = relevance_score_normalized
        return user_relevance_dict
    
    def similarity(self, group_id, rest_id, visiting_time):
        query_delete = f"DELETE FROM similarity_explan WHERE group_id = {group_id} AND restaurant_id = {rest_id}"
        cursor_user_delete = self.mysql_conn.cursor(buffered=True)
        cursor_user_delete.execute(query_delete)
        group_id = group_id
        restaurant_id = rest_id
        similarity_list = []
        
        user_list_current = []
        query_user = f"SELECT id FROM user WHERE group_id = {group_id}"
        cursor_user = self.mysql_conn.cursor(buffered=True)
        cursor_user.execute(query_user)
        group_preference_dict = dict()
        number_of_liked_group = 0
        member_preference_cleaned = []
        for user in cursor_user:
            user_list_current.append(int(user[0]))
        for user in user_list_current:
            user_preference_current = []
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
                member_preference_cleaned.extend(self.get_list_of_preferences(user, group_id, visiting_time, user_preference_current))
        query = f"SELECT group_id FROM bookmarks WHERE restaurant_id = {restaurant_id} AND group_id != {group_id}"
        cursor = self.mysql_conn.cursor(buffered=True)
        cursor.execute(query)
        user_preference_current = member_preference_cleaned
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
        # json_object = str(json.dumps(group_preference_dict))
        # group_id_int = int(group_rest_info['groupId'])
        # group_rest_int = int(group_rest_info["restaurantId"])
        # query_submit = f"INSERT INTO similarity_explan (group_id, sim, restaurant_id) VALUES ({group_id_int}," + f"'{json_object}'" + f", { group_rest_int})"
        # cursor_user_submit = self.mysql_conn.cursor(buffered=True)
        # cursor_user_submit.execute(query_submit)
        if(len(similarity_list) == 0):
            return 0
        else: 
            return np.mean(similarity_list)
    
    def get_list_of_preferences(self, user_id, group_id, visiting_time, preferences_list):
        df_preferences = pd.read_csv("OutPuts/preference_insertion_deleted_table.csv")
        preference_list_output = []
        flag = False
        for preference in preferences_list:
            preferences_insertion = df_preferences.loc[(df_preferences['user_id'] == int(user_id)) & (df_preferences['group_id'] == group_id) & (df_preferences['preference'] == preference) & (df_preferences['time'] <= visiting_time)]
            preferences_insertion.sort_values(by=['time'])
            if len(preferences_insertion) and int(preferences_insertion.iloc[-1].values[-1]) == int(0):
                preference_list_output.append(preferences_insertion.iloc[-1].values[3])
        return preference_list_output
            
    def groups_sizes(self):
        groups = pd.read_csv("OutPuts/groups_members.csv")
        with open("OutPuts/member_group_size.csv", 'w') as file:
            writer = csv.writer(file)
            writer.writerow(['index', 'user_id', 'size'])
            added_member = []
            for index, group in groups.iterrows():
                group_member_list = [x for x in list(group)[1:] if str(x) != 'nan']
                for member in group_member_list:
                    if int(member) not in added_member:
                        added_member.append(int(member))
                        writer.writerow([index, int(member), len(group_member_list)])
                    