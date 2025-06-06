from array import array
import csv
from typing import get_type_hints
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import scipy.stats as stats
import pandas as pd

       
class DataEvaluation(object):
    def __init__(self,connection_mysql):
        self.mysql_conn = connection_mysql
        
        
    def get_number_of_accounts_first_stage(self):
        query = "SELECT user_id,personal_info,decision_making,post_rating FROM progress"
        my_cursor = self.mysql_conn.cursor(buffered=True)
        my_cursor.execute(query)
        counter_personal_info = 0
        counter_decision_making = 0
        counter_post_rating = 0
        for user in my_cursor:
            if 14912 >= user[0] >= 14639  or 20798 >= user[0] >= 20734:
                if int(user[1]) == 1:
                    counter_personal_info += 1
                    if int(user[2]) == 1:
                        counter_decision_making += 1
                        if int(user[3]) == 1:
                            counter_post_rating += 1
        print(counter_personal_info,counter_decision_making,counter_post_rating)
         
    def get_demographic_info(self):
        query = "SELECT DISTINCT(user_id),gender,nationality,age FROM user_info"
        my_cursor = self.mysql_conn.cursor(buffered=True)
        my_cursor.execute(query)
        list_gender = []
        list_nationality = []
        list_age = []
        for user in my_cursor:
            if 14912 >= user[0] >= 14639  or 20798 >= user[0] >= 20734:
                list_gender.append(user[1])
                list_nationality.append(user[2])
                list_age.append(user[3])
                
        bins = len(set(list_gender))
        counts, edges, bars = plt.hist(list_gender, bins=2)
        plt.xticks(np.arange(0, 3),rotation=90)
        plt.title('Gender Distribution')
        plt.xlabel('Gender')
        plt.ylabel('Number of users')
        plt.bar_label(bars)
        plt.savefig('plots/gender_histogram.png')
        
        plt.clf()
        bins = len(set(list_nationality))
        counts, edges, bars = plt.hist(list_nationality, bins=bins)
        plt.xticks(np.arange(0,len(set(list_nationality))),rotation=90)
        plt.title('Nationality Distribution')
        plt.xlabel('Nationality')
        plt.ylabel('Number of users')
        plt.bar_label(bars)
        plt.savefig('plots/nationality_histogram.png')
        
        plt.clf()
        bins = np.arange(np.min(list_age) - 1, np.max(list_age) + 1, 1)
        plt.hist(list_gender, bins=bins)
        plt.xticks(np.arange(np.min(list_age) - 1, np.max(list_age) + 1, 3),rotation=90)
        plt.title('Age Distribution')
        plt.xlabel('Age')
        plt.ylabel('Number of users')
        plt.savefig('plots/age_histogram.png')

        print(np.mean(list_age))
            
    def get_group_type(self,group_type):
        if group_type == "G1" or group_type == "G2" or group_type == "G3" or group_type == "G4":
            return 1
        elif  group_type == "G5" or group_type == "G6" or group_type == "G7" or group_type == "G8":
            return 2
        elif  group_type == "G9" or group_type == "G10" or group_type == "G11" or group_type == "G12":
            return 3
        
    def get_system_type(self,group_type):
        if group_type == "G1" or group_type == "G5" or group_type == "G9":
            return "No"
        elif  group_type == "G2" or group_type == "G6" or group_type == "G10":
            return "R"
        elif  group_type == "G3" or group_type == "G7" or group_type == "G11": 
            return "I"
        elif  group_type == "G4" or group_type == "G8" or group_type == "G12": 
            return "RI"
    
    def get_group_average(self):
        tripScore = {1: 4,2: 4.5,3: 4,4: 4,5: 4,6: 4,7: 4.5,8: 3.5,9: 3,10: 4.5,11: 4.5,12: 4.5,13: 4.5,15: 4.5,16: 4.5,17: 4,18: 5,19: 4,20: 4,21: 2,22: 4.5,23: 4,24: 4.5,25: 4,26: 4.5,27: 3.5,28: 4.5,29: 3.5,30: 5,31: 4.5,32: 5}
        df = pd.DataFrame(columns=["user_id", "organizer_id", "group_type", "system_type", "rest_id", "rating", "rest_trip_score"])
        plt.clf()
        group_type_rating_dict = {'G1':list(), 'G2':list(), 'G3':list(), 'G4':list(), 'G5':list(), 'G6':list(), 'G7':list(), 'G8':list(), 'G9':list(), 'G10':list(), 'G11':list(), 'G12':list()}
        df_groups_type = pd.read_csv("OutPuts/group_organizer_type.csv")
        df_group_ratings = pd.read_csv("OutPuts/group_ratings.csv")
        for index, row in df_groups_type.iterrows():
            organizer = row['organizer']
            group_type = row['type']
            group_only_type = self.get_group_type(group_type)
            system_type = self.get_system_type(group_type)
            df_groups = pd.read_csv("OutPuts/groups_members.csv")
            df_groups.fillna(-1,inplace=True)
            for group_index, group_row in df_groups.iterrows():
                group_set = set([int(group_row['member1']), int(group_row['member2']), int(group_row['member3']), int(group_row['member4']), int(group_row['member5'])])
                if -1 in group_set:
                    group_set.remove(-1)
                organizer_choice = self.get_organizer_choice(organizer)
                if int(organizer) in group_set:
                    group_members_list = list(group_set)
                    for member in group_members_list:
                        for restaurant in organizer_choice:
                            df_temp = df_group_ratings.loc[(df_group_ratings['user'] == member) & (df_group_ratings['restaurant'] == restaurant)]
                            new_list = group_type_rating_dict[group_type].extend(list(df_temp['rating'].values))
                            for rating in list(df_temp['rating'].values):
                                df = df.append(pd.DataFrame([[member,organizer,group_only_type,system_type,restaurant,rating, tripScore[restaurant]]], columns=["user_id", "organizer_id", "group_type", "system_type", "rest_id", "rating", "rest_trip_score"]))
                            if new_list != None:
                                group_type_rating_dict[group_type] = new_list
        group_type_avr_rating_dict = dict()
        for key in group_type_rating_dict.keys():
            if len(group_type_rating_dict[key]) > 0:
                group_type_avr_rating_dict[key] = np.average(group_type_rating_dict[key])
        df.drop_duplicates(subset=["user_id","organizer_id"],inplace=True)
        df.to_csv("OutPuts/df_groups_ratings_with_trip_score.csv")
        input("Done")
        plt.bar(list(group_type_avr_rating_dict.keys()), list(group_type_avr_rating_dict.values()), align='center')
        plt.xticks(range(len(group_type_avr_rating_dict)), list(group_type_avr_rating_dict.keys()))
        plt.ylim(3, 5)
        plt.savefig('plots/group_type_average.png')
        
        plt.clf()
        keys_list = ['','N', 'R', 'I', 'RI']
        values_list_N = []
        values_list_N.extend(group_type_rating_dict['G1'])
        values_list_N.extend(group_type_rating_dict['G5'])
        values_list_N.extend(group_type_rating_dict['G9'])
        values_list_R = []
        values_list_R.extend(group_type_rating_dict['G2'])
        values_list_R.extend(group_type_rating_dict['G6'])
        values_list_R.extend(group_type_rating_dict['G10'])
        values_list_I = []
        values_list_I.extend(group_type_rating_dict['G3'])
        values_list_I.extend(group_type_rating_dict['G7'])
        values_list_I.extend(group_type_rating_dict['G11'])
        values_list_RI = []
        values_list_RI.extend(group_type_rating_dict['G4'])
        values_list_RI.extend(group_type_rating_dict['G8'])
        values_list_RI.extend(group_type_rating_dict['G12'])
        fig, ax = plt.subplots()
        ax.boxplot([values_list_N,values_list_R,values_list_I,values_list_RI])
        # plt.box([values_list_N,values_list_R,values_list_I,values_list_RI])
        # self.addlabels(keys_list, values_list)
        plt.xticks(range(len(keys_list)), list(keys_list))
        # plt.ylim(3, 4.5)
        plt.title("Ratings for final choices")
        plt.savefig('plots/group_type_average_all_box.png')
        # input("Yes")
        
        plt.clf()
        keys_list = ['','N', 'R', 'I', 'RI']
        values_list_N = []
        values_list_N.extend(group_type_rating_dict['G1'])
        # values_list_N.extend(group_type_rating_dict['G5'])
        # values_list_N.extend(group_type_rating_dict['G9'])
        values_list_R = []
        values_list_R.extend(group_type_rating_dict['G2'])
        # values_list_R.extend(group_type_rating_dict['G6'])
        # values_list_R.extend(group_type_rating_dict['G10'])
        values_list_I = []
        values_list_I.extend(group_type_rating_dict['G3'])
        # values_list_I.extend(group_type_rating_dict['G7'])
        # values_list_I.extend(group_type_rating_dict['G11'])
        values_list_RI = []
        values_list_RI.extend(group_type_rating_dict['G4'])
        # values_list_RI.extend(group_type_rating_dict['G8'])
        # values_list_RI.extend(group_type_rating_dict['G12'])
        fig, ax = plt.subplots()
        ax.boxplot([values_list_N,values_list_R,values_list_I,values_list_RI])
        # plt.box([values_list_N,values_list_R,values_list_I,values_list_RI])
        # self.addlabels(keys_list, values_list)
        plt.xticks(range(len(keys_list)), list(keys_list))
        # plt.ylim(3, 4.5)
        plt.title("Ratings to final choices for groups with no information")
        plt.savefig('plots/group_type_average_No_box.png')
        # input("Yes")
        
        plt.clf()
        keys_list = ['','N', 'R', 'I', 'RI']
        values_list_N = []
        # values_list_N.extend(group_type_rating_dict['G1'])
        values_list_N.extend(group_type_rating_dict['G5'])
        # values_list_N.extend(group_type_rating_dict['G9'])
        values_list_R = []
        # values_list_R.extend(group_type_rating_dict['G2'])
        values_list_R.extend(group_type_rating_dict['G6'])
        # values_list_R.extend(group_type_rating_dict['G10'])
        values_list_I = []
        # values_list_I.extend(group_type_rating_dict['G3'])
        values_list_I.extend(group_type_rating_dict['G7'])
        # values_list_I.extend(group_type_rating_dict['G11'])
        values_list_RI = []
        # values_list_RI.extend(group_type_rating_dict['G4'])
        values_list_RI.extend(group_type_rating_dict['G8'])
        # values_list_RI.extend(group_type_rating_dict['G12'])
        fig, ax = plt.subplots()
        ax.boxplot([values_list_N,values_list_R,values_list_I,values_list_RI])
        # plt.box([values_list_N,values_list_R,values_list_I,values_list_RI])
        # self.addlabels(keys_list, values_list)
        plt.xticks(range(len(keys_list)), list(keys_list))
        # plt.ylim(3, 4.5)
        plt.title("Ratings to final choices for groups with partial information")
        plt.savefig('plots/group_type_average_partial_box.png')
        # input("Yes")
        
        plt.clf()
        keys_list = ['','N', 'R', 'I', 'RI']
        values_list_N = []
        # values_list_N.extend(group_type_rating_dict['G1'])
        # values_list_N.extend(group_type_rating_dict['G5'])
        values_list_N.extend(group_type_rating_dict['G9'])
        values_list_R = []
        # values_list_R.extend(group_type_rating_dict['G2'])
        # values_list_R.extend(group_type_rating_dict['G6'])
        values_list_R.extend(group_type_rating_dict['G10'])
        values_list_I = []
        # values_list_I.extend(group_type_rating_dict['G3'])
        # values_list_I.extend(group_type_rating_dict['G7'])
        values_list_I.extend(group_type_rating_dict['G11'])
        values_list_RI = []
        # values_list_RI.extend(group_type_rating_dict['G4'])
        # values_list_RI.extend(group_type_rating_dict['G8'])
        values_list_RI.extend(group_type_rating_dict['G12'])
        fig, ax = plt.subplots()
        ax.boxplot([values_list_N,values_list_R,values_list_I,values_list_RI])
        # plt.box([values_list_N,values_list_R,values_list_I,values_list_RI])
        # self.addlabels(keys_list, values_list)
        plt.xticks(range(len(keys_list)), list(keys_list))
        # plt.ylim(3, 4.5)
        plt.title("Ratings to final choices for groups with full information")
        plt.savefig('plots/group_type_average_full_box.png')
        # input("Yes")
        
        
        
        plt.clf()
        keys_list = ['N', 'R', 'I', 'RI']
        values_list = [(group_type_avr_rating_dict[x] + group_type_avr_rating_dict[y] + group_type_avr_rating_dict[z])/3 for x,y,z in zip(['G1', 'G2', 'G3', 'G4'],['G5', 'G6', 'G7', 'G8'],['G9', 'G10', 'G11', 'G12'])]
        plt.bar(keys_list, values_list, align='center')
        self.addlabels(keys_list, values_list)
        plt.xticks(range(len(values_list)), list(keys_list))
        plt.ylim(3, 4.5)
        plt.title("Average rating for final choices")
        plt.savefig('plots/group_type_average_all.png')
        
        plt.clf()
        keys_list = ['N', 'R', 'I', 'RI']
        values_list = [group_type_avr_rating_dict[x] for x in ['G1', 'G2', 'G3', 'G4']]
        plt.bar(keys_list, values_list, align='center')
        self.addlabels(keys_list, values_list)
        plt.xticks(range(len(values_list)), list(keys_list))
        plt.ylim(3, 4.5)
        plt.title("Average rating for groups with no information")
        plt.savefig('plots/group_type_average_l1.png')
        
        plt.clf()
        keys_list = ['N', 'R', 'I', 'RI']
        values_list = [group_type_avr_rating_dict[x] for x in ['G5', 'G6', 'G7', 'G8']]
        plt.bar(keys_list, values_list, align='center')
        self.addlabels(keys_list, values_list)
        plt.xticks(range(len(values_list)), list(keys_list))
        plt.ylim(3, 4.5)
        plt.title("Average rating for groups with partial information")
        plt.savefig('plots/group_type_average_l2.png')
        
        plt.clf()
        keys_list = ['N', 'R', 'I', 'RI']
        values_list = [group_type_avr_rating_dict[x] for x in ['G9', 'G10', 'G11', 'G12']]
        plt.bar(keys_list, values_list, align='center')
        self.addlabels(keys_list, values_list)
        plt.xticks(range(len(values_list)), list(keys_list))
        plt.ylim(3, 4.5)
        plt.title("Average rating for groups with full information")
        plt.savefig('plots/group_type_average_l3.png')
        
    def addlabels(self, x,y):
        for i in range(len(x)):
            plt.text(i, y[i], round(y[i],2), ha = 'center')
        
    def get_group_size_average(self):
        plt.clf()
        group_type_rating_dict = {'G12':list(), 'G13':list(), 'G14':list(), 'G15':list(), 'G22':list(), 'G23':list(), 'G24':list(), 'G25':list(), 'G32':list(), 'G33':list(), 'G34':list(), 'G35':list(), 'G42':list(), 'G43':list(), 'G44':list(), 'G45':list(), 'G52':list(), 'G53':list(), 'G54':list(), 'G55':list(), 'G62':list(), 'G63':list(), 'G64':list(), 'G65':list(), 'G72':list(), 'G73':list(), 'G74':list(), 'G75':list(), 'G82':list(), 'G83':list(), 'G84':list(), 'G85':list(), 'G92':list(), 'G93':list(), 'G94':list(), 'G95':list(), 'G102':list(),  'G103':list(),  'G104':list(),  'G105':list(), 'G112':list(), 'G113':list(), 'G114':list(), 'G115':list(), 'G122':list(), 'G123':list(), 'G124':list(), 'G125':list()}
        df_groups_type = pd.read_csv("OutPuts/group_organizer_type.csv")
        df_group_ratings = pd.read_csv("OutPuts/group_ratings.csv")
        df_group_size = pd.read_csv("OutPuts/member_group_size.csv")
        for index, row in df_groups_type.iterrows():
            organizer = row['organizer']
            group_level_type = row['type']
            df_groups = pd.read_csv("OutPuts/groups_members.csv")
            df_groups.fillna(-1,inplace=True)
            for group_index, group_row in df_groups.iterrows():
                group_set = set([int(group_row['member1']), int(group_row['member2']), int(group_row['member3']), int(group_row['member4']), int(group_row['member5'])])
                if -1 in group_set:
                    group_set.remove(-1)
                organizer_choice = self.get_organizer_choice(organizer)
                if int(organizer) in group_set:
                    group_size = df_group_size.loc[df_group_size["user_id"] == int(organizer), "size"].values
                    group_type = str(group_level_type) + str(group_size[0])
                    group_members_list = list(group_set)
                    for member in group_members_list:
                        for restaurant in organizer_choice:
                            df_temp = df_group_ratings.loc[(df_group_ratings['user'] == member) & (df_group_ratings['restaurant'] == restaurant)]
                            new_list = group_type_rating_dict[group_type].extend(list(df_temp['rating'].values))
                            if new_list != None:
                                group_type_rating_dict[group_type] = new_list
        group_type_avr_rating_dict = dict()
        for key in group_type_rating_dict.keys():
            if len(group_type_rating_dict[key]) > 0:
                group_type_avr_rating_dict[key] = np.average(group_type_rating_dict[key])
        width = 0.20
        ind = np.arange(12) 
        bar1 = plt.bar(ind, [group_type_avr_rating_dict["G12"], group_type_avr_rating_dict["G22"], group_type_avr_rating_dict["G32"], group_type_avr_rating_dict["G42"], group_type_avr_rating_dict["G52"], group_type_avr_rating_dict["G62"], group_type_avr_rating_dict["G72"], group_type_avr_rating_dict["G82"], group_type_avr_rating_dict["G92"], group_type_avr_rating_dict["G102"], group_type_avr_rating_dict["G112"], group_type_avr_rating_dict["G122"]], width, color = 'r')
        bar2 = plt.bar(ind+width, [group_type_avr_rating_dict["G13"], group_type_avr_rating_dict["G23"], group_type_avr_rating_dict["G33"], group_type_avr_rating_dict["G43"], group_type_avr_rating_dict["G53"], group_type_avr_rating_dict["G63"], group_type_avr_rating_dict["G73"], group_type_avr_rating_dict["G83"], group_type_avr_rating_dict["G93"], group_type_avr_rating_dict["G103"], group_type_avr_rating_dict["G113"], group_type_avr_rating_dict["G123"]], width, color = 'g')
        bar3 = plt.bar(ind+2*width, [group_type_avr_rating_dict["G14"], group_type_avr_rating_dict["G24"], group_type_avr_rating_dict["G34"], group_type_avr_rating_dict["G44"], group_type_avr_rating_dict["G54"], group_type_avr_rating_dict["G64"], group_type_avr_rating_dict["G74"], group_type_avr_rating_dict["G84"], group_type_avr_rating_dict["G94"], group_type_avr_rating_dict["G104"], group_type_avr_rating_dict["G114"], group_type_avr_rating_dict["G124"]], width, color = 'b')
        bar4 = plt.bar(ind+3*width, [group_type_avr_rating_dict["G15"], group_type_avr_rating_dict["G25"], group_type_avr_rating_dict["G35"], group_type_avr_rating_dict["G45"], group_type_avr_rating_dict["G55"], group_type_avr_rating_dict["G65"], group_type_avr_rating_dict["G75"], group_type_avr_rating_dict["G85"], group_type_avr_rating_dict["G95"], group_type_avr_rating_dict["G105"], group_type_avr_rating_dict["G115"], group_type_avr_rating_dict["G125"]], width, color = 'm')
        N = 3
        ind = np.arange(N) 
        plt.xlabel("Frequency")
        plt.ylabel('Group Types')
        plt.title("Group Type Frequence")
        plt.xticks(np.arange(12)+width,['G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9', 'G10', 'G11', 'G12'])
        plt.legend( (bar1, bar2, bar3, bar4), ('Size = 2', 'Size = 3', 'Size = 4', 'Size = 5') )
        plt.ylim(3, 5)
        plt.savefig('plots/group_type_average_size.png')
        
        plt.clf()
        width = 0.20
        ind = np.arange(4) 
        bar1 = plt.bar(ind, [group_type_avr_rating_dict["G12"], group_type_avr_rating_dict["G22"], group_type_avr_rating_dict["G32"], group_type_avr_rating_dict["G42"]], width, color = 'r')
        bar2 = plt.bar(ind+width, [group_type_avr_rating_dict["G13"], group_type_avr_rating_dict["G23"], group_type_avr_rating_dict["G33"], group_type_avr_rating_dict["G43"]], width, color = 'g')
        bar3 = plt.bar(ind+2*width, [group_type_avr_rating_dict["G14"], group_type_avr_rating_dict["G24"], group_type_avr_rating_dict["G34"], group_type_avr_rating_dict["G44"]], width, color = 'b')
        bar4 = plt.bar(ind+3*width, [group_type_avr_rating_dict["G15"], group_type_avr_rating_dict["G25"], group_type_avr_rating_dict["G35"], group_type_avr_rating_dict["G45"]], width, color = 'm')
        N = 3
        ind = np.arange(N) 
        plt.xlabel("Frequency")
        plt.ylabel('Group Types')
        plt.title("Group Type Frequence")
        plt.xticks(np.arange(4)+width,['G1', 'G2', 'G3', 'G4'])
        plt.legend( (bar1, bar2, bar3, bar4), ('Size = 2', 'Size = 3', 'Size = 4', 'Size = 5') )
        plt.ylim(3, 5)
        plt.savefig('plots/group_type_average_size_l1.png')
        
        plt.clf()
        width = 0.20
        ind = np.arange(4) 
        bar1 = plt.bar(ind, [group_type_avr_rating_dict["G52"], group_type_avr_rating_dict["G62"], group_type_avr_rating_dict["G72"], group_type_avr_rating_dict["G82"]], width, color = 'r')
        bar2 = plt.bar(ind+width, [group_type_avr_rating_dict["G53"], group_type_avr_rating_dict["G63"], group_type_avr_rating_dict["G73"], group_type_avr_rating_dict["G83"]], width, color = 'g')
        bar3 = plt.bar(ind+2*width, [group_type_avr_rating_dict["G54"], group_type_avr_rating_dict["G64"], group_type_avr_rating_dict["G74"], group_type_avr_rating_dict["G84"]], width, color = 'b')
        bar4 = plt.bar(ind+3*width, [group_type_avr_rating_dict["G55"], group_type_avr_rating_dict["G65"], group_type_avr_rating_dict["G75"], group_type_avr_rating_dict["G85"]], width, color = 'm')
        N = 3
        ind = np.arange(N) 
        plt.xlabel("Frequency")
        plt.ylabel('Group Types')
        plt.title("Group Type Frequence")
        plt.xticks(np.arange(4)+width,['G5', 'G6', 'G7', 'G8'])
        plt.legend( (bar1, bar2, bar3, bar4), ('Size = 2', 'Size = 3', 'Size = 4', 'Size = 5') )
        plt.ylim(2, 5)
        plt.savefig('plots/group_type_average_size_l2.png')
        
        plt.clf()
        
        width = 0.20
        ind = np.arange(4) 
        bar1 = plt.bar(ind, [group_type_avr_rating_dict["G92"], group_type_avr_rating_dict["G102"], group_type_avr_rating_dict["G112"], group_type_avr_rating_dict["G122"]], width, color = 'r')
        bar2 = plt.bar(ind+width, [group_type_avr_rating_dict["G93"], group_type_avr_rating_dict["G103"], group_type_avr_rating_dict["G113"], group_type_avr_rating_dict["G123"]], width, color = 'g')
        bar3 = plt.bar(ind+2*width, [group_type_avr_rating_dict["G94"], group_type_avr_rating_dict["G104"], group_type_avr_rating_dict["G114"], group_type_avr_rating_dict["G124"]], width, color = 'b')
        bar4 = plt.bar(ind+3*width, [group_type_avr_rating_dict["G95"], group_type_avr_rating_dict["G105"], group_type_avr_rating_dict["G115"], group_type_avr_rating_dict["G125"]], width, color = 'm')
        N = 3
        ind = np.arange(N) 
        plt.xlabel("Frequency")
        plt.ylabel('Group Types')
        plt.title("Group Type Frequence")
        plt.xticks(np.arange(4)+width,['G9', 'G10', 'G11', 'G12'])
        plt.legend( (bar1, bar2, bar3, bar4), ('Size = 2', 'Size = 3', 'Size = 4', 'Size = 5') )
        plt.ylim(2, 5)
        plt.savefig('plots/group_type_average_size_l3.png')
        
    def get_organizer_choice(self, organizer):
        query = f"SELECT choice FROM user_group_info WHERE user_id = {organizer}"
        my_cursor = self.mysql_conn.cursor(buffered=True)
        my_cursor.execute(query)
        choices_list = []
        for choice in my_cursor:
            choices_list.append(choice[0])
        return choices_list
    
    def avr_individual_loss(self):
        tripScore = {1: 4,2: 4.5,3: 4,4: 4,5: 4,6: 4,7: 4.5,8: 3.5,9: 3,10: 4.5,11: 4.5,12: 4.5,13: 4.5,15: 4.5,16: 4.5,17: 4,18: 5,19: 4,20: 4,21: 2,22: 4.5,23: 4,24: 4.5,25: 4,26: 4.5,27: 3.5,28: 4.5,29: 3.5,30: 5,31: 4.5,32: 5}
        df = pd.DataFrame(columns=["user_id", "organizer_id", "group_type", "system_type", "rest_id", "rating", "rest_trip_score"])
        plt.clf()
        group_type_rating_dict = {'G1':list(), 'G2':list(), 'G3':list(), 'G4':list(), 'G5':list(), 'G6':list(), 'G7':list(), 'G8':list(), 'G9':list(), 'G10':list(), 'G11':list(), 'G12':list()}
        df_groups_type = pd.read_csv("OutPuts/group_organizer_type.csv")
        df_individual_ratings = pd.read_csv("OutPuts/individual_ratings.csv")
        df_booked = pd.read_csv("OutPuts/organizer_booked_cleaned.csv")
        for index, row in df_groups_type.iterrows():
            organizer = row['organizer']
            group_type = row['type']
            group_only_type = self.get_group_type(group_type)
            system_type = self.get_system_type(group_type)
            df_groups = pd.read_csv("OutPuts/groups_members.csv")
            df_groups.fillna(-1,inplace=True)
            for group_index, group_row in df_groups.iterrows():
                group_set = set([int(group_row['member1']), int(group_row['member2']), int(group_row['member3']), int(group_row['member4']), int(group_row['member5'])])
                if -1 in group_set:
                    group_set.remove(-1)
                organizer_choice = self.get_organizer_choice(organizer)
                if int(organizer) in group_set:
                    group_members_list = list(group_set)
                    for member in group_members_list:
                        member_max_score = self.get_member_max_score(member)
                        for restaurant in organizer_choice:
                            df_temp = df_individual_ratings.loc[(df_individual_ratings['user'] == member) & (df_individual_ratings['restaurant'] == restaurant)]
                            new_list = group_type_rating_dict[group_type].extend([member_max_score - x for x in list(df_temp['rating'].values)])
                            if new_list != None:
                                group_type_rating_dict[group_type] = new_list
                            for rating in [member_max_score - x for x in list(df_temp['rating'].values)]:
                                df = df.append(pd.DataFrame([[member,organizer,group_only_type,system_type,restaurant,rating, tripScore[restaurant], ]], columns=["user_id", "organizer_id", "group_type", "system_type", "rest_id", "rating", "rest_trip_score"]))
        group_type_avr_rating_dict = dict()
        plt.clf()
        for key in group_type_rating_dict.keys():
            if len(group_type_rating_dict[key]) > 0:
                group_type_avr_rating_dict[key] = np.average(group_type_rating_dict[key])
        df.drop_duplicates(subset=["user_id","organizer_id"],inplace=True)
        df.to_csv("OutPuts/df_individual_loss_with_trip_score.csv")
        plt.bar(list(group_type_avr_rating_dict.keys()), list(group_type_avr_rating_dict.values()), align='center')
        plt.xticks(range(len(group_type_avr_rating_dict)), list(group_type_avr_rating_dict.keys()))
        plt.ylim(0, 2)

        plt.savefig('plots/avr_individual_loss.png')
        
        plt.clf()
        keys_list = ['','N', 'R', 'I', 'RI']
        values_list_N = []
        values_list_N.extend(group_type_rating_dict['G1'])
        values_list_N.extend(group_type_rating_dict['G5'])
        values_list_N.extend(group_type_rating_dict['G9'])
        values_list_R = []
        values_list_R.extend(group_type_rating_dict['G2'])
        values_list_R.extend(group_type_rating_dict['G6'])
        values_list_R.extend(group_type_rating_dict['G10'])
        values_list_I = []
        values_list_I.extend(group_type_rating_dict['G3'])
        values_list_I.extend(group_type_rating_dict['G7'])
        values_list_I.extend(group_type_rating_dict['G11'])
        values_list_RI = []
        values_list_RI.extend(group_type_rating_dict['G4'])
        values_list_RI.extend(group_type_rating_dict['G8'])
        values_list_RI.extend(group_type_rating_dict['G12'])
        fig, ax = plt.subplots()
        ax.boxplot([values_list_N,values_list_R,values_list_I,values_list_RI])
        # plt.box([values_list_N,values_list_R,values_list_I,values_list_RI])
        # self.addlabels(keys_list, values_list)
        plt.xticks(range(len(keys_list)), list(keys_list))
        # plt.ylim(3, 4.5)
        ax.set_xlabel("Variants")
        ax.set_ylabel("Rating")
        plt.title("MIL for final choices")
        plt.savefig('plots/Loss_all_box.png')
        # input("Yes")
        
        plt.clf()
        keys_list = ['','N', 'R', 'I', 'RI']
        values_list_N = []
        values_list_N.extend(group_type_rating_dict['G1'])
        # values_list_N.extend(group_type_rating_dict['G5'])
        # values_list_N.extend(group_type_rating_dict['G9'])
        values_list_R = []
        values_list_R.extend(group_type_rating_dict['G2'])
        # values_list_R.extend(group_type_rating_dict['G6'])
        # values_list_R.extend(group_type_rating_dict['G10'])
        values_list_I = []
        values_list_I.extend(group_type_rating_dict['G3'])
        # values_list_I.extend(group_type_rating_dict['G7'])
        # values_list_I.extend(group_type_rating_dict['G11'])
        values_list_RI = []
        values_list_RI.extend(group_type_rating_dict['G4'])
        # values_list_RI.extend(group_type_rating_dict['G8'])
        # values_list_RI.extend(group_type_rating_dict['G12'])
        fig, ax = plt.subplots()
        ax.boxplot([values_list_N,values_list_R,values_list_I,values_list_RI])
        # plt.box([values_list_N,values_list_R,values_list_I,values_list_RI])
        # self.addlabels(keys_list, values_list)
        plt.xticks(range(len(keys_list)), list(keys_list))
        # plt.ylim(3, 4.5)
        ax.set_xlabel(['N','R','I','RI'])
        ax.set_ylabel("Rating")
        plt.title("MIL for groups with no information")
        plt.savefig('plots/Loss_No_box.png')
        # input("Yes")
        
        plt.clf()
        keys_list = ['','N', 'R', 'I', 'RI']
        values_list_N = []
        # values_list_N.extend(group_type_rating_dict['G1'])
        values_list_N.extend(group_type_rating_dict['G5'])
        # values_list_N.extend(group_type_rating_dict['G9'])
        values_list_R = []
        # values_list_R.extend(group_type_rating_dict['G2'])
        values_list_R.extend(group_type_rating_dict['G6'])
        # values_list_R.extend(group_type_rating_dict['G10'])
        values_list_I = []
        # values_list_I.extend(group_type_rating_dict['G3'])
        values_list_I.extend(group_type_rating_dict['G7'])
        # values_list_I.extend(group_type_rating_dict['G11'])
        values_list_RI = []
        # values_list_RI.extend(group_type_rating_dict['G4'])
        values_list_RI.extend(group_type_rating_dict['G8'])
        # values_list_RI.extend(group_type_rating_dict['G12'])
        fig, ax = plt.subplots()
        ax.boxplot([values_list_N,values_list_R,values_list_I,values_list_RI])
        # plt.box([values_list_N,values_list_R,values_list_I,values_list_RI])
        # self.addlabels(keys_list, values_list)
        plt.xticks(range(len(keys_list)), list(keys_list))
        # plt.ylim(3, 4.5)
        ax.set_xlabel("Variants")
        ax.set_ylabel("Rating")
        plt.title("MIL for groups with partial information")
        plt.savefig('plots/Loss_partial_box.png')
        # input("Yes")
        
        plt.clf()
        keys_list = ['','N', 'R', 'I', 'RI']
        values_list_N = []
        # values_list_N.extend(group_type_rating_dict['G1'])
        # values_list_N.extend(group_type_rating_dict['G5'])
        values_list_N.extend(group_type_rating_dict['G9'])
        values_list_R = []
        # values_list_R.extend(group_type_rating_dict['G2'])
        # values_list_R.extend(group_type_rating_dict['G6'])
        values_list_R.extend(group_type_rating_dict['G10'])
        values_list_I = []
        # values_list_I.extend(group_type_rating_dict['G3'])
        # values_list_I.extend(group_type_rating_dict['G7'])
        values_list_I.extend(group_type_rating_dict['G11'])
        values_list_RI = []
        # values_list_RI.extend(group_type_rating_dict['G4'])
        # values_list_RI.extend(group_type_rating_dict['G8'])
        values_list_RI.extend(group_type_rating_dict['G12'])
        fig, ax = plt.subplots()
        ax.boxplot([values_list_N,values_list_R,values_list_I,values_list_RI])
        # plt.box([values_list_N,values_list_R,values_list_I,values_list_RI])
        # self.addlabels(keys_list, values_list)
        plt.xticks(range(len(keys_list)), list(keys_list))
        # plt.ylim(3, 4.5)
        ax.set_xlabel("Variants")
        ax.set_ylabel("Rating")
        plt.title("MIL for groups with full information")
        plt.savefig('plots/Loss_full_box.png')
        # input("Yes")
        
        plt.clf()
        keys_list = ['N', 'R', 'I', 'RI']
        values_list = [(group_type_avr_rating_dict[x] + group_type_avr_rating_dict[y] + group_type_avr_rating_dict[z])/3 for x,y,z in zip(['G1', 'G2', 'G3', 'G4'],['G5', 'G6', 'G7', 'G8'],['G9', 'G10', 'G11', 'G12'])]
        print(values_list)
        plt.bar(keys_list, values_list, align='center')
        self.addlabels(keys_list, values_list)
        plt.xticks(range(len(values_list)), list(keys_list))
        plt.ylim(0, 2)
        plt.title("Mean Individual Loss")
        plt.savefig('plots/avr_individual_loss_all.png')
        
        plt.clf()
        keys_list = ['N', 'R', 'I', 'RI']
        values_list = [group_type_avr_rating_dict[x] for x in ['G1', 'G2', 'G3', 'G4']]
        plt.bar(keys_list, values_list, align='center')
        plt.xticks(range(len(values_list)), list(keys_list))
        plt.ylim(0, 2)
        self.addlabels(keys_list, values_list)
        plt.title("Mean Individual Loss for groups with No information")
        plt.savefig('plots/avr_individual_loss_l1.png')
        
        plt.clf()
        keys_list = ['N', 'R', 'I', 'RI']
        values_list = [group_type_avr_rating_dict[x] for x in ['G5', 'G6', 'G7', 'G8']]
        plt.bar(keys_list, values_list, align='center')
        plt.xticks(range(len(values_list)), list(['N', 'R', 'I', 'RI']))
        plt.ylim(0, 2)
        self.addlabels(keys_list, values_list)
        plt.title("Mean Individual Loss for groups with partial information")
        plt.savefig('plots/avr_individual_loss_l2.png')
        
        plt.clf()
        keys_list = ['N', 'R', 'I', 'RI']
        values_list = [group_type_avr_rating_dict[x] for x in ['G9', 'G10', 'G11', 'G12']]
        plt.bar(keys_list, values_list, align='center')
        plt.xticks(range(len(values_list)), list(['N', 'R', 'I', 'RI']))
        plt.ylim(0, 2)
        self.addlabels(keys_list, values_list)
        plt.title("Mean Individual Loss for groups with full information")
        plt.savefig('plots/avr_individual_loss_l3.png')
     
    def avr_individual_loss_size(self):
        plt.clf()
        group_type_rating_dict = {'G12':list(), 'G13':list(), 'G14':list(), 'G15':list(), 'G22':list(), 'G23':list(), 'G24':list(), 'G25':list(), 'G32':list(), 'G33':list(), 'G34':list(), 'G35':list(), 'G42':list(), 'G43':list(), 'G44':list(), 'G45':list(), 'G52':list(), 'G53':list(), 'G54':list(), 'G55':list(), 'G62':list(), 'G63':list(), 'G64':list(), 'G65':list(), 'G72':list(), 'G73':list(), 'G74':list(), 'G75':list(), 'G82':list(), 'G83':list(), 'G84':list(), 'G85':list(), 'G92':list(), 'G93':list(), 'G94':list(), 'G95':list(), 'G102':list(),  'G103':list(),  'G104':list(),  'G105':list(), 'G112':list(), 'G113':list(), 'G114':list(), 'G115':list(), 'G122':list(), 'G123':list(), 'G124':list(), 'G125':list()}
        df_groups_type = pd.read_csv("OutPuts/group_organizer_type.csv")
        df_individual_ratings = pd.read_csv("OutPuts/individual_ratings.csv")
        df_group_size = pd.read_csv("OutPuts/member_group_size.csv")
        for index, row in df_groups_type.iterrows():
            organizer = row['organizer']
            group_level_type = row['type']
            df_groups = pd.read_csv("OutPuts/groups_members.csv")
            df_groups.fillna(-1,inplace=True)
            for group_index, group_row in df_groups.iterrows():
                group_set = set([int(group_row['member1']), int(group_row['member2']), int(group_row['member3']), int(group_row['member4']), int(group_row['member5'])])
                if -1 in group_set:
                    group_set.remove(-1)
                organizer_choice = self.get_organizer_choice(organizer)
                if int(organizer) in group_set:
                    group_members_list = list(group_set)
                    group_size = df_group_size.loc[df_group_size["user_id"] == int(organizer), "size"].values
                    group_type = str(group_level_type) + str(group_size[0])
                    for member in group_members_list:
                        member_max_score = self.get_member_max_score(member)
                        for restaurant in organizer_choice:
                            df_temp = df_individual_ratings.loc[(df_individual_ratings['user'] == member) & (df_individual_ratings['restaurant'] == restaurant)]
                            new_list = group_type_rating_dict[group_type].extend([member_max_score - x for x in list(df_temp['rating'].values)])
                            if new_list != None:
                                group_type_rating_dict[group_type] = new_list
        group_type_avr_rating_dict = dict()
        for key in group_type_rating_dict.keys():
            if len(group_type_rating_dict[key]) > 0:
                group_type_avr_rating_dict[key] = np.average(group_type_rating_dict[key])
        
        width = 0.20
        ind = np.arange(12) 
        bar1 = plt.bar(ind, [group_type_avr_rating_dict["G12"], group_type_avr_rating_dict["G22"], group_type_avr_rating_dict["G32"], group_type_avr_rating_dict["G42"], group_type_avr_rating_dict["G52"], group_type_avr_rating_dict["G62"], group_type_avr_rating_dict["G72"], group_type_avr_rating_dict["G82"], group_type_avr_rating_dict["G92"], group_type_avr_rating_dict["G102"], group_type_avr_rating_dict["G112"], group_type_avr_rating_dict["G122"]], width, color = 'r')
        bar2 = plt.bar(ind+width, [group_type_avr_rating_dict["G13"], group_type_avr_rating_dict["G23"], group_type_avr_rating_dict["G33"], group_type_avr_rating_dict["G43"], group_type_avr_rating_dict["G53"], group_type_avr_rating_dict["G63"], group_type_avr_rating_dict["G73"], group_type_avr_rating_dict["G83"], group_type_avr_rating_dict["G93"], group_type_avr_rating_dict["G103"], group_type_avr_rating_dict["G113"], group_type_avr_rating_dict["G123"]], width, color = 'g')
        bar3 = plt.bar(ind+2*width, [group_type_avr_rating_dict["G14"], group_type_avr_rating_dict["G24"], group_type_avr_rating_dict["G34"], group_type_avr_rating_dict["G44"], group_type_avr_rating_dict["G54"], group_type_avr_rating_dict["G64"], group_type_avr_rating_dict["G74"], group_type_avr_rating_dict["G84"], group_type_avr_rating_dict["G94"], group_type_avr_rating_dict["G104"], group_type_avr_rating_dict["G114"], group_type_avr_rating_dict["G124"]], width, color = 'b')
        bar4 = plt.bar(ind+3*width, [group_type_avr_rating_dict["G15"], group_type_avr_rating_dict["G25"], group_type_avr_rating_dict["G35"], group_type_avr_rating_dict["G45"], group_type_avr_rating_dict["G55"], group_type_avr_rating_dict["G65"], group_type_avr_rating_dict["G75"], group_type_avr_rating_dict["G85"], group_type_avr_rating_dict["G95"], group_type_avr_rating_dict["G105"], group_type_avr_rating_dict["G115"], group_type_avr_rating_dict["G125"]], width, color = 'm')
        N = 3
        ind = np.arange(N) 
        plt.xlabel("Frequency")
        plt.ylabel('Group Types')
        plt.title("Group Type Frequence")
        plt.xticks(np.arange(12)+width,['G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9', 'G10', 'G11', 'G12'])
        plt.legend( (bar1, bar2, bar3, bar4), ('Size = 2', 'Size = 3', 'Size = 4', 'Size = 5') )
        plt.ylim(0, 3)
        plt.savefig('plots/avr_individual_loss_size.png')
        
        plt.clf()
        width = 0.20
        ind = np.arange(4) 
        bar1 = plt.bar(ind, [group_type_avr_rating_dict["G12"], group_type_avr_rating_dict["G22"], group_type_avr_rating_dict["G32"], group_type_avr_rating_dict["G42"]], width, color = 'r')
        bar2 = plt.bar(ind+width, [group_type_avr_rating_dict["G13"], group_type_avr_rating_dict["G23"], group_type_avr_rating_dict["G33"], group_type_avr_rating_dict["G43"]], width, color = 'g')
        bar3 = plt.bar(ind+2*width, [group_type_avr_rating_dict["G14"], group_type_avr_rating_dict["G24"], group_type_avr_rating_dict["G34"], group_type_avr_rating_dict["G44"]], width, color = 'b')
        bar4 = plt.bar(ind+3*width, [group_type_avr_rating_dict["G15"], group_type_avr_rating_dict["G25"], group_type_avr_rating_dict["G35"], group_type_avr_rating_dict["G45"]], width, color = 'm')
        N = 3
        ind = np.arange(N) 
        plt.xlabel("Frequency")
        plt.ylabel('Group Types')
        plt.title("Group Type Frequence")
        plt.xticks(np.arange(4)+width,['G1', 'G2', 'G3', 'G4'])
        plt.legend( (bar1, bar2, bar3, bar4), ('Size = 2', 'Size = 3', 'Size = 4', 'Size = 5') )
        plt.ylim(0, 3)
        plt.savefig('plots/avr_individual_loss_size_l1.png')
        
        plt.clf()
        width = 0.20
        ind = np.arange(4) 
        bar1 = plt.bar(ind, [group_type_avr_rating_dict["G52"], group_type_avr_rating_dict["G62"], group_type_avr_rating_dict["G72"], group_type_avr_rating_dict["G82"]], width, color = 'r')
        bar2 = plt.bar(ind+width, [group_type_avr_rating_dict["G53"], group_type_avr_rating_dict["G63"], group_type_avr_rating_dict["G73"], group_type_avr_rating_dict["G83"]], width, color = 'g')
        bar3 = plt.bar(ind+2*width, [group_type_avr_rating_dict["G54"], group_type_avr_rating_dict["G64"], group_type_avr_rating_dict["G74"], group_type_avr_rating_dict["G84"]], width, color = 'b')
        bar4 = plt.bar(ind+3*width, [group_type_avr_rating_dict["G55"], group_type_avr_rating_dict["G65"], group_type_avr_rating_dict["G75"], group_type_avr_rating_dict["G85"]], width, color = 'm')
        N = 3
        ind = np.arange(N) 
        plt.xlabel("Frequency")
        plt.ylabel('Group Types')
        plt.title("Group Type Frequence")
        plt.xticks(np.arange(4)+width,['G5', 'G6', 'G7', 'G8'])
        plt.legend( (bar1, bar2, bar3, bar4), ('Size = 2', 'Size = 3', 'Size = 4', 'Size = 5') )
        plt.ylim(0, 3)
        plt.savefig('plots/avr_individual_loss_size_l2.png')
        
        plt.clf()
        
        width = 0.20
        ind = np.arange(4) 
        bar1 = plt.bar(ind, [group_type_avr_rating_dict["G92"], group_type_avr_rating_dict["G102"], group_type_avr_rating_dict["G112"], group_type_avr_rating_dict["G122"]], width, color = 'r')
        bar2 = plt.bar(ind+width, [group_type_avr_rating_dict["G93"], group_type_avr_rating_dict["G103"], group_type_avr_rating_dict["G113"], group_type_avr_rating_dict["G123"]], width, color = 'g')
        bar3 = plt.bar(ind+2*width, [group_type_avr_rating_dict["G94"], group_type_avr_rating_dict["G104"], group_type_avr_rating_dict["G114"], group_type_avr_rating_dict["G124"]], width, color = 'b')
        bar4 = plt.bar(ind+3*width, [group_type_avr_rating_dict["G95"], group_type_avr_rating_dict["G105"], group_type_avr_rating_dict["G115"], group_type_avr_rating_dict["G125"]], width, color = 'm')
        N = 3
        ind = np.arange(N) 
        plt.xlabel("Frequency")
        plt.ylabel('Group Types')
        plt.title("Group Type Frequence")
        plt.xticks(np.arange(4)+width,['G9', 'G10', 'G11', 'G12'])
        plt.legend( (bar1, bar2, bar3, bar4), ('Size = 2', 'Size = 3', 'Size = 4', 'Size = 5') )
        plt.ylim(0, 3)
        plt.savefig('plots/avr_individual_loss_size_l3.png')
        
    def get_member_max_score(self, member):
        df_individual_ratings = pd.read_csv("OutPuts/individual_ratings.csv")
        rating_list = list(df_individual_ratings.loc[(df_individual_ratings['user'] == member), "rating"].values)
        if len(rating_list) > 0:
            return np.max(rating_list)
        else:
            return 0
    
    def item_fairness(self):
        plt.clf()
        group_type_rating_dict = {'G1':list(), 'G2':list(), 'G3':list(), 'G4':list(), 'G5':list(), 'G6':list(), 'G7':list(), 'G8':list(), 'G9':list(), 'G10':list(), 'G11':list(), 'G12':list()}
        df_groups_type = pd.read_csv("OutPuts/group_organizer_type.csv")
        df_individual_ratings = pd.read_csv("OutPuts/individual_ratings.csv")
        for index, row in df_groups_type.iterrows():
            organizer = row['organizer']
            group_type = row['type']
            df_groups = pd.read_csv("OutPuts/groups_members.csv")
            df_groups.fillna(-1,inplace=True)
            for group_index, group_row in df_groups.iterrows():
                group_set = set([int(group_row['member1']), int(group_row['member2']), int(group_row['member3']), int(group_row['member4']), int(group_row['member5'])])
                if -1 in group_set:
                    group_set.remove(-1)
                organizer_choice = self.get_organizer_choice(organizer)
                if int(organizer) in group_set:
                    group_members_list = list(group_set)
                    for restaurant in organizer_choice:
                        group_restaurant_rating_list = list()
                        for member in group_members_list:
                            df_temp = df_individual_ratings.loc[(df_individual_ratings['user'] == member) & (df_individual_ratings['restaurant'] == restaurant), "rating"]
                            if len(list(df_temp.values)) > 0:
                                group_restaurant_rating_list.append(np.mean(list(df_temp.values)))
                        if group_restaurant_rating_list != None and len(group_restaurant_rating_list) > 0:
                            group_type_rating_dict[group_type].append(np.var(group_restaurant_rating_list))
        group_type_avr_rating_dict = dict()
        for key in group_type_rating_dict.keys():
            if len(group_type_rating_dict[key]) > 0:
                group_type_avr_rating_dict[key] = np.average(group_type_rating_dict[key])
        plt.bar(list(group_type_avr_rating_dict.keys()), list(group_type_avr_rating_dict.values()), align='center')
        plt.xticks(range(len(group_type_avr_rating_dict)), list(group_type_avr_rating_dict.keys()))
        plt.savefig('plots/avr_fairness.png')
        
        plt.clf()
        keys_list = ['G1', 'G2', 'G3', 'G4']
        values_list = [group_type_avr_rating_dict[x] for x in ['G1', 'G2', 'G3', 'G4']]
        plt.bar(keys_list, values_list, align='center')
        plt.xticks(range(len(values_list)), list(keys_list))
        plt.ylim(0, 2)
        plt.savefig('plots/avr_fairness_l1.png')
        
        plt.clf()
        keys_list = ['G5', 'G6', 'G7', 'G8']
        values_list = [group_type_avr_rating_dict[x] for x in keys_list]
        plt.bar(keys_list, values_list, align='center')
        plt.xticks(range(len(values_list)), list(keys_list))
        plt.ylim(0, 2)
        plt.savefig('plots/avr_fairness_l2.png')
        
        plt.clf()
        keys_list = ['G9', 'G10', 'G11', 'G12']
        values_list = [group_type_avr_rating_dict[x] for x in keys_list]
        plt.bar(keys_list, values_list, align='center')
        plt.xticks(range(len(values_list)), list(keys_list))
        plt.ylim(0, 2)
        plt.savefig('plots/avr_fairness_l3.png')
        
        plt.clf()
        keys_list = ['N', 'R', 'I', 'RI']
        values_list = [(group_type_avr_rating_dict[x] + group_type_avr_rating_dict[y] + group_type_avr_rating_dict[z])/3 for x,y,z in zip(['G1', 'G2', 'G3', 'G4'],['G5', 'G6', 'G7', 'G8'],['G9', 'G10', 'G11', 'G12'])]
        plt.bar(keys_list, values_list, align='center')
        self.addlabels(keys_list, values_list)
        plt.xticks(range(len(values_list)), list(keys_list))
        plt.ylim(0, 0.8)
        plt.title("Average rating for final choices")
        plt.savefig('plots/avr_fair_all.png')
    
    def item_fairness_size(self):
        plt.clf()
        group_type_rating_dict = {'G12':list(), 'G13':list(), 'G14':list(), 'G15':list(), 'G22':list(), 'G23':list(), 'G24':list(), 'G25':list(), 'G32':list(), 'G33':list(), 'G34':list(), 'G35':list(), 'G42':list(), 'G43':list(), 'G44':list(), 'G45':list(), 'G52':list(), 'G53':list(), 'G54':list(), 'G55':list(), 'G62':list(), 'G63':list(), 'G64':list(), 'G65':list(), 'G72':list(), 'G73':list(), 'G74':list(), 'G75':list(), 'G82':list(), 'G83':list(), 'G84':list(), 'G85':list(), 'G92':list(), 'G93':list(), 'G94':list(), 'G95':list(), 'G102':list(),  'G103':list(),  'G104':list(),  'G105':list(), 'G112':list(), 'G113':list(), 'G114':list(), 'G115':list(), 'G122':list(), 'G123':list(), 'G124':list(), 'G125':list()}
        df_groups_type = pd.read_csv("OutPuts/group_organizer_type.csv")
        df_individual_ratings = pd.read_csv("OutPuts/individual_ratings.csv")
        df_group_size = pd.read_csv("OutPuts/member_group_size.csv")
        for index, row in df_groups_type.iterrows():
            organizer = row['organizer']
            group_level_type = row['type']
            df_groups = pd.read_csv("OutPuts/groups_members.csv")
            df_groups.fillna(-1,inplace=True)
            for group_index, group_row in df_groups.iterrows():
                group_set = set([int(group_row['member1']), int(group_row['member2']), int(group_row['member3']), int(group_row['member4']), int(group_row['member5'])])
                if -1 in group_set:
                    group_set.remove(-1)
                organizer_choice = self.get_organizer_choice(organizer)
                if int(organizer) in group_set:
                    group_members_list = list(group_set)
                    group_size = df_group_size.loc[df_group_size["user_id"] == int(organizer), "size"].values
                    group_type = str(group_level_type) + str(group_size[0])
                    # if (group_type == 'G112'):
                    #     print("Next Group")
                    #     print(organizer)
                    for restaurant in organizer_choice:
                        group_restaurant_rating_list = list()
                        for member in group_members_list:
                            df_temp = df_individual_ratings.loc[(df_individual_ratings['user'] == member) & (df_individual_ratings['restaurant'] == restaurant), "rating"]
                            if len(list(df_temp.values)) > 0:
                                group_restaurant_rating_list.append(np.mean(list(df_temp.values)))
                        # if (group_type == 'G112'):
                        #     print("Scoring List")
                        #     print(group_restaurant_rating_list)
                        if group_restaurant_rating_list != None and len(group_restaurant_rating_list) > 0:
                            group_type_rating_dict[group_type].append(np.var(group_restaurant_rating_list))
                            # if (group_type == 'G112'):
                            #     print("Variance List")
                            #     print(group_type_rating_dict[group_type])
        group_type_avr_rating_dict = dict()
        for key in group_type_rating_dict.keys():
            if len(group_type_rating_dict[key]) > 0:
                group_type_avr_rating_dict[key] = np.average(group_type_rating_dict[key])
        width = 0.20
        ind = np.arange(12) 
        bar1 = plt.bar(ind, [group_type_avr_rating_dict["G12"], group_type_avr_rating_dict["G22"], group_type_avr_rating_dict["G32"], group_type_avr_rating_dict["G42"], group_type_avr_rating_dict["G52"], group_type_avr_rating_dict["G62"], group_type_avr_rating_dict["G72"], group_type_avr_rating_dict["G82"], group_type_avr_rating_dict["G92"], group_type_avr_rating_dict["G102"], group_type_avr_rating_dict["G112"], group_type_avr_rating_dict["G122"]], width, color = 'r')
        bar2 = plt.bar(ind+width, [group_type_avr_rating_dict["G13"], group_type_avr_rating_dict["G23"], group_type_avr_rating_dict["G33"], group_type_avr_rating_dict["G43"], group_type_avr_rating_dict["G53"], group_type_avr_rating_dict["G63"], group_type_avr_rating_dict["G73"], group_type_avr_rating_dict["G83"], group_type_avr_rating_dict["G93"], group_type_avr_rating_dict["G103"], group_type_avr_rating_dict["G113"], group_type_avr_rating_dict["G123"]], width, color = 'g')
        bar3 = plt.bar(ind+2*width, [group_type_avr_rating_dict["G14"], group_type_avr_rating_dict["G24"], group_type_avr_rating_dict["G34"], group_type_avr_rating_dict["G44"], group_type_avr_rating_dict["G54"], group_type_avr_rating_dict["G64"], group_type_avr_rating_dict["G74"], group_type_avr_rating_dict["G84"], group_type_avr_rating_dict["G94"], group_type_avr_rating_dict["G104"], group_type_avr_rating_dict["G114"], group_type_avr_rating_dict["G124"]], width, color = 'b')
        bar4 = plt.bar(ind+3*width, [group_type_avr_rating_dict["G15"], group_type_avr_rating_dict["G25"], group_type_avr_rating_dict["G35"], group_type_avr_rating_dict["G45"], group_type_avr_rating_dict["G55"], group_type_avr_rating_dict["G65"], group_type_avr_rating_dict["G75"], group_type_avr_rating_dict["G85"], group_type_avr_rating_dict["G95"], group_type_avr_rating_dict["G105"], group_type_avr_rating_dict["G115"], group_type_avr_rating_dict["G125"]], width, color = 'm')
        N = 3
        ind = np.arange(N) 
        plt.xlabel("Frequency")
        plt.ylabel('Group Types')
        plt.title("Group Type Frequence")
        plt.xticks(np.arange(12)+width,['G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9', 'G10', 'G11', 'G12'])
        plt.legend( (bar1, bar2, bar3, bar4), ('Size = 2', 'Size = 3', 'Size = 4', 'Size = 5') )
        plt.ylim(0, 3)
        plt.savefig('plots/avr_fairness_size.png')
        
        plt.clf()
        width = 0.20
        ind = np.arange(4) 
        bar1 = plt.bar(ind, [group_type_avr_rating_dict["G12"], group_type_avr_rating_dict["G22"], group_type_avr_rating_dict["G32"], group_type_avr_rating_dict["G42"]], width, color = 'r')
        bar2 = plt.bar(ind+width, [group_type_avr_rating_dict["G13"], group_type_avr_rating_dict["G23"], group_type_avr_rating_dict["G33"], group_type_avr_rating_dict["G43"]], width, color = 'g')
        bar3 = plt.bar(ind+2*width, [group_type_avr_rating_dict["G14"], group_type_avr_rating_dict["G24"], group_type_avr_rating_dict["G34"], group_type_avr_rating_dict["G44"]], width, color = 'b')
        bar4 = plt.bar(ind+3*width, [group_type_avr_rating_dict["G15"], group_type_avr_rating_dict["G25"], group_type_avr_rating_dict["G35"], group_type_avr_rating_dict["G45"]], width, color = 'm')
        N = 3
        ind = np.arange(N) 
        plt.xlabel("Frequency")
        plt.ylabel('Group Types')
        plt.title("Group Type Frequence")
        plt.xticks(np.arange(4)+width,['G1', 'G2', 'G3', 'G4'])
        plt.legend( (bar1, bar2, bar3, bar4), ('Size = 2', 'Size = 3', 'Size = 4', 'Size = 5') )
        plt.ylim(0, 3)
        plt.savefig('plots/avr_fairness_size_l1.png')
        
        plt.clf()
        width = 0.20
        ind = np.arange(4) 
        bar1 = plt.bar(ind, [group_type_avr_rating_dict["G52"], group_type_avr_rating_dict["G62"], group_type_avr_rating_dict["G72"], group_type_avr_rating_dict["G82"]], width, color = 'r')
        bar2 = plt.bar(ind+width, [group_type_avr_rating_dict["G53"], group_type_avr_rating_dict["G63"], group_type_avr_rating_dict["G73"], group_type_avr_rating_dict["G83"]], width, color = 'g')
        bar3 = plt.bar(ind+2*width, [group_type_avr_rating_dict["G54"], group_type_avr_rating_dict["G64"], group_type_avr_rating_dict["G74"], group_type_avr_rating_dict["G84"]], width, color = 'b')
        bar4 = plt.bar(ind+3*width, [group_type_avr_rating_dict["G55"], group_type_avr_rating_dict["G65"], group_type_avr_rating_dict["G75"], group_type_avr_rating_dict["G85"]], width, color = 'm')
        N = 3
        ind = np.arange(N) 
        plt.xlabel("Frequency")
        plt.ylabel('Group Types')
        plt.title("Group Type Frequence")
        plt.xticks(np.arange(4)+width,['G5', 'G6', 'G7', 'G8'])
        plt.legend( (bar1, bar2, bar3, bar4), ('Size = 2', 'Size = 3', 'Size = 4', 'Size = 5') )
        plt.ylim(0, 3)
        plt.savefig('plots/avr_fairness_size_l2.png')
        
        plt.clf()
        
        width = 0.20
        ind = np.arange(4) 
        bar1 = plt.bar(ind, [group_type_avr_rating_dict["G92"], group_type_avr_rating_dict["G102"], group_type_avr_rating_dict["G112"], group_type_avr_rating_dict["G122"]], width, color = 'r')
        bar2 = plt.bar(ind+width, [group_type_avr_rating_dict["G93"], group_type_avr_rating_dict["G103"], group_type_avr_rating_dict["G113"], group_type_avr_rating_dict["G123"]], width, color = 'g')
        bar3 = plt.bar(ind+2*width, [group_type_avr_rating_dict["G94"], group_type_avr_rating_dict["G104"], group_type_avr_rating_dict["G114"], group_type_avr_rating_dict["G124"]], width, color = 'b')
        bar4 = plt.bar(ind+3*width, [group_type_avr_rating_dict["G95"], group_type_avr_rating_dict["G105"], group_type_avr_rating_dict["G115"], group_type_avr_rating_dict["G125"]], width, color = 'm')
        N = 3
        ind = np.arange(N) 
        plt.xlabel("Frequency")
        plt.ylabel('Group Types')
        plt.title("Group Type Frequence")
        plt.xticks(np.arange(4)+width,['G9', 'G10', 'G11', 'G12'])
        plt.legend( (bar1, bar2, bar3, bar4), ('Size = 2', 'Size = 3', 'Size = 4', 'Size = 5') )
        plt.ylim(0, 3)
        plt.savefig('plots/avr_fairness_size_l3.png')
    
    def sus_score(self):
        query = "SELECT q1,q2,q3,q4,q5,q6,q7,q8,q9,q10 FROM sus WHERE id > 64"
        my_cursor = self.mysql_conn.cursor(buffered=True)
        my_cursor.execute(query)
        scores_list = []
        questionnaire_scores = np.zeros(10)
        for scores in my_cursor:
            scores_list.append((((scores[0] + 1) - 1) + ((scores[2] + 1) - 1 ) + ((scores[4] + 1) - 1) + ((scores[6] + 1) - 1) + ((scores[8] + 1) - 1) + (5 - (scores[1] + 1)) + (5 - (scores[3] + 1)) + (5 - (scores[5] + 1)) + (5 - (scores[7] + 1)) + (5 - (scores[9] + 1))) * 2.5) 
            questionnaire_scores += (((scores[0] + 1) - 1), ((scores[2] + 1) - 1 ), ((scores[4] + 1) - 1), ((scores[6] + 1) - 1), ((scores[8] + 1) - 1), (5 - (scores[1] + 1)), (5 - (scores[3] + 1)), (5 - (scores[5] + 1)), (5 - (scores[7] + 1)), (5 - (scores[9] + 1)))
        
        bins = np.arange(np.min(scores_list) - 1, np.max(scores_list) + 1, 1) # fixed bin size

        plt.xlim([min(scores_list)-1, max(scores_list)+1])

        plt.hist(scores_list, bins=bins)
        plt.xticks(np.arange(np.min(scores_list) - 1, np.max(scores_list) + 1, 3))
        plt.title('SUS scores distribution')
        plt.xlabel('Scores')
        plt.ylabel('Number of users')

        plt.savefig('plots/sus_histogram.png')
        print(scores_list)
        print(np.std(scores_list))
        print(np.mean(scores_list))
        print(questionnaire_scores/19)
    
    def significance_test_MIL(self):
        group_type_rating_dict = {'G1':list(), 'G2':list(), 'G3':list(), 'G4':list(), 'G5':list(), 'G6':list(), 'G7':list(), 'G8':list(), 'G9':list(), 'G10':list(), 'G11':list(), 'G12':list()}
        df_groups_type = pd.read_csv("OutPuts/group_organizer_type.csv")
        df_group_ratings = pd.read_csv("OutPuts/group_ratings.csv")
        for index, row in df_groups_type.iterrows():
            organizer = row['organizer']
            group_type = row['type']
            df_groups = pd.read_csv("OutPuts/groups_members.csv")
            df_groups.fillna(-1,inplace=True)
            for group_index, group_row in df_groups.iterrows():
                group_set = set([int(group_row['member1']), int(group_row['member2']), int(group_row['member3']), int(group_row['member4']), int(group_row['member5'])])
                if -1 in group_set:
                    group_set.remove(-1)
                organizer_choice = self.get_organizer_choice(organizer)
                if int(organizer) in group_set:
                    group_members_list = list(group_set)
                    for member in group_members_list:
                        for restaurant in organizer_choice:
                            df_temp = df_group_ratings.loc[(df_group_ratings['user'] == member) & (df_group_ratings['restaurant'] == restaurant)]
                            new_list = group_type_rating_dict[group_type].extend(list(df_temp['rating'].values))
                            if new_list != None:
                                group_type_rating_dict[group_type] = new_list
        group_type_avr_rating_dict = dict()
        for key in group_type_rating_dict.keys():
            if len(group_type_rating_dict[key]) > 0:
                group_type_avr_rating_dict[key] = np.average(group_type_rating_dict[key])
                
        list_name = ['N', 'R', 'I', 'RI']
        list_total_N = []
        list_total_N.append(group_type_rating_dict['G1'])
        list_total_N.append(group_type_rating_dict['G5'])
        list_total_N.append(group_type_rating_dict['G9'])
        
        list_total_R = []
        list_total_R.append(group_type_rating_dict['G2'])
        list_total_R.append(group_type_rating_dict['G6'])
        list_total_R.append(group_type_rating_dict['G10'])
        
        list_total_I = []
        list_total_I.append(group_type_rating_dict['G3'])
        list_total_I.append(group_type_rating_dict['G7'])
        list_total_I.append(group_type_rating_dict['G11'])
        
        list_total_RI = []
        list_total_RI.append(group_type_rating_dict['G4'])
        list_total_RI.append(group_type_rating_dict['G8'])
        list_total_RI.append(group_type_rating_dict['G12'])
        
        system_list = [list_total_N,list_total_R,list_total_I,list_total_RI]
        
        def extending_list(input_list):       
            flat_list = []
            for sublist in input_list:
                for item in sublist:
                    flat_list.append(item)
            return flat_list
        
        print("ANOVA")
        print(stats.f_oneway(extending_list(list_total_N),extending_list(list_total_R),extending_list(list_total_I),extending_list(list_total_RI)))
        input()
        
        for system1, name1 in zip(system_list, list_name):
            for system2, name2 in zip(system_list, list_name):
                if (name1 != name2):
                    print(name1, name2)
                    print(stats.mannwhitneyu(extending_list(system1), extending_list(system2)))
                    print('*********************')
        
        for name1, system1 in group_type_rating_dict.items():
            for name2,system2 in group_type_rating_dict.items():
                if (name1 != name2):
                    print(name1, name2)
                    print(stats.mannwhitneyu((system1), (system2)))
                    print('*********************')
                    
        
        
                    
                    
        # for system1 in keys_list:
        #     for system2 in keys_list.remove(system1):
        #         print(stats.wilcoxon(list1, list2))
        
        # plt.clf()
        # keys_list = ['N', 'R', 'I', 'RI']
        # values_list = [group_type_avr_rating_dict[x] for x in ['G1', 'G2', 'G3', 'G4']]
        # plt.bar(keys_list, values_list, align='center')
        # self.addlabels(keys_list, values_list)
        # plt.xticks(range(len(values_list)), list(keys_list))
        # plt.ylim(3, 4.5)
        # plt.title("Average rating for groups with no information")
        # plt.savefig('plots/group_type_average_l1.png')
        
        # plt.clf()
        # keys_list = ['N', 'R', 'I', 'RI']
        # values_list = [group_type_avr_rating_dict[x] for x in ['G5', 'G6', 'G7', 'G8']]
        # plt.bar(keys_list, values_list, align='center')
        # self.addlabels(keys_list, values_list)
        # plt.xticks(range(len(values_list)), list(keys_list))
        # plt.ylim(3, 4.5)
        # plt.title("Average rating for groups with partial information")
        # plt.savefig('plots/group_type_average_l2.png')
        
        # plt.clf()
        # keys_list = ['N', 'R', 'I', 'RI']
        # values_list = [group_type_avr_rating_dict[x] for x in ['G9', 'G10', 'G11', 'G12']]
        # plt.bar(keys_list, values_list, align='center')
        # self.addlabels(keys_list, values_list)
        # plt.xticks(range(len(values_list)), list(keys_list))
        # plt.ylim(3, 4.5)
        # plt.title("Average rating for groups with full information")
        # plt.savefig('plots/group_type_average_l3.png')
        # print(stats.wilcoxon(list1, list2))
    
    # def rating_distribution(self):
    #     pass
    
    def box_plot_loss(self):
        plt.clf()
        df = pd.read_csv("OutPuts/df_individual_loss.csv")
        l1_No = df.loc[(df['group_type'] == 1) & (df['system_type'] == 'No')]["rating"].values
        l2_No = df.loc[(df['group_type'] == 2) & (df['system_type'] == 'No')]["rating"].values
        l3_No = df.loc[(df['group_type'] == 3) & (df['system_type'] == 'No')]["rating"].values
        l1_R = df.loc[(df['group_type'] == 1) & (df['system_type'] == 'R')]["rating"].values
        l2_R = df.loc[(df['group_type'] == 2) & (df['system_type'] == 'R')]["rating"].values
        l3_R = df.loc[(df['group_type'] == 3) & (df['system_type'] == 'R')]["rating"].values
        l1_I = df.loc[(df['group_type'] == 1) & (df['system_type'] == 'I')]["rating"].values
        l2_I = df.loc[(df['group_type'] == 2) & (df['system_type'] == 'I')]["rating"].values
        l3_I = df.loc[(df['group_type'] == 3) & (df['system_type'] == 'I')]["rating"].values
        l1_RI = df.loc[(df['group_type'] == 1) & (df['system_type'] == 'RI')]["rating"].values
        l2_RI = df.loc[(df['group_type'] == 2) & (df['system_type'] == 'RI')]["rating"].values
        l3_RI = df.loc[(df['group_type'] == 3) & (df['system_type'] == 'RI')]["rating"].values
        li_list = [l1_No, l1_R, l1_I, l1_RI]
        l2_list = [l2_No, l2_R, l2_I, l2_RI]
        l3_list = [l3_No, l3_R, l3_I, l3_RI]
        ticks = ['N', 'R', 'I', 'RI']
        
        l1_plot = plt.boxplot(li_list,
                                    positions=np.array(
            np.arange(len(li_list)))*4.0-0.8,
                                    widths=0.4)
        l2_plot = plt.boxplot(l2_list,
                                    positions=np.array(
            np.arange(len(l2_list)))*4.0-0.2,
                                    widths=0.4)
        l3_plot = plt.boxplot(l3_list,
                                    positions=np.array(
            np.arange(len(l3_list)))*4.0+0.4,
                                    widths=0.4)
        
      
        def define_box_properties(plot_name, color_code, label):
            for k, v in plot_name.items():
                plt.setp(plot_name.get(k), color=color_code)
                
            plt.plot([], c=color_code, label=label)
            plt.legend()
        
        
        define_box_properties(l1_plot, 'red', 'No')
        define_box_properties(l2_plot, 'purple', 'Partial')
        define_box_properties(l3_plot, 'blue', 'Full')
        
        plt.xticks(np.arange(0, len(ticks) * 4, 4), ticks)
        
        plt.xlim(-2, len(ticks)*4)
        
        plt.ylim(-0.1, 4.2)
        
        plt.title('Box plot for MIL')
        plt.savefig('plots/loss_box.png')
    
    def box_plot_avr(self):
        plt.clf()
        df = pd.read_csv("OutPuts/df_groups_ratings.csv")
        l1_No = df.loc[(df['group_type'] == 1) & (df['system_type'] == 'No')]["rating"].values
        l2_No = df.loc[(df['group_type'] == 2) & (df['system_type'] == 'No')]["rating"].values
        l3_No = df.loc[(df['group_type'] == 3) & (df['system_type'] == 'No')]["rating"].values
        l1_R = df.loc[(df['group_type'] == 1) & (df['system_type'] == 'R')]["rating"].values
        l2_R = df.loc[(df['group_type'] == 2) & (df['system_type'] == 'R')]["rating"].values
        l3_R = df.loc[(df['group_type'] == 3) & (df['system_type'] == 'R')]["rating"].values
        l1_I = df.loc[(df['group_type'] == 1) & (df['system_type'] == 'I')]["rating"].values
        l2_I = df.loc[(df['group_type'] == 2) & (df['system_type'] == 'I')]["rating"].values
        l3_I = df.loc[(df['group_type'] == 3) & (df['system_type'] == 'I')]["rating"].values
        l1_RI = df.loc[(df['group_type'] == 1) & (df['system_type'] == 'RI')]["rating"].values
        l2_RI = df.loc[(df['group_type'] == 2) & (df['system_type'] == 'RI')]["rating"].values
        l3_RI = df.loc[(df['group_type'] == 3) & (df['system_type'] == 'RI')]["rating"].values
        li_list = [l1_No, l1_R, l1_I, l1_RI]
        l2_list = [l2_No, l2_R, l2_I, l2_RI]
        l3_list = [l3_No, l3_R, l3_I, l3_RI]
        ticks = ['N', 'R', 'I', 'RI']
        
        l1_plot = plt.boxplot(li_list,
                                    positions=np.array(
            np.arange(len(li_list)))*4.0-0.8,
                                    widths=0.4)
        l2_plot = plt.boxplot(l2_list,
                                    positions=np.array(
            np.arange(len(l2_list)))*4.0-0.2,
                                    widths=0.4)
        l3_plot = plt.boxplot(l3_list,
                                    positions=np.array(
            np.arange(len(l3_list)))*4.0+0.4,
                                    widths=0.4)
        
      
        def define_box_properties(plot_name, color_code, label):
            for k, v in plot_name.items():
                plt.setp(plot_name.get(k), color=color_code)
                
            plt.plot([], c=color_code, label=label)
            plt.legend()
        
        
        define_box_properties(l1_plot, 'red', 'No')
        define_box_properties(l2_plot, 'purple', 'Partial')
        define_box_properties(l3_plot, 'blue', 'Full')
        
        plt.xticks(np.arange(0, len(ticks) * 4, 4), ticks)
        
        plt.xlim(-2, len(ticks)*4)
        
        plt.ylim(0.5, 5.5)
        
        plt.title("Box plot for given ratings for organizers' choices")
        plt.savefig('plots/avr_box.png')
                    
                
                            