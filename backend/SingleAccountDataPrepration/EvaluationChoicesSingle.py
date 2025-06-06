from array import array
import csv
from typing import get_type_hints
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import scipy.stats as stats
import pandas as pd
from SingleAccountDataPrepration.EvaluationPreprationSingle import DataPreprationSingle
from scipy.stats import mannwhitneyu
from scipy.stats import wilcoxon
from scipy.stats import f_oneway
       
class DataEvaluationSingle(object):
    def __init__(self,connection_mysql):
        self.mysql_conn = connection_mysql
        self.first_account_organizers = DataPreprationSingle(self.mysql_conn).get_first_account_id()
        self.all_participant_set = DataPreprationSingle(self.mysql_conn).get_all_users_for_first_accounts()
              
    def get_number_of_accounts_first_stage(self):
        query = "SELECT user_id,personal_info,decision_making,post_rating FROM progress"
        my_cursor = self.mysql_conn.cursor(buffered=True)
        my_cursor.execute(query)
        counter_personal_info = 0
        counter_decision_making = 0
        counter_post_rating = 0
        for user in my_cursor:
            if user[0] in self.first_account_organizers and (14912 >= user[0] >= 14639  or 20798 >= user[0] >= 20734):
            # if user[0] in self.all_participant_set and (14912 >= user[0] >= 14639  or 20798 >= user[0] >= 20734):
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
            if user[0] in self.first_account_organizers and (14912 >= user[0] >= 14639  or 20798 >= user[0] >= 20734):
            # if user[0] in self.all_participant_set and (14912 >= user[0] >= 14639  or 20798 >= user[0] >= 20734):
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
        Revised_df_list = pd.read_csv("OutPuts/Selected_first.csv")['user_id'].unique()
        tripScore = {1: 4,2: 4.5,3: 4,4: 4,5: 4,6: 4,7: 4.5,8: 3.5,9: 3,10: 4.5,11: 4.5,12: 4.5,13: 4.5,15: 4.5,16: 4.5,17: 4,18: 5,19: 4,20: 4,21: 2,22: 4.5,23: 4,24: 4.5,25: 4,26: 4.5,27: 3.5,28: 4.5,29: 3.5,30: 5,31: 4.5,32: 5}
        price = {18:1, 30:1, 2:2, 31: 1, 25:2, 23:2, 19:2, 20:2, 1:1, 27:0, 8:0, 9:0, 21:0, 17:1, 3:0, 26:1, 24:0, 11:2, 4: 0, 12:2, 32:2, 6:0, 7:1, 16:1, 10: 1, 13:0, 15:0, 28:2, 22: 2, 5:0, 29:0}
        diversity = { 18:6, 30:5, 2: 6, 31: 3, 25:5, 23:5, 19:7, 20:5, 1:4, 27:8, 8:7, 9:7, 21:4, 17:7, 3:6, 26:6, 24:6, 11:6, 4: 5, 12:5, 32:5, 6:5, 7:4, 16:4,  10: 4, 13:1, 15:1, 28:1, 22:7, 5:8, 29:10}
        pop = {18:4, 30:2, 2: 1, 31:1, 25:2, 23:1, 19:0, 20:2, 1:1, 27:1, 8:1, 9:1, 21:1, 17:1, 3:1, 26:1, 24:1, 11:1, 4: 2, 12:0, 32:2, 6:1, 7:1, 16:1, 10:1, 13:1, 15:1, 28:1, 22:2, 5:4, 29:5}
        df = pd.DataFrame(columns=["user_id", "organizer_id", "group_type", "system_type", "rest_id", "rating", "rest_trip_score", "price", "diversity", "popularity", "fitness", "sim"])
        plt.clf()
        group_type_rating_dict = {'G1':list(), 'G2':list(), 'G3':list(), 'G4':list(), 'G5':list(), 'G6':list(), 'G7':list(), 'G8':list(), 'G9':list(), 'G10':list(), 'G11':list(), 'G12':list()}
        # df_groups_type = pd.read_csv("OutPuts/group_organizer_type_single.csv").drop_duplicates(subset=['organizer'])
        df_groups_type = pd.read_csv("OutPuts/group_organizer_type_single.csv").drop_duplicates(subset=['organizer'])
        # df_group_ratings = pd.read_csv("OutPuts/group_ratings_single.csv")
        df_group_ratings = pd.read_csv("OutPuts/Revised/group_ratings_single.csv")
        # df_organizer_booked = pd.read_csv("OutPuts/organizer_booked_cleaned.csv")
        df_organizer_booked = pd.read_csv("OutPuts/organizer_booked_cleaned.csv")
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
                if int(organizer) in group_set and int(organizer) in Revised_df_list:
                    group_members_list = list(group_set)
                    for member in group_members_list:
                        for restaurant in organizer_choice:
                            df_temp = df_group_ratings.loc[(df_group_ratings['user'] == member) & (df_group_ratings['restaurant'] == restaurant)]
                            new_list = group_type_rating_dict[group_type].extend(list(df_temp['rating'].values))
                            for rating in list(df_temp['rating'].values):
                                df = df.append(pd.DataFrame([[member,organizer,group_only_type,system_type,restaurant,rating, tripScore[restaurant], price[restaurant], diversity[restaurant], pop[restaurant], df_organizer_booked.loc[(df_organizer_booked['user_id'] == organizer) & (df_organizer_booked['rest_id'] == restaurant)].drop_duplicates()["fit_score"].values[0], df_organizer_booked.loc[(df_organizer_booked['user_id'] == organizer) & (df_organizer_booked['rest_id'] == restaurant)].drop_duplicates()["sim_score"].values[0]]], columns=["user_id", "organizer_id", "group_type", "system_type", "rest_id", "rating", "rest_trip_score", "price", "diversity", "popularity", "fitness", "sim"]))
                            if new_list != None:
                                group_type_rating_dict[group_type] = new_list
        group_type_avr_rating_dict = dict()
        group_type_avr_rating_dict_size = dict()
        # x = new_group_type_rating_dict["GNL"]
        # y = new_group_type_rating_dict["GRIL"]
        # res = mannwhitneyu(x, y)
        # print(res)
        GN = []
        GN.extend(group_type_rating_dict['G1'])
        GN.extend(group_type_rating_dict['G5'])
        GN.extend(group_type_rating_dict['G9'])
        GR = []
        GR.extend(group_type_rating_dict['G2'])
        GR.extend(group_type_rating_dict['G6'])
        GR.extend(group_type_rating_dict['G10'])
        GI = []
        GI.extend(group_type_rating_dict['G3'])
        GI.extend(group_type_rating_dict['G7'])
        GI.extend(group_type_rating_dict['G11'])
        GRI = []
        GRI.extend(group_type_rating_dict['G4'])
        GRI.extend(group_type_rating_dict['G8'])
        GRI.extend(group_type_rating_dict['G12'])
        # res = f_oneway(GN,GR,GI,GRI)
        # print(res)
        # input()
        
        GN = []
        # GN.extend(group_type_rating_dict['G1'])
        # GN.extend(group_type_rating_dict['G5'])
        GN.extend(group_type_rating_dict['G9'])
        GR = []
        # GR.extend(group_type_rating_dict['G2'])
        # GR.extend(group_type_rating_dict['G6'])
        GR.extend(group_type_rating_dict['G10'])
        GI = []
        # GI.extend(group_type_rating_dict['G3'])
        # GI.extend(group_type_rating_dict['G7'])
        GI.extend(group_type_rating_dict['G11'])
        GRI = []
        # GRI.extend(group_type_rating_dict['G4'])
        # GRI.extend(group_type_rating_dict['G8'])
        GRI.extend(group_type_rating_dict['G12'])
        res = f_oneway(GN,GR,GI,GRI)
        print(res)
        print(mannwhitneyu(GN,GRI))
        input("Level")
        for key in group_type_rating_dict.keys():
            if len(group_type_rating_dict[key]) > 0:
                group_type_avr_rating_dict[key] = np.average(group_type_rating_dict[key])
                group_type_avr_rating_dict_size[key] = len(group_type_rating_dict[key])
        df.drop_duplicates(subset=["user_id","organizer_id"],inplace=True)
        # df.to_csv("OutPuts/df_groups_ratings_with_trip_score_single.csv")
        df.to_csv("OutPuts/Revised/df_groups_ratings_with_trip_score_single.csv")
        plt.bar(list(group_type_avr_rating_dict.keys()), list(group_type_avr_rating_dict.values()), align='center')
        plt.xticks(range(len(group_type_avr_rating_dict)), list(group_type_avr_rating_dict.keys()))
        plt.ylim(3, 5)
        # plt.savefig('plots/Single/group_type_average_single.png')
        plt.savefig('plots/Single/Revised/group_type_average_single.png')
        
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
        # plt.savefig('plots/Single/group_type_average_all_box_single.png')
        plt.savefig('plots/Single/Revised/group_type_average_all_box_single.png')
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
        # plt.savefig('plots/Single/group_type_average_No_box_single.png')
        plt.savefig('plots/Single/Revised/group_type_average_No_box_single.png')
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
        # plt.savefig('plots/Single/group_type_average_partial_box_single.png')
        plt.savefig('plots/Single/Revised/group_type_average_partial_box_single.png')
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
        # plt.savefig('plots/Single/group_type_average_full_box_single.png')
        plt.savefig('plots/Single/Revised/group_type_average_full_box_single.png')
        # input("Yes")
        
        
        
        plt.clf()
        keys_list = ['N', 'R', 'I', 'RI']
        values_list = [((group_type_avr_rating_dict[x] * group_type_avr_rating_dict_size[x]) + (group_type_avr_rating_dict[y] * group_type_avr_rating_dict_size[y]) + (group_type_avr_rating_dict[z] * group_type_avr_rating_dict_size[z]))/(group_type_avr_rating_dict_size[x] + group_type_avr_rating_dict_size[y] + group_type_avr_rating_dict_size[z]) for x,y,z in zip(['G1', 'G2', 'G3', 'G4'],['G5', 'G6', 'G7', 'G8'],['G9', 'G10', 'G11', 'G12'])]
        bar_colors = ['tab:red', 'tab:blue', 'tab:green', 'tab:orange']
        plt.bar(keys_list, values_list,color=bar_colors, align='center')
        self.addlabels(keys_list, values_list)
        plt.xticks(range(len(values_list)), list(keys_list))
        plt.ylim(3, 5)
        plt.title("Average group scores")
        # plt.savefig('plots/Single/group_type_average_all_single.png')
        plt.savefig('plots/Single/Revised/group_type_average_all_single.png')
        
        plt.clf()
        keys_list = ['N', 'R', 'I', 'RI']
        values_list = [group_type_avr_rating_dict[x] for x in ['G1', 'G2', 'G3', 'G4']]
        bar_colors = ['tab:red', 'tab:blue', 'tab:green', 'tab:orange']
        plt.bar(keys_list, values_list,color=bar_colors, align='center')
        self.addlabels(keys_list, values_list)
        plt.xticks(range(len(values_list)), list(keys_list))
        plt.ylim(3, 5)
        plt.title("Average group scores for groups with no information")
        # plt.savefig('plots/Single/group_type_average_l1_single.png')
        plt.savefig('plots/Single/Revised/group_type_average_l1_single.png')
        
        plt.clf()
        keys_list = ['N', 'R', 'I', 'RI']
        values_list = [group_type_avr_rating_dict[x] for x in ['G5', 'G6', 'G7', 'G8']]
        bar_colors = ['tab:red', 'tab:blue', 'tab:green', 'tab:orange']
        plt.bar(keys_list, values_list,color=bar_colors, align='center')
        self.addlabels(keys_list, values_list)
        plt.xticks(range(len(values_list)), list(keys_list))
        plt.ylim(3, 5)
        plt.title("Average group scores for groups with partial information")
        # plt.savefig('plots/Single/group_type_average_l2_single.png')
        plt.savefig('plots/Single/Revised/group_type_average_l2_single.png')
        
        plt.clf()
        keys_list = ['N', 'R', 'I', 'RI']
        values_list = [group_type_avr_rating_dict[x] for x in ['G9', 'G10', 'G11', 'G12']]
        bar_colors = ['tab:red', 'tab:blue', 'tab:green', 'tab:orange']
        plt.bar(keys_list, values_list,color=bar_colors, align='center')
        self.addlabels(keys_list, values_list)
        plt.xticks(range(len(values_list)), list(keys_list))
        plt.ylim(3, 5)
        plt.title("Average group scores for groups with full information")
        # plt.savefig('plots/Single/group_type_average_l3_single.png')
        plt.savefig('plots/Single/Revised/group_type_average_l3_single.png')
        
    def addlabels(self, x,y):
        for i in range(len(x)):
            plt.text(i, y[i], round(y[i],2), ha = 'center')
        
    def get_group_size_average(self):
        Revised_df_list = pd.read_csv("OutPuts/Selected_first.csv")['user_id'].unique()
        plt.clf()
        group_type_rating_dict = {'G12':list(), 'G13':list(), 'G14':list(), 'G15':list(), 'G22':list(), 'G23':list(), 'G24':list(), 'G25':list(), 'G32':list(), 'G33':list(), 'G34':list(), 'G35':list(), 'G42':list(), 'G43':list(), 'G44':list(), 'G45':list(), 'G52':list(), 'G53':list(), 'G54':list(), 'G55':list(), 'G62':list(), 'G63':list(), 'G64':list(), 'G65':list(), 'G72':list(), 'G73':list(), 'G74':list(), 'G75':list(), 'G82':list(), 'G83':list(), 'G84':list(), 'G85':list(), 'G92':list(), 'G93':list(), 'G94':list(), 'G95':list(), 'G102':list(),  'G103':list(),  'G104':list(),  'G105':list(), 'G112':list(), 'G113':list(), 'G114':list(), 'G115':list(), 'G122':list(), 'G123':list(), 'G124':list(), 'G125':list()}
        df_groups_type = pd.read_csv("OutPuts/group_organizer_type.csv").drop_duplicates(subset=['organizer'])
        # df_group_ratings = pd.read_csv("OutPuts/group_ratings_single.csv")
        df_group_ratings = pd.read_csv("OutPuts/Revised/group_ratings_single.csv")
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
                if int(organizer) in group_set  and int(organizer) in Revised_df_list:
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
            else:
                group_type_avr_rating_dict[key] = 0
        width = 0.20
        ind = np.arange(12) 
        print(list(group_type_avr_rating_dict.keys()))
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
        # plt.savefig('plots/Single/group_type_average_size_single.png')
        plt.savefig('plots/Single/Revised/group_type_average_size_single.png')
        
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
        # plt.savefig('plots/Single/group_type_average_size_l2_single.png')
        plt.savefig('plots/Single/Revised/group_type_average_size_l2_single.png')
        
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
        # plt.savefig('plots/Single/group_type_average_size_l3_single.png')
        plt.savefig('plots/Single/Revised/group_type_average_size_l3_single.png')
        
    def get_group_size_average_without_info_level(self):
        Revised_df_list = pd.read_csv("OutPuts/Selected_first.csv")['user_id'].unique()
        plt.clf()
        group_type_rating_dict = {'GN2':list(), 'GN3':list(), 'GN4':list(), 'GN5':list(), 'GR2':list(), 'GR3':list(), 'GR4':list(), 'GR5':list(), 'GI2':list(), 'GI3':list(), 'GI4':list(), 'GI5':list(), 'GRI2':list(), 'GRI3':list(), 'GRI4':list(), 'GRI5':list()}
        df_groups_type = pd.read_csv("OutPuts/group_organizer_type.csv").drop_duplicates(subset=['organizer'])
        # df_group_ratings = pd.read_csv("OutPuts/group_ratings_single.csv")
        df_group_ratings = pd.read_csv("OutPuts/Revised/group_ratings_single.csv")
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
                if int(organizer) in group_set and int(organizer) in Revised_df_list:
                    group_size = df_group_size.loc[df_group_size["user_id"] == int(organizer), "size"].values
                    if group_level_type in ['G1', 'G5', 'G9']:
                        group_type = 'GN'
                    elif group_level_type in ['G2', 'G6', 'G10']:
                        group_type = 'GR'
                    elif group_level_type in ['G3', 'G7', 'G11']:
                        group_type = 'GI'
                    else:
                        group_type = 'GRI'
                    group_type = group_type + str(group_size[0])
                    group_members_list = list(group_set)
                    for member in group_members_list:
                        for restaurant in organizer_choice:
                            df_temp = df_group_ratings.loc[(df_group_ratings['user'] == member) & (df_group_ratings['restaurant'] == restaurant)]
                            new_list = group_type_rating_dict[group_type].extend(list(df_temp['rating'].values))
                            if new_list != None:
                                group_type_rating_dict[group_type] = new_list
        group_type_avr_rating_dict = dict()
        new_group_type_rating_dict = dict()
        group_type_rating_dict['GN2'].extend(group_type_rating_dict['GN3'])
        new_group_type_rating_dict['GNS'] = group_type_rating_dict['GN2']
        group_type_rating_dict['GN4'].extend(group_type_rating_dict['GN5'])
        new_group_type_rating_dict['GNL'] = group_type_rating_dict['GN4']
        group_type_rating_dict['GR2'].extend(group_type_rating_dict['GR3'])
        new_group_type_rating_dict['GRS'] = group_type_rating_dict['GR2']
        group_type_rating_dict['GR4'].extend(group_type_rating_dict['GR5'])
        new_group_type_rating_dict['GRL'] = group_type_rating_dict['GR4']
        group_type_rating_dict['GI2'].extend(group_type_rating_dict['GI3'])
        new_group_type_rating_dict['GIS'] = group_type_rating_dict['GI2']
        group_type_rating_dict['GI4'].extend(group_type_rating_dict['GI5'])
        new_group_type_rating_dict['GIL'] = group_type_rating_dict['GI4']
        group_type_rating_dict['GRI2'].extend(group_type_rating_dict['GRI3'])
        new_group_type_rating_dict['GRIS'] = group_type_rating_dict['GRI2']
        group_type_rating_dict['GRI4'].extend(group_type_rating_dict['GRI5'])
        new_group_type_rating_dict['GRIL'] = group_type_rating_dict['GRI4']
        # for key in group_type_rating_dict.keys():
        #     if len(group_type_rating_dict[key]) > 0:
        #         group_type_avr_rating_dict[key] = np.average(group_type_rating_dict[key])
        #     else:
        #         group_type_avr_rating_dict[key] = 0
        for key in new_group_type_rating_dict.keys():
            if len(new_group_type_rating_dict[key]) > 0:
                group_type_avr_rating_dict[key] = np.average(new_group_type_rating_dict[key])
            else:
                group_type_avr_rating_dict[key] = 0
        width = 0.20
        ind = np.arange(4) 
        # bar1 = plt.bar(ind, [group_type_avr_rating_dict["GN2"], group_type_avr_rating_dict["GR2"], group_type_avr_rating_dict["GI2"], group_type_avr_rating_dict["GRI2"]], width, color = 'r')
        # bar2 = plt.bar(ind+width, [group_type_avr_rating_dict["GN3"], group_type_avr_rating_dict["GR3"], group_type_avr_rating_dict["GI3"], group_type_avr_rating_dict["GRI3"]], width, color = 'g')
        # bar3 = plt.bar(ind+2*width, [group_type_avr_rating_dict["GN4"], group_type_avr_rating_dict["GR4"], group_type_avr_rating_dict["GI4"], group_type_avr_rating_dict["GRI4"]], width, color = 'b')
        # bar4 = plt.bar(ind+3*width, [group_type_avr_rating_dict["GN5"], group_type_avr_rating_dict["GR5"], group_type_avr_rating_dict["GI5"], group_type_avr_rating_dict["GRI5"]], width, color = 'm')
        
        
        
        # bar1 = plt.bar(ind, [group_type_avr_rating_dict["GN2"], group_type_avr_rating_dict["GN3"], group_type_avr_rating_dict["GN4"], group_type_avr_rating_dict["GN5"]], width, color = 'r')
        # bar2 = plt.bar(ind+width, [group_type_avr_rating_dict["GR2"], group_type_avr_rating_dict["GR3"], group_type_avr_rating_dict["GR4"], group_type_avr_rating_dict["GR5"]], width, color = 'g')
        # bar3 = plt.bar(ind+2*width, [group_type_avr_rating_dict["GI2"], group_type_avr_rating_dict["GI3"], group_type_avr_rating_dict["GI4"], group_type_avr_rating_dict["GI5"]], width, color = 'b')
        # bar4 = plt.bar(ind+3*width, [group_type_avr_rating_dict["GRI2"], group_type_avr_rating_dict["GRI3"], group_type_avr_rating_dict["GRI4"], group_type_avr_rating_dict["GRI5"]], width, color = 'm')
        
        
        # N = 3
        # ind = np.arange(N) 
        # plt.ylabel("Average Group Score")
        # plt.xlabel('Group Size')
        # plt.title("Average Group Score for groups with different sizes")
        # plt.xticks(np.arange(4)+1.5*width,['2', '3', '4', '5'])
        # plt.legend( (bar1, bar2, bar3, bar4), ('N', 'R', 'I', 'RI'))
        # plt.ylim(3, 5)
        # # plt.savefig('plots/Single/1.group_type_average_size_single_without_level.png')
        # plt.savefig('plots/Single/Revised/group_type_average_size_single_without_level.png')
        fig, ax = plt.subplots()
        width = 0.20
        ind = np.arange(2) 
        bar1 = ax.bar(ind, [group_type_avr_rating_dict["GNS"], group_type_avr_rating_dict["GNL"]], width, color = 'r')
        bar2 = ax.bar(ind+width, [group_type_avr_rating_dict["GRS"], group_type_avr_rating_dict["GRL"]], width, color = 'g')
        bar3 = ax.bar(ind+2*width, [group_type_avr_rating_dict["GIS"], group_type_avr_rating_dict["GIL"]], width, color = 'b')
        bar4 = ax.bar(ind+3*width, [group_type_avr_rating_dict["GRIS"], group_type_avr_rating_dict["GRIL"]], width, color = 'm')
        def autolabel(rects):
            """Attach a text label above each bar in *rects*, displaying its height."""
            for rect in rects:
                height = rect.get_height()
                ax.annotate('{}'.format(round(height,2)),
                            xy=(rect.get_x() + rect.get_width() / 2, height),
                            xytext=(0, 3),  # 3 points vertical offset
                            textcoords="offset points",
                            ha='center', va='bottom')
        autolabel(bar1)
        autolabel(bar2)
        autolabel(bar3)
        autolabel(bar4)

        N = 3
        ind = np.arange(N) 
        ax.set_ylabel("MIL")
        ax.set_xlabel('Group Size')
        ax.set_title("Average Group Score for groups with different size")
        ax.set_xticks(np.arange(2)+1.5*width,['Small', 'Large'])
        ax.legend( (bar1, bar2, bar3, bar4), ('N', 'R', 'I', 'RI'), loc='upper left')
        ax.set_ylim(3, 5)
        fig.savefig('plots/Single/Revised/group_type_average_size_single_without_level_mixed.png')
        
        x = new_group_type_rating_dict["GNS"]
        y = new_group_type_rating_dict["GRIS"]
        res = mannwhitneyu(x, y)
        print(res)
        res = f_oneway(new_group_type_rating_dict["GNL"], new_group_type_rating_dict["GRL"], new_group_type_rating_dict["GIL"], new_group_type_rating_dict["GRIL"])
        print(res)

    def get_organizer_choice(self, organizer):
        query = f"SELECT choice FROM user_group_info WHERE user_id = {organizer}"
        my_cursor = self.mysql_conn.cursor(buffered=True)
        my_cursor.execute(query)
        choices_list = []
        for choice in my_cursor:
            choices_list.append(choice[0])
        return choices_list
    
    def avr_individual_loss(self):
        Revised_df_list = pd.read_csv("OutPuts/Selected_first.csv")['user_id'].unique()
        tripScore = {1: 4,2: 4.5,3: 4,4: 4,5: 4,6: 4,7: 4.5,8: 3.5,9: 3,10: 4.5,11: 4.5,12: 4.5,13: 4.5,15: 4.5,16: 4.5,17: 4,18: 5,19: 4,20: 4,21: 2,22: 4.5,23: 4,24: 4.5,25: 4,26: 4.5,27: 3.5,28: 4.5,29: 3.5,30: 5,31: 4.5,32: 5}
        price = {18:1, 30:1, 2:2, 31: 1, 25:2, 23:2, 19:2, 20:2, 1:1, 27:0, 8:0, 9:0, 21:0, 17:1, 3:0, 26:1, 24:0, 11:2, 4: 0, 12:2, 32:2, 6:0, 7:1, 16:1, 10: 1, 13:0, 15:0, 28:2, 22: 2, 5:0, 29:0}
        diversity = { 18:6, 30:5, 2: 6, 31: 3, 25:8, 23:7, 19:7, 20:5, 1:4, 27:8, 8:7, 9:7, 21:5, 17:7, 3:6, 26:6, 24:6, 11:6, 4: 5, 12:5, 32:5, 6:5, 7:4, 16:4,  10: 4, 13:1, 15:1, 28:1, 22:7, 5:8, 29:10}
        pop = {18:4, 30:2, 2: 1, 31:1, 25:2, 23:1, 19:0, 20:2, 1:1, 27:1, 8:1, 9:1, 21:1, 17:1, 3:1, 26:1, 24:1, 11:1, 4: 2, 12:0, 32:2, 6:1, 7:1, 16:1, 10:1, 13:1, 15:1, 28:1, 22:2, 5:4, 29:5}
        df = pd.DataFrame(columns=["user_id", "organizer_id", "group_type", "system_type", "rest_id", "rating", "rest_trip_score", "price", "diversity", "popularity"])
        plt.clf()
        group_type_rating_dict = {'G1':list(), 'G2':list(), 'G3':list(), 'G4':list(), 'G5':list(), 'G6':list(), 'G7':list(), 'G8':list(), 'G9':list(), 'G10':list(), 'G11':list(), 'G12':list()}
        df_groups_type = pd.read_csv("OutPuts/group_organizer_type.csv").drop_duplicates(subset=['organizer'])
        # df_individual_ratings = pd.read_csv("OutPuts/individual_ratings_single.csv")
        df_individual_ratings = pd.read_csv("OutPuts/Revised/individual_ratings_single.csv")
        df_booked = pd.read_csv("OutPuts/organizer_booked_cleaned_single.csv")
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
                if int(organizer) in group_set and int(organizer) in Revised_df_list:
                    group_members_list = list(group_set)
                    for member in group_members_list:
                        member_max_score = self.get_member_max_score(member)
                        for restaurant in organizer_choice:
                            df_temp = df_individual_ratings.loc[(df_individual_ratings['user'] == member) & (df_individual_ratings['restaurant'] == restaurant)]
                            new_list = group_type_rating_dict[group_type].extend([member_max_score - x for x in list(df_temp['rating'].values)])
                            if new_list != None:
                                group_type_rating_dict[group_type] = new_list
                            for rating in [member_max_score - x for x in list(df_temp['rating'].values)]:
                                df = df.append(pd.DataFrame([[member,organizer,group_only_type,system_type,restaurant,rating, tripScore[restaurant], price[restaurant], diversity[restaurant], pop[restaurant] ]], columns=["user_id", "organizer_id", "group_type", "system_type", "rest_id", "rating", "rest_trip_score", "price", "diversity", "popularity"]))
        group_type_avr_rating_dict = dict()
        plt.clf()
        group_type_avr_rating_dict_size = dict()
        # x = new_group_type_rating_dict["GNL"]
        # y = new_group_type_rating_dict["GRIL"]
        # res = mannwhitneyu(x, y)
        # print(res)
        GN = []
        GN.extend(group_type_rating_dict['G1'])
        GN.extend(group_type_rating_dict['G5'])
        GN.extend(group_type_rating_dict['G9'])
        GR = []
        GR.extend(group_type_rating_dict['G2'])
        GR.extend(group_type_rating_dict['G6'])
        GR.extend(group_type_rating_dict['G10'])
        GI = []
        GI.extend(group_type_rating_dict['G3'])
        GI.extend(group_type_rating_dict['G7'])
        GI.extend(group_type_rating_dict['G11'])
        GRI = []
        GRI.extend(group_type_rating_dict['G4'])
        GRI.extend(group_type_rating_dict['G8'])
        GRI.extend(group_type_rating_dict['G12'])
        # res = f_oneway(GN,GR,GI,GRI)
        # print(res)
        # input()
        GN = []
        # GN.extend(group_type_rating_dict['G1'])
        # GN.extend(group_type_rating_dict['G5'])
        GN.extend(group_type_rating_dict['G9'])
        GR = []
        # GR.extend(group_type_rating_dict['G2'])
        # GR.extend(group_type_rating_dict['G6'])
        GR.extend(group_type_rating_dict['G10'])
        GI = []
        # GI.extend(group_type_rating_dict['G3'])
        # GI.extend(group_type_rating_dict['G7'])
        GI.extend(group_type_rating_dict['G11'])
        GRI = []
        # GRI.extend(group_type_rating_dict['G4'])
        # GRI.extend(group_type_rating_dict['G8'])
        GRI.extend(group_type_rating_dict['G12'])
        res = f_oneway(GN,GR,GI,GRI)
        print(res)
        input("Level")
        for key in group_type_rating_dict.keys():
            if len(group_type_rating_dict[key]) > 0:
                group_type_avr_rating_dict[key] = np.average(group_type_rating_dict[key])
                group_type_avr_rating_dict_size[key] = len(group_type_rating_dict[key])
        df.drop_duplicates(subset=["user_id","organizer_id"],inplace=True)
        # df.to_csv("OutPuts/df_individual_loss_with_trip_score_single.csv")
        df.to_csv("OutPuts/Revised/df_individual_loss_with_trip_score_single.csv")
        plt.bar(list(group_type_avr_rating_dict.keys()), list(group_type_avr_rating_dict.values()), align='center')
        plt.xticks(range(len(group_type_avr_rating_dict)), list(group_type_avr_rating_dict.keys()))
        plt.ylim(0, 2)

        # plt.savefig('plots/Single/avr_individual_loss_single.png')
        plt.savefig('plots/Single/Revised/avr_individual_loss_single.png')
        
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
        # plt.savefig('plots/Single/Loss_all_box_single.png')
        plt.savefig('plots/Single/Revised/Loss_all_box_single.png')
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
        # plt.savefig('plots/Single/Loss_No_box_single.png')
        plt.savefig('plots/Single/Revised/Loss_No_box_single.png')
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
        # plt.savefig('plots/Single/Loss_partial_box_single.png')
        plt.savefig('plots/Single/Revised/Loss_partial_box_single.png')
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
        # plt.savefig('plots/Single/Loss_full_box_single.png')
        plt.savefig('plots/Single/Revised/Loss_full_box_single.png')
        # input("Yes")
        
        plt.clf()
        keys_list = ['N', 'R', 'I', 'RI']
        values_list = [((group_type_avr_rating_dict[x] * group_type_avr_rating_dict_size[x]) + (group_type_avr_rating_dict[y] * group_type_avr_rating_dict_size[y]) + (group_type_avr_rating_dict[z] * group_type_avr_rating_dict_size[z]))/(group_type_avr_rating_dict_size[x] + group_type_avr_rating_dict_size[y] + group_type_avr_rating_dict_size[z]) for x,y,z in zip(['G1', 'G2', 'G3', 'G4'],['G5', 'G6', 'G7', 'G8'],['G9', 'G10', 'G11', 'G12'])]
        print(values_list)
        bar_colors = ['tab:red', 'tab:blue', 'tab:green', 'tab:orange']
        plt.bar(keys_list, values_list,color=bar_colors, align='center')
        self.addlabels(keys_list, values_list)
        plt.xticks(range(len(values_list)), list(keys_list))
        plt.ylim(0, 2)
        plt.title("Mean Individual Loss")
        # plt.savefig('plots/Single/avr_individual_loss_all_single.png')
        plt.savefig('plots/Single/Revised/avr_individual_loss_all_single.png')
        
        plt.clf()
        keys_list = ['N', 'R', 'I', 'RI']
        values_list = [group_type_avr_rating_dict[x] for x in ['G1', 'G2', 'G3', 'G4']]
        bar_colors = ['tab:red', 'tab:blue', 'tab:green', 'tab:orange']
        plt.bar(keys_list, values_list,color=bar_colors, align='center')
        plt.xticks(range(len(values_list)), list(keys_list))
        plt.ylim(0, 2)
        self.addlabels(keys_list, values_list)
        plt.title("MIL for groups with No information")
        # plt.savefig('plots/Single/avr_individual_loss_l1_single.png')
        plt.savefig('plots/Single/Revised//avr_individual_loss_l1_single.png')
        
        plt.clf()
        keys_list = ['N', 'R', 'I', 'RI']
        values_list = [group_type_avr_rating_dict[x] for x in ['G5', 'G6', 'G7', 'G8']]
        plt.bar(keys_list, values_list, align='center')
        plt.xticks(range(len(values_list)), list(['N', 'R', 'I', 'RI']))
        plt.ylim(0, 2)
        self.addlabels(keys_list, values_list)
        bar_colors = ['tab:red', 'tab:blue', 'tab:green', 'tab:orange']
        plt.bar(keys_list, values_list,color=bar_colors, align='center')
        plt.title("MIL for groups with partial information")
        # plt.savefig('plots/Single/avr_individual_loss_l2_single.png')
        plt.savefig('plots/Single/Revised/avr_individual_loss_l2_single.png')
        
        plt.clf()
        keys_list = ['N', 'R', 'I', 'RI']
        values_list = [group_type_avr_rating_dict[x] for x in ['G9', 'G10', 'G11', 'G12']]
        bar_colors = ['tab:red', 'tab:blue', 'tab:green', 'tab:orange']
        plt.bar(keys_list, values_list,color=bar_colors, align='center')
        plt.xticks(range(len(values_list)), list(['N', 'R', 'I', 'RI']))
        plt.ylim(0, 2)
        self.addlabels(keys_list, values_list)
        plt.title("MIL for groups with full information")
        # plt.savefig('plots/Single/avr_individual_loss_l3_single.png')
        plt.savefig('plots/Single/Revised/avr_individual_loss_l3_single.png')
     
    def avr_individual_loss_size(self):
        plt.clf()
        group_type_rating_dict = {'G12':list(), 'G13':list(), 'G14':list(), 'G15':list(), 'G22':list(), 'G23':list(), 'G24':list(), 'G25':list(), 'G32':list(), 'G33':list(), 'G34':list(), 'G35':list(), 'G42':list(), 'G43':list(), 'G44':list(), 'G45':list(), 'G52':list(), 'G53':list(), 'G54':list(), 'G55':list(), 'G62':list(), 'G63':list(), 'G64':list(), 'G65':list(), 'G72':list(), 'G73':list(), 'G74':list(), 'G75':list(), 'G82':list(), 'G83':list(), 'G84':list(), 'G85':list(), 'G92':list(), 'G93':list(), 'G94':list(), 'G95':list(), 'G102':list(),  'G103':list(),  'G104':list(),  'G105':list(), 'G112':list(), 'G113':list(), 'G114':list(), 'G115':list(), 'G122':list(), 'G123':list(), 'G124':list(), 'G125':list()}
        df_groups_type = pd.read_csv("OutPuts/group_organizer_type.csv")
        df_individual_ratings = pd.read_csv("OutPuts/individual_ratings_single.csv")
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
            else:
                group_type_avr_rating_dict[key] = 0
        
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
        plt.savefig('plots/Single/avr_individual_loss_size_single.png')
        
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
        plt.savefig('plots/Single/avr_individual_loss_size_l1_single.png')
        
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
        plt.savefig('plots/Single/avr_individual_loss_size_l2_single.png')
        
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
        plt.savefig('plots/Single/avr_individual_loss_size_l3_single.png')
        
    def avr_individual_loss_size_without_info_level(self):
        Revised_df_list = pd.read_csv("OutPuts/Selected_first.csv")['user_id'].unique()
        plt.clf()
        group_type_rating_dict = {'GN2':list(), 'GN3':list(), 'GN4':list(), 'GN5':list(), 'GR2':list(), 'GR3':list(), 'GR4':list(), 'GR5':list(), 'GI2':list(), 'GI3':list(), 'GI4':list(), 'GI5':list(), 'GRI2':list(), 'GRI3':list(), 'GRI4':list(), 'GRI5':list()}
        df_groups_type = pd.read_csv("OutPuts/group_organizer_type.csv").drop_duplicates(subset=['organizer'])
        # df_individual_ratings = pd.read_csv("OutPuts/individual_ratings_single.csv")
        df_individual_ratings = pd.read_csv("OutPuts/Revised/individual_ratings_single.csv")
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
                if int(organizer) in group_set and int(organizer) in Revised_df_list:
                    group_members_list = list(group_set)
                    group_size = df_group_size.loc[df_group_size["user_id"] == int(organizer), "size"].values
                    if group_level_type in ['G1', 'G5', 'G9']:
                        group_type = 'GN'
                    elif group_level_type in ['G2', 'G6', 'G10']:
                        group_type = 'GR'
                    elif group_level_type in ['G3', 'G7', 'G11']:
                        group_type = 'GI'
                    else:
                        group_type = 'GRI'
                    group_type = group_type + str(group_size[0])
                    for member in group_members_list:
                        member_max_score = self.get_member_max_score(member)
                        for restaurant in organizer_choice:
                            df_temp = df_individual_ratings.loc[(df_individual_ratings['user'] == member) & (df_individual_ratings['restaurant'] == restaurant)]
                            new_list = group_type_rating_dict[group_type].extend([member_max_score - x for x in list(df_temp['rating'].values)])
                            if new_list != None:
                                group_type_rating_dict[group_type] = new_list
        group_type_avr_rating_dict = dict()
        new_group_type_rating_dict = dict()
        group_type_rating_dict['GN2'].extend(group_type_rating_dict['GN3'])
        new_group_type_rating_dict['GNS'] = group_type_rating_dict['GN2']
        group_type_rating_dict['GN4'].extend(group_type_rating_dict['GN5'])
        new_group_type_rating_dict['GNL'] = group_type_rating_dict['GN4']
        group_type_rating_dict['GR2'].extend(group_type_rating_dict['GR3'])
        new_group_type_rating_dict['GRS'] = group_type_rating_dict['GR2']
        group_type_rating_dict['GR4'].extend(group_type_rating_dict['GR5'])
        new_group_type_rating_dict['GRL'] = group_type_rating_dict['GR4']
        group_type_rating_dict['GI2'].extend(group_type_rating_dict['GI3'])
        new_group_type_rating_dict['GIS'] = group_type_rating_dict['GI2']
        group_type_rating_dict['GI4'].extend(group_type_rating_dict['GI5'])
        new_group_type_rating_dict['GIL'] = group_type_rating_dict['GI4']
        group_type_rating_dict['GRI2'].extend(group_type_rating_dict['GRI3'])
        new_group_type_rating_dict['GRIS'] = group_type_rating_dict['GRI2']
        group_type_rating_dict['GRI4'].extend(group_type_rating_dict['GRI5'])
        new_group_type_rating_dict['GRIL'] = group_type_rating_dict['GRI4']
        # for key in group_type_rating_dict.keys():
        #     if len(group_type_rating_dict[key]) > 0:
        #         group_type_avr_rating_dict[key] = np.average(group_type_rating_dict[key])
        #     else:
        #         group_type_avr_rating_dict[key] = 0
        
        for key in new_group_type_rating_dict.keys():
            if len(new_group_type_rating_dict[key]) > 0:
                group_type_avr_rating_dict[key] = np.average(new_group_type_rating_dict[key])
            else:
                group_type_avr_rating_dict[key] = 0
        
        # width = 0.20
        # ind = np.arange(4) 
        # bar1 = plt.bar(ind, [group_type_avr_rating_dict["GN2"], group_type_avr_rating_dict["GN3"], group_type_avr_rating_dict["GN4"], group_type_avr_rating_dict["GN5"]], width, color = 'r')
        # bar2 = plt.bar(ind+width, [group_type_avr_rating_dict["GR2"], group_type_avr_rating_dict["GR3"], group_type_avr_rating_dict["GR4"], group_type_avr_rating_dict["GR5"]], width, color = 'g')
        # bar3 = plt.bar(ind+2*width, [group_type_avr_rating_dict["GI2"], group_type_avr_rating_dict["GI3"], group_type_avr_rating_dict["GI4"], group_type_avr_rating_dict["GI5"]], width, color = 'b')
        # bar4 = plt.bar(ind+3*width, [group_type_avr_rating_dict["GRI2"], group_type_avr_rating_dict["GRI3"], group_type_avr_rating_dict["GRI4"], group_type_avr_rating_dict["GRI5"]], width, color = 'm')
        fig, ax = plt.subplots()
        width = 0.20
        ind = np.arange(2) 
        bar1 = ax.bar(ind, [group_type_avr_rating_dict["GNS"], group_type_avr_rating_dict["GNL"]], width, color = 'r')
        bar2 = ax.bar(ind+width, [group_type_avr_rating_dict["GRS"], group_type_avr_rating_dict["GRL"]], width, color = 'g')
        bar3 = ax.bar(ind+2*width, [group_type_avr_rating_dict["GIS"], group_type_avr_rating_dict["GIL"]], width, color = 'b')
        bar4 = ax.bar(ind+3*width, [group_type_avr_rating_dict["GRIS"], group_type_avr_rating_dict["GRIL"]], width, color = 'm')
        
        
        N = 3
        ind = np.arange(N) 
        ax.set_ylabel("MIL")
        ax.set_xlabel('Group Size')
        ax.set_title("MIL for groups with different sizes")
        ax.set_xticks(np.arange(2)+1.5*width,['Small', 'Large'])
        ax.legend( (bar1, bar2, bar3, bar4), ('N', 'R', 'I', 'RI'))
        ax.set_ylim(0,2)
        # plt.savefig('plots/Single/1.avr_individual_loss_size_single_without_level.png')
        
        
        def autolabel(rects):
            """Attach a text label above each bar in *rects*, displaying its height."""
            for rect in rects:
                height = rect.get_height()
                ax.annotate('{}'.format(round(height,2)),
                            xy=(rect.get_x() + rect.get_width() / 2, height),
                            xytext=(0, 3),  # 3 points vertical offset
                            textcoords="offset points",
                            ha='center', va='bottom')
        autolabel(bar1)
        autolabel(bar2)
        autolabel(bar3)
        autolabel(bar4)
        fig.savefig('plots/Single/Revised/avr_individual_loss_size_single_without_level_mixed.png')
        
        plt.clf()
        x = new_group_type_rating_dict["GNS"]
        y = new_group_type_rating_dict["GRIS"]
        res = mannwhitneyu(x, y, alternative='greater')
        print(res)
        res = f_oneway(new_group_type_rating_dict["GNL"], new_group_type_rating_dict["GRL"], new_group_type_rating_dict["GIL"], new_group_type_rating_dict["GRIL"])
        print(res)
        input("Done")
        
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
        # df_individual_ratings = pd.read_csv("OutPuts/df_individual_loss_with_trip_score_single.csv")
        df_individual_ratings = pd.read_csv("OutPuts/Revised/df_individual_loss_with_trip_score_single.csv")
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
                            df_temp = df_individual_ratings.loc[(df_individual_ratings['user_id'] == member) & (df_individual_ratings['rest_id'] == restaurant), "rating"]
                            if len(list(df_temp.values)) > 0:
                                group_restaurant_rating_list.append(np.mean(list(df_temp.values)))
                        if group_restaurant_rating_list != None and len(group_restaurant_rating_list) > 0:
                            group_type_rating_dict[group_type].append(np.var(group_restaurant_rating_list))
        group_type_avr_rating_dict = dict()
        
        GN = []
        GN.extend(group_type_rating_dict['G1'])
        GN.extend(group_type_rating_dict['G5'])
        GN.extend(group_type_rating_dict['G9'])
        GR = []
        GR.extend(group_type_rating_dict['G2'])
        GR.extend(group_type_rating_dict['G6'])
        GR.extend(group_type_rating_dict['G10'])
        GI = []
        GI.extend(group_type_rating_dict['G3'])
        GI.extend(group_type_rating_dict['G7'])
        GI.extend(group_type_rating_dict['G11'])
        GRI = []
        GRI.extend(group_type_rating_dict['G4'])
        GRI.extend(group_type_rating_dict['G8'])
        GRI.extend(group_type_rating_dict['G12'])
        res = f_oneway(GN,GR,GI,GRI)
        print(res)
        input()
        
        for key in group_type_rating_dict.keys():
            if len(group_type_rating_dict[key]) > 0:
                group_type_avr_rating_dict[key] = np.average(group_type_rating_dict[key])
        plt.bar(list(group_type_avr_rating_dict.keys()), list(group_type_avr_rating_dict.values()), align='center')
        plt.xticks(range(len(group_type_avr_rating_dict)), list(group_type_avr_rating_dict.keys()))
        # plt.savefig('plots/avr_fairness.png')
        plt.savefig('plots/Single/Revised/avr_fairness.png')
        
        plt.clf()
        keys_list = ['G1', 'G2', 'G3', 'G4']
        values_list = [group_type_avr_rating_dict[x] for x in ['G1', 'G2', 'G3', 'G4']]
        plt.title("Fairness for groups with No Information")
        plt.bar(keys_list, values_list, align='center')
        plt.xticks(range(len(values_list)), ['N', 'R', 'I', 'RI'])
        plt.ylim(0, 0.8)
        # plt.savefig('plots/Single/avr_fairness_l1_single.png')
        plt.savefig('plots/Single/Revised/avr_fairness_l1_single.png')
        
        plt.clf()
        keys_list = ['G5', 'G6', 'G7', 'G8']
        values_list = [group_type_avr_rating_dict[x] for x in keys_list]
        plt.title("Fairness for groups with Partial Information")
        plt.bar(keys_list, values_list, align='center')
        plt.xticks(range(len(values_list)), ['N', 'R', 'I', 'RI'])
        plt.ylim(0, 0.8)
        # plt.savefig('plots/Single/avr_fairness_l2_single.png')
        plt.savefig('plots/Single/Revised/avr_fairness_l2_single.png')
        
        plt.clf()
        keys_list = ['G9', 'G10', 'G11', 'G12']
        values_list = [group_type_avr_rating_dict[x] for x in keys_list]
        plt.title("Fairness for groups with Full Information")
        plt.bar(keys_list, values_list, align='center')
        plt.xticks(range(len(values_list)), ['N', 'R', 'I', 'RI'])
        plt.ylim(0, 0.8)
        # plt.savefig('plots/Single/avr_fairness_l3_single.png')
        plt.savefig('plots/Single/Revised/avr_fairness_l3_single.png')
        
        plt.clf()
        keys_list = ['N', 'R', 'I', 'RI']
        values_list = [(group_type_avr_rating_dict[x] + group_type_avr_rating_dict[y] + group_type_avr_rating_dict[z])/3 for x,y,z in zip(['G1', 'G2', 'G3', 'G4'],['G5', 'G6', 'G7', 'G8'],['G9', 'G10', 'G11', 'G12'])]
        plt.title("Fairness")
        bar_colors = ['tab:red', 'tab:blue', 'tab:green', 'tab:orange']
        plt.bar(keys_list, values_list,color=bar_colors, align='center')
        self.addlabels(keys_list, values_list)
        plt.xticks(range(len(values_list)), ['N', 'R', 'I', 'RI'])
        plt.ylim(0, 0.8)
        plt.title("Fairness")
        # plt.savefig('plots/Single/avr_fair_all_single.png')
        plt.savefig('plots/Single/Revised/avr_fair_all_single.png')
    
    def item_fairness_size(self):
        plt.clf()
        group_type_rating_dict = {'G12':list(), 'G13':list(), 'G14':list(), 'G15':list(), 'G22':list(), 'G23':list(), 'G24':list(), 'G25':list(), 'G32':list(), 'G33':list(), 'G34':list(), 'G35':list(), 'G42':list(), 'G43':list(), 'G44':list(), 'G45':list(), 'G52':list(), 'G53':list(), 'G54':list(), 'G55':list(), 'G62':list(), 'G63':list(), 'G64':list(), 'G65':list(), 'G72':list(), 'G73':list(), 'G74':list(), 'G75':list(), 'G82':list(), 'G83':list(), 'G84':list(), 'G85':list(), 'G92':list(), 'G93':list(), 'G94':list(), 'G95':list(), 'G102':list(),  'G103':list(),  'G104':list(),  'G105':list(), 'G112':list(), 'G113':list(), 'G114':list(), 'G115':list(), 'G122':list(), 'G123':list(), 'G124':list(), 'G125':list()}
        df_groups_type = pd.read_csv("OutPuts/group_organizer_type.csv")
        df_individual_ratings = pd.read_csv("OutPuts/individual_ratings_single.csv")
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
            else:
                group_type_avr_rating_dict[key] = 0
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
        plt.savefig('plots/Single/avr_fairness_size_single.png')
        
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
        plt.savefig('plots/Single/avr_fairness_size_l1_single.png')
        
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
        plt.savefig('plots/Single/avr_fairness_size_l2_single.png')
        
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
        plt.savefig('plots/Single/avr_fairness_size_l3_single.png')
    
    def item_fairness_size_without_info_level(self):
        plt.clf()
        group_type_rating_dict = {'GN2':list(), 'GN3':list(), 'GN4':list(), 'GN5':list(), 'GR2':list(), 'GR3':list(), 'GR4':list(), 'GR5':list(), 'GI2':list(), 'GI3':list(), 'GI4':list(), 'GI5':list(), 'GRI2':list(), 'GRI3':list(), 'GRI4':list(), 'GRI5':list()}
        df_groups_type = pd.read_csv("OutPuts/group_organizer_type.csv").drop_duplicates(subset=['organizer'])
        # df_individual_ratings = pd.read_csv("OutPuts/df_individual_loss_with_trip_score_single.csv")
        df_individual_ratings = pd.read_csv("OutPuts/Revised/df_individual_loss_with_trip_score_single.csv")
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
                    if group_level_type in ['G1', 'G5', 'G9']:
                        group_type = 'GN'
                    elif group_level_type in ['G2', 'G6', 'G10']:
                        group_type = 'GR'
                    elif group_level_type in ['G3', 'G7', 'G11']:
                        group_type = 'GI'
                    else:
                        group_type = 'GRI'
                    group_type = group_type + str(group_size[0])
                    for restaurant in organizer_choice:
                        group_restaurant_rating_list = list()
                        for member in group_members_list:
                            df_temp = df_individual_ratings.loc[(df_individual_ratings['user_id'] == member) & (df_individual_ratings['rest_id'] == restaurant), "rating"]
                            if len(list(df_temp.values)) > 0:
                                group_restaurant_rating_list.append(np.mean(list(df_temp.values)))
                        if group_restaurant_rating_list != None and len(group_restaurant_rating_list) > 0:
                            group_type_rating_dict[group_type].append(np.var(group_restaurant_rating_list))
        group_type_avr_rating_dict = dict()
        for key in group_type_rating_dict.keys():
            if len(group_type_rating_dict[key]) > 0:
                group_type_avr_rating_dict[key] = np.average(group_type_rating_dict[key])
            else:
                group_type_avr_rating_dict[key] = 0
        width = 0.20
        ind = np.arange(4) 
        
        bar1 = plt.bar(ind, [group_type_avr_rating_dict["GN2"], group_type_avr_rating_dict["GN3"], group_type_avr_rating_dict["GN4"], group_type_avr_rating_dict["GN5"]], width, color = 'r')
        bar2 = plt.bar(ind+width, [group_type_avr_rating_dict["GR2"], group_type_avr_rating_dict["GR3"], group_type_avr_rating_dict["GR4"], group_type_avr_rating_dict["GR5"]], width, color = 'g')
        bar3 = plt.bar(ind+2*width, [group_type_avr_rating_dict["GI2"], group_type_avr_rating_dict["GI3"], group_type_avr_rating_dict["GI4"], group_type_avr_rating_dict["GI5"]], width, color = 'b')
        bar4 = plt.bar(ind+3*width, [group_type_avr_rating_dict["GRI2"], group_type_avr_rating_dict["GRI3"], group_type_avr_rating_dict["GRI4"], group_type_avr_rating_dict["GRI5"]], width, color = 'm')
        N = 3
        ind = np.arange(N) 
        plt.ylabel("Average Fairness")
        plt.xlabel('Group size')
        plt.title("Fairness for groups with different size")
        plt.xticks(np.arange(4)+1.5*width,['2', '3', '4', '5'])
        plt.legend( (bar1, bar2, bar3, bar4), ('N', 'R', 'I', 'RI'))
        plt.ylim(0, 1.3)
        # plt.savefig('plots/Single/1.avr_fairness_size_single_without_level.png')
        plt.savefig('plots/Single/Revised/avr_fairness_size_single_without_level.png')
    
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
                    
    def number_of_usages_R_I(self):
        df_remember = pd.read_csv("./OutPuts/organizer_usage_remeber_single.csv")
        df_conflict = pd.read_csv("./OutPuts/organizer_usage_conflict_single.csv")
        df_selected_organizers = pd.read_csv("./OutPuts/group_organizer_type_single.csv")
        group_type_rating_dict = {'G1':0, 'G2':0, 'G3':0, 'G4':0, 'G5':0, 'G6':0, 'G7':0, 'G8':0, 'G9':0, 'G10':0, 'G11':0, 'G12':0}
        group_type_usage_dict = {'G1':0, 'G2':0, 'G3':0, 'G4':0, 'G5':0, 'G6':0, 'G7':0, 'G8':0, 'G9':0, 'G10':0, 'G11':0, 'G12':0}
        df_groups_type = pd.read_csv("OutPuts/group_organizer_type.csv").drop_duplicates(subset=['organizer'])
        organizer_set = set()
        
        unique_count_remember = df_remember.groupby('for_user').size().reset_index(name='Count')
        print("Number of recalling used for different users:", len(unique_count_remember))
        for index, row in df_remember.iterrows():
            if row['user_id'] not in organizer_set:
                group_type = df_groups_type.loc[df_groups_type['organizer'] == row['user_id']]['type'].values[0]
                group_type_usage_dict[group_type] = group_type_usage_dict[group_type] + 1
                organizer_set.add(row['user_id'])
                print(group_type_usage_dict)
                # input()
        
        unique_count_remember = df_conflict.groupby('for_user').size().reset_index(name='Count')
        print("Number of incompatibel used for different users:", len(unique_count_remember))
        
        unique_count_remember = df_remember.groupby('user_id').size().reset_index(name='Count')
        print("Number of of organizer used recalling:", len(unique_count_remember))
        
        unique_count_remember = df_conflict.groupby('user_id').size().reset_index(name='Count')
        print("Number of organizer used incompatibel:", len(unique_count_remember))
        
        for index, group in df_selected_organizers.drop_duplicates(subset='organizer').iterrows():
            group_type_rating_dict[group['type']] = group_type_rating_dict[group['type']] +  1
        print('Number of organizers in each system', group_type_rating_dict)
        
        print('Number of organizers for system N', group_type_rating_dict['G1'] + group_type_rating_dict['G5'] + group_type_rating_dict['G9'])
        print('Number of organizers for system only R', group_type_rating_dict['G2'] + group_type_rating_dict['G6'] + group_type_rating_dict['G10'])
        print('Number of organizers for system only R for groups with No information', group_type_rating_dict['G2'])
        print('Number of organizers for system only R for groups with Partial information', group_type_rating_dict['G2'])
        print('Number of organizers for system only I', group_type_rating_dict['G3'] + group_type_rating_dict['G7'] + group_type_rating_dict['G11'])
        print('Number of organizers for system R and I', group_type_rating_dict['G4'] + group_type_rating_dict['G8'] + group_type_rating_dict['G12'])
        print('Number of organizers for system R and I for groups with No information', group_type_rating_dict['G4'])
        print('Number of organizers for system R and I for groups with Partial information', group_type_rating_dict['G8'])
        print('Number of organizers for system R', group_type_rating_dict['G2'] + group_type_rating_dict['G6'] + group_type_rating_dict['G10'] + group_type_rating_dict['G4'] + group_type_rating_dict['G8'] + group_type_rating_dict['G12'])
        
        print('Number of organizers for system I', group_type_rating_dict['G3'] + group_type_rating_dict['G7'] + group_type_rating_dict['G11'] + group_type_rating_dict['G4'] + group_type_rating_dict['G8'] + group_type_rating_dict['G12'])
        
    def number_of_usages_R_I_list(self):
        df_remember = pd.read_csv("./OutPuts/organizer_usage_remeber_single2.csv")
        df_conflict = pd.read_csv("./OutPuts/organizer_usage_conflict_single2.csv")
        df_selected_organizers = pd.read_csv("./OutPuts/group_organizer_type_single.csv")
        group_type_rating_dict = {'G1':set(), 'G2':set(), 'G3':set(), 'G4':set(), 'G5':set(), 'G6':set(), 'G7':set(), 'G8':set(), 'G9':set(), 'G10':set(), 'G11':set(), 'G12':set()}
        remembering_set = set(df_remember.drop_duplicates(subset='user_id')['user_id'])
        df_conflict_set = set(df_conflict.drop_duplicates(subset='user_id')['user_id'])
        
        return remembering_set.union(df_conflict_set)
        
    def get_group_average_supporting_used(self):
        tripScore = {1: 4,2: 4.5,3: 4,4: 4,5: 4,6: 4,7: 4.5,8: 3.5,9: 3,10: 4.5,11: 4.5,12: 4.5,13: 4.5,15: 4.5,16: 4.5,17: 4,18: 5,19: 4,20: 4,21: 2,22: 4.5,23: 4,24: 4.5,25: 4,26: 4.5,27: 3.5,28: 4.5,29: 3.5,30: 5,31: 4.5,32: 5}
        df = pd.DataFrame(columns=["user_id", "organizer_id", "group_type", "system_type", "rest_id", "rating", "rest_trip_score"])
        plt.clf()
        organizer_used_supports = self.number_of_usages_R_I_list()
        print(organizer_used_supports)
        group_type_rating_dict = {'G1':[0], 'G2':list(), 'G3':list(), 'G4':list(), 'G5':[0], 'G6':list(), 'G7':list(), 'G8':list(), 'G9':[0], 'G10':list(), 'G11':list(), 'G12':list()}
        df_groups_type = pd.read_csv("OutPuts/group_organizer_type_single.csv")
        df_group_ratings = pd.read_csv("OutPuts/group_ratings_single.csv")
        for index, row in df_groups_type.iterrows():
            organizer = row['organizer']
            group_type = row['type']
            if (int(organizer)  in organizer_used_supports):
                group_only_type = self.get_group_type(group_type)
                system_type = self.get_system_type(group_type)
                df_groups = pd.read_csv("OutPuts/groups_members.csv")
                df_groups.fillna(-1,inplace=True)
                for group_index, group_row in df_groups.iterrows():
                    group_set = set([int(group_row['member1']), int(group_row['member2']), int(group_row['member3']), int(group_row['member4']), int(group_row['member5'])])
                    if -1 in group_set:
                        group_set.remove(-1)
                    organizer_choice = self.get_organizer_choice(organizer)
                    
                    if (int(organizer) in group_set):
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
        # df.drop_duplicates(subset=["user_id","organizer_id"],inplace=True)
        # df.to_csv("OutPuts/df_groups_ratings_with_trip_score_single.csv")
        plt.bar(list(group_type_avr_rating_dict.keys()), list(group_type_avr_rating_dict.values()), align='center')
        plt.xticks(range(len(group_type_avr_rating_dict)), list(group_type_avr_rating_dict.keys()))
        plt.ylim(3, 5)
        plt.savefig('plots/Single/group_type_average_single_supporting_used.png')
        
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
        plt.savefig('plots/Single/group_type_average_all_box_single_supporting_used.png')
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
        plt.savefig('plots/Single/group_type_average_No_box_single_supporting_used.png')
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
        plt.savefig('plots/Single/group_type_average_partial_box_single_supporting_used.png')
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
        plt.savefig('plots/Single/group_type_average_full_box_single_supporting_used.png')
        # input("Yes")
        
        
        
        plt.clf()
        keys_list = ['N', 'R', 'I', 'RI']
        values_list = [(group_type_avr_rating_dict[x] + group_type_avr_rating_dict[y] + group_type_avr_rating_dict[z])/3 for x,y,z in zip(['G1', 'G2', 'G3', 'G4'],['G5', 'G6', 'G7', 'G8'],['G9', 'G10', 'G11', 'G12'])]
        plt.bar(keys_list, values_list, align='center')
        self.addlabels(keys_list, values_list)
        plt.xticks(range(len(values_list)), list(keys_list))
        plt.ylim(3, 5)
        plt.title("Average rating for final choices")
        plt.savefig('plots/Single/group_type_average_all_single_supporting_used.png')
        
        plt.clf()
        keys_list = ['N', 'R', 'I', 'RI']
        values_list = [group_type_avr_rating_dict[x] for x in ['G1', 'G2', 'G3', 'G4']]
        plt.bar(keys_list, values_list, align='center')
        self.addlabels(keys_list, values_list)
        plt.xticks(range(len(values_list)), list(keys_list))
        plt.ylim(3, 5)
        plt.title("Average rating for groups with no information")
        plt.savefig('plots/Single/group_type_average_l1_single_supporting_used.png')
        
        plt.clf()
        keys_list = ['N', 'R', 'I', 'RI']
        values_list = [group_type_avr_rating_dict[x] for x in ['G5', 'G6', 'G7', 'G8']]
        plt.bar(keys_list, values_list, align='center')
        self.addlabels(keys_list, values_list)
        plt.xticks(range(len(values_list)), list(keys_list))
        plt.ylim(3, 5)
        plt.title("Average rating for groups with partial information")
        plt.savefig('plots/Single/group_type_average_l2_single_supporting_used.png')
        
        plt.clf()
        keys_list = ['N', 'R', 'I', 'RI']
        values_list = [group_type_avr_rating_dict[x] for x in ['G9', 'G10', 'G11', 'G12']]
        plt.bar(keys_list, values_list, align='center')
        self.addlabels(keys_list, values_list)
        plt.xticks(range(len(values_list)), list(keys_list))
        plt.ylim(3, 5)
        plt.title("Average rating for groups with full information")
        plt.savefig('plots/Single/group_type_average_l3_single_supporting_used.png')
    
    def get_rating_scors_graph(self):
        tripScore = {1: 4,2: 4.5,3: 4,4: 4,5: 4,6: 4,7: 4.5,8: 3.5,9: 3,10: 4.5,11: 4.5,12: 4.5,13: 4.5,15: 4.5,16: 4.5,17: 4,18: 5,19: 4,20: 4,21: 2,22: 4.5,23: 4,24: 4.5,25: 4,26: 4.5,27: 3.5,28: 4.5,29: 3.5,30: 5,31: 4.5,32: 5}
        
        group_type_rating_dict = {'G1':list(), 'G2':list(), 'G3':list(), 'G4':list(), 'G5':list(), 'G6':list(), 'G7':list(), 'G8':list(), 'G9':list(), 'G10':list(), 'G11':list(), 'G12':list()}
        group_type_fit_dict = {'G1':list(), 'G2':list(), 'G3':list(), 'G4':list(), 'G5':list(), 'G6':list(), 'G7':list(), 'G8':list(), 'G9':list(), 'G10':list(), 'G11':list(), 'G12':list()}
        group_type_sim_dict = {'G1':list(), 'G2':list(), 'G3':list(), 'G4':list(), 'G5':list(), 'G6':list(), 'G7':list(), 'G8':list(), 'G9':list(), 'G10':list(), 'G11':list(), 'G12':list()}
        group_type_price_dict = {'G1':list(), 'G2':list(), 'G3':list(), 'G4':list(), 'G5':list(), 'G6':list(), 'G7':list(), 'G8':list(), 'G9':list(), 'G10':list(), 'G11':list(), 'G12':list()}
        group_type_diversity_dict = {'G1':list(), 'G2':list(), 'G3':list(), 'G4':list(), 'G5':list(), 'G6':list(), 'G7':list(), 'G8':list(), 'G9':list(), 'G10':list(), 'G11':list(), 'G12':list()}
        group_type_popularity_dict = {'G1':list(), 'G2':list(), 'G3':list(), 'G4':list(), 'G5':list(), 'G6':list(), 'G7':list(), 'G8':list(), 'G9':list(), 'G10':list(), 'G11':list(), 'G12':list()}
        trip_score_dict = {'G1':list(), 'G2':list(), 'G3':list(), 'G4':list(), 'G5':list(), 'G6':list(), 'G7':list(), 'G8':list(), 'G9':list(), 'G10':list(), 'G11':list(), 'G12':list()}
        
        df_groups_type = pd.read_csv("OutPuts/group_organizer_type_single.csv").drop_duplicates(subset=['organizer'])
        df_group_scores = pd.read_csv("OutPuts/1_df_groups_ratings_with_trip_score_single.csv")
        for index, row in df_groups_type.iterrows():
            organizer = row['organizer']
            group_type = row['type']
            price_flag = True
            diversity_flag = True
            popularity_flag = True
            fitness_flag = True
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
                            df_rating = df_group_scores.loc[(df_group_scores['user_id'] == member) & (df_group_scores['organizer_id'] == organizer) & (df_group_scores['rest_id'] == restaurant)]
                            if len(df_rating['rating'].values) != 0:
                                group_type_rating_dict[group_type].append(df_rating['rating'].values[-1])
                            df_scores = df_group_scores.loc[(df_group_scores['user_id'] == member) & (df_group_scores['rest_id'] == restaurant)]
                            if len(df_scores['price'].values) != 0 and price_flag:
                                group_type_price_dict[group_type].append(df_scores['price'].values[-1])
                                price_flag = False
                            if len(df_scores['diversity'].values) != 0 and diversity_flag:
                                group_type_diversity_dict[group_type].append(df_scores['diversity'].values[-1])
                                diversity_flag = False
                            if len(df_scores['popularity'].values) != 0 and popularity_flag:
                                group_type_popularity_dict[group_type].append(df_scores['popularity'].values[-1])
                                popularity_flag = False
                            if len(df_scores.loc[df_group_scores['organizer_id'] == organizer]['fitness'].values) != 0 and df_scores.loc[df_group_scores['organizer_id'] == organizer]['fitness'].values[-1] > -1 and fitness_flag:
                                group_type_fit_dict[group_type].append(df_scores.loc[df_group_scores['organizer_id'] == organizer]['fitness'].values[-1])
                            if len(df_scores.loc[df_group_scores['organizer_id'] == organizer]['sim'].values) != 0 and df_scores.loc[df_group_scores['organizer_id'] == organizer]['sim'].values[-1] > -1 and fitness_flag:
                                group_type_sim_dict[group_type].append(df_scores.loc[df_group_scores['organizer_id'] == organizer]['sim'].values[-1])
                                # if (df_scores['fitness'].values[0] == 0):
                                #     print(df_scores['fitness'])
                                #     print(group_type,organizer)
                                #     input()
                                fitness_flag = False
                            trip_score_dict[group_type].append(tripScore[restaurant])

        N_list_fit = list()
        R_list_fit = list()
        I_list_fit = list()
        RI_list_fit = list()
        N_list_sim = list()
        R_list_sim = list()
        I_list_sim = list()
        RI_list_sim = list()
        N_list_rating = list()
        R_list_rating = list()
        I_list_rating = list()
        RI_list_rating = list()
        N_list_trip_rating = list()
        R_list_trip_rating = list()
        I_list_trip_rating = list()
        RI_list_trip_rating = list()
        N_list_price = list()
        R_list_price = list()
        I_list_price = list()
        RI_list_price = list()
        N_list_diversity = list()
        R_list_diversity = list()
        I_list_diversity = list()
        RI_list_diversity = list()
        N_list_popularity = list()
        R_list_popularity = list()
        I_list_popularity = list()
        RI_list_popularity = list()
        for key in group_type_rating_dict.keys():
            if len(group_type_rating_dict[key]) > 0:
                if key in {'G1', 'G5', 'G9'}:
                    N_list_rating .extend(group_type_rating_dict[key])
                if key in {'G2', 'G6', 'G10'}:
                    R_list_rating .extend(group_type_rating_dict[key])
                if key in {'G3', 'G7', 'G11'}:
                    I_list_rating .extend(group_type_rating_dict[key])
                if key in {'G4', 'G8', 'G12'}:
                    RI_list_rating .extend(group_type_rating_dict[key])
            if len(trip_score_dict[key]) > 0:
                if key in {'G1', 'G5', 'G9'}:
                    N_list_trip_rating .extend(trip_score_dict[key])
                if key in {'G2', 'G6', 'G10'}:
                    R_list_trip_rating .extend(trip_score_dict[key])
                if key in {'G3', 'G7', 'G11'}:
                    I_list_trip_rating .extend(trip_score_dict[key])
                if key in {'G4', 'G8', 'G12'}:
                    RI_list_trip_rating .extend(trip_score_dict[key])
            if len(group_type_price_dict[key]) > 0:
                if key in {'G1', 'G5', 'G9'}:
                    N_list_price.extend(group_type_price_dict[key])
                if key in {'G2', 'G6', 'G10'}:
                    R_list_price.extend(group_type_price_dict[key])
                if key in {'G3', 'G7', 'G11'}:
                    I_list_price.extend(group_type_price_dict[key])
                if key in {'G4', 'G8', 'G12'}:
                    RI_list_price.extend(group_type_price_dict[key])
            if len(group_type_diversity_dict[key]) > 0:
                if key in {'G1', 'G5', 'G9'}:
                    N_list_diversity.extend(group_type_diversity_dict[key])
                if key in {'G2', 'G6', 'G10'}:
                    R_list_diversity.extend(group_type_diversity_dict[key])
                if key in {'G3', 'G7', 'G11'}:
                    I_list_diversity.extend(group_type_diversity_dict[key])
                if key in {'G4', 'G8', 'G12'}:
                    RI_list_diversity.extend(group_type_diversity_dict[key])
            if len(group_type_popularity_dict[key]) > 0:
                if key in {'G1', 'G5', 'G9'}:
                    N_list_popularity.extend(group_type_popularity_dict[key])
                if key in {'G2', 'G6', 'G10'}:
                    R_list_popularity.extend(group_type_popularity_dict[key])
                if key in {'G3', 'G7', 'G11'}:
                    I_list_popularity.extend(group_type_popularity_dict[key])
                if key in {'G4', 'G8', 'G12'}:
                    RI_list_popularity.extend(group_type_popularity_dict[key])
            if len(group_type_fit_dict[key]) > 0:
                if key in {'G1', 'G5', 'G9'}:
                    N_list_fit.extend(group_type_fit_dict[key])
                if key in {'G2', 'G6', 'G10'}:
                    R_list_fit.extend(group_type_fit_dict[key])
                if key in {'G3', 'G7', 'G11'}:
                    I_list_fit.extend(group_type_fit_dict[key])
                if key in {'G4', 'G8', 'G12'}:
                    RI_list_fit.extend(group_type_fit_dict[key])
            if len(group_type_sim_dict[key]) > 0:
                if key in {'G1', 'G5', 'G9'}:
                    N_list_sim.extend(group_type_sim_dict[key])
                if key in {'G2', 'G6', 'G10'}:
                    R_list_sim.extend(group_type_sim_dict[key])
                if key in {'G3', 'G7', 'G11'}:
                    I_list_sim.extend(group_type_sim_dict[key])
                if key in {'G4', 'G8', 'G12'}:
                    RI_list_sim.extend(group_type_sim_dict[key])
        plt.clf()
        width = 0.15
        ind = np.arange(4) 
        bar1 = plt.bar(ind, [np.average(N_list_rating)/5, np.average(R_list_rating)/5, np.average(I_list_rating)/5, np.average(RI_list_rating)/5], width, color = 'r')
        bar2 = plt.bar(ind+width, [np.average(N_list_price)/3, np.average(R_list_price)/3, np.average(I_list_price)/3, np.average(RI_list_price)/3], width, color = 'g')
        bar3 = plt.bar(ind+2*width, [np.average(N_list_diversity)/10, np.average(R_list_diversity)/10, np.average(I_list_diversity)/10, np.average(RI_list_diversity)/10], width, color = 'b')
        bar4 = plt.bar(ind+3*width, [np.average(N_list_popularity)/5, np.average(R_list_popularity)/5, np.average(I_list_popularity)/5, np.average(RI_list_popularity)/5], width, color = 'm')
        bar5 = plt.bar(ind+4*width, [np.average(N_list_trip_rating)/5, np.average(R_list_trip_rating)/5, np.average(I_list_trip_rating)/5, np.average(RI_list_trip_rating)/5], width, color = 'y') 
        plt.xlabel("Scores")
        plt.ylabel('System Types')
        plt.title("Different scores")
        plt.xticks(np.arange(4)+(2*width),['N', 'R', 'I', 'RI'])
        plt.legend( (bar1, bar5, bar2, bar3, bar4), ('Rating', 'Trip Advisor', 'Price', 'Diversity', 'Popularity') )
        plt.ylim(0, 1)
        plt.savefig('plots/Single/group_type_average_scores_single.png')
        
        print('Rating', np.average(N_list_rating),np.average(R_list_rating),np.average(I_list_rating),np.average(RI_list_rating))
        print("N VS. R",mannwhitneyu(N_list_rating, R_list_rating, alternative='less'))
        print("N VS. I",mannwhitneyu(N_list_rating, I_list_rating, alternative='less'))
        print("N VS. RI",mannwhitneyu(N_list_rating, RI_list_rating, alternative='less'))
        print("R VS. I",mannwhitneyu(R_list_rating, I_list_rating, alternative='less'))
        print("R VS. RI",mannwhitneyu(R_list_rating, RI_list_rating, alternative='less'))
        print("I VS. RI",mannwhitneyu(I_list_rating, RI_list_rating, alternative='less'))
        print("ANOVA")
        print(stats.f_oneway(N_list_rating,R_list_rating,I_list_rating,RI_list_rating))
        print('Price', np.average(N_list_price),np.average(R_list_price),np.average(I_list_price),np.average(RI_list_price))
        print("N VS. R",mannwhitneyu(N_list_price, R_list_price, alternative='greater'))
        print("N VS. I",mannwhitneyu(N_list_price, I_list_price, alternative='greater'))
        print("N VS. RI",mannwhitneyu(N_list_price, RI_list_price, alternative='greater'))
        print("R VS. I",mannwhitneyu(R_list_price, I_list_price, alternative='greater'))
        print("R VS. RI",mannwhitneyu(R_list_price, RI_list_price, alternative='greater'))
        print("I VS. RI",mannwhitneyu(I_list_price, RI_list_price, alternative='greater'))
        print("ANOVA")
        print(stats.f_oneway(N_list_price,R_list_price,I_list_price,RI_list_price))
        print('Diversity', np.average(N_list_diversity),np.average(R_list_diversity),np.average(I_list_diversity),np.average(RI_list_diversity))
        print("N VS. R",mannwhitneyu(N_list_diversity, R_list_diversity, alternative='less'))
        print("N VS. I",mannwhitneyu(N_list_diversity, I_list_diversity, alternative='less'))
        print("N VS. RI",mannwhitneyu(N_list_diversity, RI_list_diversity, alternative='less'))
        print("R VS. I",mannwhitneyu(R_list_diversity, I_list_diversity, alternative='less'))
        print("R VS. RI",mannwhitneyu(R_list_diversity, RI_list_diversity, alternative='less'))
        print("I VS. RI",mannwhitneyu(I_list_diversity, RI_list_diversity, alternative='less'))
        print("ANOVA")
        print(stats.f_oneway(N_list_diversity,R_list_diversity,I_list_diversity,RI_list_diversity))
        print('Popularity', np.average(N_list_popularity),np.average(R_list_popularity),np.average(I_list_popularity),np.average(RI_list_popularity))
        print("N VS. R",mannwhitneyu(N_list_popularity, R_list_popularity, alternative='less'))
        print("N VS. I",mannwhitneyu(N_list_popularity, I_list_popularity, alternative='less'))
        print("N VS. RI",mannwhitneyu(N_list_popularity, RI_list_popularity, alternative='less'))
        print("R VS. I",mannwhitneyu(R_list_popularity, I_list_popularity, alternative='less'))
        print("R VS. RI",mannwhitneyu(R_list_popularity, RI_list_popularity, alternative='less'))
        print("I VS. RI",mannwhitneyu(I_list_popularity, RI_list_popularity, alternative='less'))
        print("ANOVA")
        print(stats.f_oneway(N_list_popularity,R_list_popularity,I_list_popularity,RI_list_popularity))
        print('Trip Score', np.average(N_list_trip_rating),np.average(R_list_trip_rating),np.average(I_list_trip_rating),np.average(RI_list_trip_rating))
        print("N VS. R",mannwhitneyu(N_list_trip_rating, R_list_trip_rating, alternative='less'))
        print("N VS. I",mannwhitneyu(N_list_trip_rating, I_list_trip_rating, alternative='less'))
        print("N VS. RI",mannwhitneyu(N_list_trip_rating, RI_list_trip_rating, alternative='less'))
        print("R VS. I",mannwhitneyu(R_list_trip_rating, I_list_trip_rating, alternative='less'))
        print("R VS. RI",mannwhitneyu(R_list_trip_rating, RI_list_trip_rating, alternative='less'))
        print("I VS. RI",mannwhitneyu(I_list_trip_rating, RI_list_trip_rating, alternative='less'))
        print("ANOVA")
        print(stats.f_oneway(N_list_trip_rating,R_list_trip_rating,I_list_trip_rating,RI_list_trip_rating))
        print('Fitness score', np.average(N_list_fit),np.average(R_list_fit),np.average(I_list_fit),np.average(RI_list_fit))
        print("N VS. R",mannwhitneyu(N_list_fit, R_list_fit, alternative='less'))
        print("N VS. I",mannwhitneyu(N_list_fit, I_list_fit, alternative='less'))
        print("N VS. RI",mannwhitneyu(N_list_fit, RI_list_fit, alternative='less'))
        print("R VS. I",mannwhitneyu(R_list_fit, I_list_fit, alternative='less'))
        print("R VS. RI",mannwhitneyu(R_list_fit, RI_list_fit, alternative='less'))
        print("I VS. RI",mannwhitneyu(I_list_fit, RI_list_fit, alternative='less'))
        print("ANOVA")
        print(stats.f_oneway(N_list_fit,R_list_fit,I_list_fit,RI_list_fit))
        print('Sim score', np.average(N_list_sim),np.average(R_list_sim),np.average(I_list_sim),np.average(RI_list_sim))
        print("N VS. R",mannwhitneyu(N_list_sim, R_list_sim, alternative='less'))
        print("N VS. I",mannwhitneyu(N_list_sim, I_list_sim, alternative='less'))
        print("N VS. RI",mannwhitneyu(N_list_sim, RI_list_sim, alternative='less'))
        print("R VS. I",mannwhitneyu(R_list_sim, I_list_sim, alternative='less'))
        print("R VS. RI",mannwhitneyu(R_list_sim, RI_list_sim, alternative='less'))
        print("I VS. RI",mannwhitneyu(I_list_sim, I_list_sim, alternative='less'))
        print("ANOVA")
        print(stats.f_oneway(N_list_sim,R_list_sim,I_list_sim,I_list_sim))
        
    def group_member_size(self):
        df1 = pd.read_csv("OutPuts/Revised/df_individual_loss_with_trip_score_single.csv")
        # df2 = pd.read_csv("OutPuts/Revised/df_individual_loss_with_trip_score_single.csv")
        # print([x for x in df1['organizer_id'].unique() if x not in df2['organizer_id'].unique()])
        print(df1['user_id'].nunique())
        
    def get_group_number(self):
        Revised_df_list = pd.read_csv("OutPuts/Selected_first.csv")['user_id'].unique()
        df = pd.read_csv("OutPuts/Revised/groups_members_single.csv").drop_duplicates(['member1'])
        df_group_scores = pd.read_csv("OutPuts/Revised/df_individual_loss_with_trip_score_single.csv")
        filtered_df = df[df.isin(Revised_df_list).any(axis=1)]
        # print((filtered_df))
        print(((df_group_scores['system_type'] == 'I')).sum())

        
        
        
        
         
                            