import csv
from typing import get_type_hints
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
from Explanations import Explanations
from datetime import datetime

class Evaluations(object):
    
    def __init__(self,connection_mysql):
        self.mysql_conn = connection_mysql
    
    def sorting_type_frequency(self):
        group_type_rating_dict = {'G1':list(), 'G2':list(), 'G3':list(), 'G4':list(), 'G5':list(), 'G6':list(), 'G7':list(), 'G8':list(), 'G9':list(), 'G10':list(), 'G11':list(), 'G12':list()}
        group_type_counter_dict = {'G1':0, 'G2':0, 'G3':0, 'G4':0, 'G5':0, 'G6':0, 'G7':0, 'G8':0, 'G9':0, 'G10':0, 'G11':0, 'G12':0}
        df_groups_type = pd.read_csv("OutPuts/group_organizer_type.csv")
        df_group_sorting = pd.read_csv("OutPuts/organizer_sorting.csv")  
        pop_list = [0,0,0,0,0,0,0,0,0,0,0,0]
        fit_list = [0,0,0,0,0,0,0,0,0,0,0,0]
        sim_list = [0,0,0,0,0,0,0,0,0,0,0,0]
        group_with_choice = self.get_groups_with_choice()
        for index, row in df_groups_type.iterrows():
            organizer = row['organizer']
            group_type = row['type']
            df_organizer_sorting_pop = df_group_sorting.loc[(df_group_sorting['type'] == 'pop') & (df_group_sorting['user_id'] == organizer) & (df_group_sorting['group_id'].isin(group_with_choice))]
            df_organizer_sorting_fit = df_group_sorting.loc[(df_group_sorting['type'] == 'fit') & (df_group_sorting['user_id'] == organizer) & (df_group_sorting['group_id'].isin(group_with_choice))]
            df_organizer_sorting_sim = df_group_sorting.loc[(df_group_sorting['type'] == 'sim') & (df_group_sorting['user_id'] == organizer) & (df_group_sorting['group_id'].isin(group_with_choice))]
            temp_list = [len(df_organizer_sorting_pop),len(df_organizer_sorting_fit), len(df_organizer_sorting_sim)]
            if len(group_type_rating_dict[group_type]) == 0:
                group_type_rating_dict[group_type] = temp_list
            else:
                group_type_rating_dict[group_type] += temp_list
            group_type_counter_dict[group_type] += 1
            if len(df_organizer_sorting_pop) - 1 > 0:
                pop_list[list(group_type_counter_dict.keys()).index(group_type)] += (len(df_organizer_sorting_pop) - 1)
            fit_list[list(group_type_counter_dict.keys()).index(group_type)] += len(df_organizer_sorting_fit)
            sim_list[list(group_type_counter_dict.keys()).index(group_type)] += len(df_organizer_sorting_sim)
        width = 0.25
        ind = np.arange(len(pop_list)) 
        bar1 = plt.bar(ind-0.25, [int(b) / int(m) for b,m in zip(pop_list, list(group_type_counter_dict.values()))], width, color = 'r')
        bar2 = plt.bar(ind, [int(b) / int(m) for b,m in zip(fit_list, list(group_type_counter_dict.values()))], width, color='g')
        bar3 = plt.bar(ind+0.25, [int(b) / int(m) for b,m in zip(sim_list, list(group_type_counter_dict.values()))], width, color = 'b')
        N = 3
        ind = np.arange(N) 
        plt.xlabel("Frequency")
        plt.ylabel('Group Types')
        plt.title("Group Type Frequence")
        plt.xticks(np.arange(12),list(group_type_counter_dict.keys()))
        plt.legend( (bar1, bar2, bar3), ('Popularity', 'Fitness', 'Similarity') )
        plt.savefig('plots/sorting_frequency_average.png')
        
        plt.clf()
        width = 0.25
        ind = np.arange(4) 
        bar1 = plt.bar(ind-0.25, [int(b) / int(m) for b,m in zip(pop_list, list(group_type_counter_dict.values()))][0:4], width, color = 'r')
        bar2 = plt.bar(ind, [int(b) / int(m) for b,m in zip(fit_list, list(group_type_counter_dict.values()))][0:4], width, color='g')
        bar3 = plt.bar(ind+0.25, [int(b) / int(m) for b,m in zip(sim_list, list(group_type_counter_dict.values()))][0:4], width, color = 'b')
        N = 3
        ind = np.arange(N) 
        plt.xlabel("Frequency")
        plt.ylabel('Group Types')
        plt.title("Group Type Frequence")
        plt.xticks(np.arange(4),list(group_type_counter_dict.keys())[0:4])
        plt.legend( (bar1, bar2, bar3), ('Popularity', 'Fitness', 'Similarity') )
        plt.savefig('plots/sorting_frequency_average_l1.png')
        
        plt.clf()
        width = 0.25
        ind = np.arange(4) 
        bar1 = plt.bar(ind-0.25, [int(b) / int(m) for b,m in zip(pop_list, list(group_type_counter_dict.values()))][4:8], width, color = 'r')
        bar2 = plt.bar(ind, [int(b) / int(m) for b,m in zip(fit_list, list(group_type_counter_dict.values()))][4:8], width, color='g')
        bar3 = plt.bar(ind+0.25, [int(b) / int(m) for b,m in zip(sim_list, list(group_type_counter_dict.values()))][4:8], width, color = 'b')
        N = 3
        ind = np.arange(N) 
        plt.xlabel("Frequency")
        plt.ylabel('Group Types')
        plt.title("Group Type Frequence")
        plt.xticks(np.arange(4),list(group_type_counter_dict.keys())[4:8])
        plt.legend( (bar1, bar2, bar3), ('Popularity', 'Fitness', 'Similarity') )
        plt.savefig('plots/sorting_frequency_average_l2.png')
        
        plt.clf()
        width = 0.25
        ind = np.arange(4) 
        bar1 = plt.bar(ind-0.25, [int(b) / int(m) for b,m in zip(pop_list, list(group_type_counter_dict.values()))][8:12], width, color = 'r')
        bar2 = plt.bar(ind, [int(b) / int(m) for b,m in zip(fit_list, list(group_type_counter_dict.values()))][8:12], width, color='g')
        bar3 = plt.bar(ind+0.25, [int(b) / int(m) for b,m in zip(sim_list, list(group_type_counter_dict.values()))][8:12], width, color = 'b')
        N = 3
        ind = np.arange(N) 
        plt.xlabel("Frequency")
        plt.ylabel('Group Types')
        plt.title("Group Type Frequence")
        plt.xticks(np.arange(4),list(group_type_counter_dict.keys())[8:12])
        plt.legend( (bar1, bar2, bar3), ('Popularity', 'Fitness', 'Similarity') )
        plt.savefig('plots/sorting_frequency_average_l3.png')
               
    def sorting_type_frequency_sized(self):
        group_type_rating_dict = {'G1':list(), 'G2':list(), 'G3':list(), 'G4':list(), 'G5':list(), 'G6':list(), 'G7':list(), 'G8':list(), 'G9':list(), 'G10':list(), 'G11':list(), 'G12':list()}
        group_type_counter_dict = {'G1':0, 'G2':0, 'G3':0, 'G4':0, 'G5':0, 'G6':0, 'G7':0, 'G8':0, 'G9':0, 'G10':0, 'G11':0, 'G12':0}
        df_groups_type = pd.read_csv("OutPuts/group_organizer_type.csv")
        df_group_sorting = pd.read_csv("OutPuts/organizer_sorting.csv")  
        pop_list = [0,0,0,0,0,0,0,0,0,0,0,0]
        fit_list = [0,0,0,0,0,0,0,0,0,0,0,0]
        sim_list = [0,0,0,0,0,0,0,0,0,0,0,0]
        group_with_choice = self.get_groups_with_choice()
        for index, row in df_groups_type.iterrows():
            organizer = row['organizer']
            group_type = row['type']
            df_organizer_sorting_pop = df_group_sorting.loc[(df_group_sorting['type'] == 'pop') & (df_group_sorting['user_id'] == organizer) & (df_group_sorting['group_id'].isin(group_with_choice))]
            df_organizer_sorting_fit = df_group_sorting.loc[(df_group_sorting['type'] == 'fit') & (df_group_sorting['user_id'] == organizer) & (df_group_sorting['group_id'].isin(group_with_choice))]
            df_organizer_sorting_sim = df_group_sorting.loc[(df_group_sorting['type'] == 'sim') & (df_group_sorting['user_id'] == organizer) & (df_group_sorting['group_id'].isin(group_with_choice))]
            temp_list = [len(df_organizer_sorting_pop),len(df_organizer_sorting_fit), len(df_organizer_sorting_sim)]
            if len(group_type_rating_dict[group_type]) == 0:
                group_type_rating_dict[group_type] = temp_list
            else:
                group_type_rating_dict[group_type] += temp_list
            group_type_counter_dict[group_type] += 1
            if len(df_organizer_sorting_pop) - 1 > 0:
                pop_list[list(group_type_counter_dict.keys()).index(group_type)] += (len(df_organizer_sorting_pop) - 1)
            fit_list[list(group_type_counter_dict.keys()).index(group_type)] += len(df_organizer_sorting_fit)
            sim_list[list(group_type_counter_dict.keys()).index(group_type)] += len(df_organizer_sorting_sim)
        width = 0.25
        ind = np.arange(len(pop_list)) 
        bar1 = plt.bar(ind-0.25, [int(b) / int(m) for b,m in zip(pop_list, list(group_type_counter_dict.values()))], width, color = 'r')
        bar2 = plt.bar(ind, [int(b) / int(m) for b,m in zip(fit_list, list(group_type_counter_dict.values()))], width, color='g')
        bar3 = plt.bar(ind+0.25, [int(b) / int(m) for b,m in zip(sim_list, list(group_type_counter_dict.values()))], width, color = 'b')
        N = 3
        ind = np.arange(N) 
        plt.xlabel("Frequency")
        plt.ylabel('Group Types')
        plt.title("Group Type Frequence")
        plt.xticks(np.arange(12),list(group_type_counter_dict.keys()))
        plt.legend( (bar1, bar2, bar3), ('Popularity', 'Fitness', 'Similarity') )
        plt.savefig('plots/sorting_frequency_average.png')
        
    def get_groups_with_choice(self):
        choice_set = set()
        query = "SELECT group_id FROM selected"
        my_cursor = self.mysql_conn.cursor(buffered=True)
        my_cursor.execute(query)
        for group in my_cursor:
            choice_set.add(group[0])
        return choice_set
            
    def sorting_type_last(self):
        group_type_rating_dict = {'G1':list(), 'G2':list(), 'G3':list(), 'G4':list(), 'G5':list(), 'G6':list(), 'G7':list(), 'G8':list(), 'G9':list(), 'G10':list(), 'G11':list(), 'G12':list()}
        group_type_counter_dict = {'G1':1, 'G2':1, 'G3':1, 'G4':1, 'G5':1, 'G6':1, 'G7':1, 'G8':1, 'G9':1, 'G10':1, 'G11':1, 'G12':1}
        df_groups_type = pd.read_csv("OutPuts/group_organizer_type.csv")
        df_group_sorting = pd.read_csv("OutPuts/organizer_sorting.csv")  
        pop_list = [0,0,0,0,0,0,0,0,0,0,0,0]
        fit_list = [0,0,0,0,0,0,0,0,0,0,0,0]
        sim_list = [0,0,0,0,0,0,0,0,0,0,0,0]
        for index, row in df_group_sorting.iterrows():
            df_group_sorting.iloc[index, df_group_sorting.columns.get_loc('time')] = pd.to_datetime(df_group_sorting.iloc[index, df_group_sorting.columns.get_loc('time')],format="%Y-%m-%d %H:%M:%S")
        group_with_choice = self.get_groups_with_choice()
        for index, row in df_groups_type.iterrows():
            organizer = row['organizer']
            group_type = row['type']
            df_group_sorting.to_csv('OutPuts/check.csv')
            df_time_max = df_group_sorting.loc[(df_group_sorting['user_id'] == organizer)  & (df_group_sorting['group_id'].isin(group_with_choice)), 'time'].values
            df_organizer_sorting_pop = df_group_sorting.loc[(df_group_sorting['type'] == 'pop') & (df_group_sorting['user_id'] == organizer)  & (df_group_sorting['group_id'].isin(group_with_choice))]
            if not len(df_time_max):
                continue
            df_organizer_sorting_pop = df_organizer_sorting_pop.loc[(df_organizer_sorting_pop.time == df_time_max[-1])]
            df_organizer_sorting_fit = df_group_sorting.loc[(df_group_sorting['type'] == 'fit') & (df_group_sorting['user_id'] == organizer) & (df_group_sorting['group_id'].isin(group_with_choice))]
            df_organizer_sorting_fit = df_organizer_sorting_fit.loc[(df_organizer_sorting_fit.time == df_time_max[-1])]
            df_organizer_sorting_sim = df_group_sorting.loc[(df_group_sorting['type'] == 'sim') & (df_group_sorting['user_id'] == organizer) & (df_group_sorting['group_id'].isin(group_with_choice))]
            df_organizer_sorting_sim = df_organizer_sorting_sim.loc[(df_organizer_sorting_sim.time == df_time_max[-1])]
            temp_list = [len(df_organizer_sorting_pop),len(df_organizer_sorting_fit), len(df_organizer_sorting_sim)]
            if len(group_type_rating_dict[group_type]) == 0:
                group_type_rating_dict[group_type] = temp_list
            else:
                group_type_rating_dict[group_type] += temp_list
            group_type_counter_dict[group_type] += 1
            pop_list[list(group_type_counter_dict.keys()).index(group_type)] += len(df_organizer_sorting_pop)
            fit_list[list(group_type_counter_dict.keys()).index(group_type)] += len(df_organizer_sorting_fit)
            sim_list[list(group_type_counter_dict.keys()).index(group_type)] += len(df_organizer_sorting_sim)
        width = 0.25
        ind = np.arange(len(pop_list)) 
        bar1 = plt.bar(ind-0.25, [int(b) / int(m) for b,m in zip(pop_list, list(group_type_counter_dict.values()))], width, color = 'r')
        bar2 = plt.bar(ind, [int(b) / int(m) for b,m in zip(fit_list, list(group_type_counter_dict.values()))], width, color='g')
        bar3 = plt.bar(ind+0.25, [int(b) / int(m) for b,m in zip(sim_list, list(group_type_counter_dict.values()))], width, color = 'b')
        N = 3
        ind = np.arange(N) 
        plt.xlabel("Frequency")
        plt.ylabel('Group Types')
        plt.title("Group Type Frequence")
        plt.xticks(np.arange(12)+width,list(group_type_counter_dict.keys()))
        plt.legend( (bar1, bar2, bar3), ('Popularity', 'Fitness', 'Similarity') )
        plt.savefig('plots/sorting_last.png')
        
        plt.clf()
        width = 0.25
        ind = np.arange(4) 
        bar1 = plt.bar(ind-0.25, [int(b) / int(m) for b,m in zip(pop_list, list(group_type_counter_dict.values()))][0:4], width, color = 'r')
        bar2 = plt.bar(ind, [int(b) / int(m) for b,m in zip(fit_list, list(group_type_counter_dict.values()))][0:4], width, color='g')
        bar3 = plt.bar(ind+0.25, [int(b) / int(m) for b,m in zip(sim_list, list(group_type_counter_dict.values()))][0:4], width, color = 'b')
        N = 3
        ind = np.arange(N) 
        plt.xlabel("Frequency")
        plt.ylabel('Group Types')
        plt.title("Group Type Frequence")
        plt.xticks(np.arange(4),list(group_type_counter_dict.keys())[0:4])
        plt.legend( (bar1, bar2, bar3), ('Popularity', 'Fitness', 'Similarity') )
        plt.savefig('plots/sorting_last_l1.png')
        
        plt.clf()
        width = 0.25
        ind = np.arange(4) 
        bar1 = plt.bar(ind-0.25, [int(b) / int(m) for b,m in zip(pop_list, list(group_type_counter_dict.values()))][4:8], width, color = 'r')
        bar2 = plt.bar(ind, [int(b) / int(m) for b,m in zip(fit_list, list(group_type_counter_dict.values()))][4:8], width, color='g')
        bar3 = plt.bar(ind+0.25, [int(b) / int(m) for b,m in zip(sim_list, list(group_type_counter_dict.values()))][4:8], width, color = 'b')
        N = 3
        ind = np.arange(N) 
        plt.xlabel("Frequency")
        plt.ylabel('Group Types')
        plt.title("Group Type Frequence")
        plt.xticks(np.arange(4),list(group_type_counter_dict.keys())[4:8])
        plt.legend( (bar1, bar2, bar3), ('Popularity', 'Fitness', 'Similarity') )
        plt.savefig('plots/sorting_last_l2.png')
        
        plt.clf()
        width = 0.25
        ind = np.arange(4) 
        bar1 = plt.bar(ind-0.25, [int(b) / int(m) for b,m in zip(pop_list, list(group_type_counter_dict.values()))][8:12], width, color = 'r')
        bar2 = plt.bar(ind, [int(b) / int(m) for b,m in zip(fit_list, list(group_type_counter_dict.values()))][8:12], width, color='g')
        bar3 = plt.bar(ind+0.25, [int(b) / int(m) for b,m in zip(sim_list, list(group_type_counter_dict.values()))][8:12], width, color = 'b')
        N = 3
        ind = np.arange(N) 
        plt.xlabel("Frequency")
        plt.ylabel('Group Types')
        plt.title("Group Type Frequence")
        plt.xticks(np.arange(4),list(group_type_counter_dict.keys())[8:12])
        plt.legend( (bar1, bar2, bar3), ('Popularity', 'Fitness', 'Similarity') )
        plt.savefig('plots/sorting_last_l3.png')
        
    def sorting_type_for_visited(self):
        group_type_rating_dict = {'G1':list(), 'G2':list(), 'G3':list(), 'G4':list(), 'G5':list(), 'G6':list(), 'G7':list(), 'G8':list(), 'G9':list(), 'G10':list(), 'G11':list(), 'G12':list()}
        group_type_counter_dict = {'G1':1, 'G2':1, 'G3':1, 'G4':1, 'G5':1, 'G6':1, 'G7':1, 'G8':1, 'G9':1, 'G10':1, 'G11':1, 'G12':1}
        df_groups_type = pd.read_csv("OutPuts/group_organizer_type.csv")
        df_group_sorting = pd.read_csv("OutPuts/organizer_visiting.csv")  
        pop_list = [0,0,0,0,0,0,0,0,0,0,0,0]
        fit_list = [0,0,0,0,0,0,0,0,0,0,0,0]
        sim_list = [0,0,0,0,0,0,0,0,0,0,0,0]
        
        for index, row in df_groups_type.iterrows():
            organizer = row['organizer']
            group_type = row['type']
            df_organizer_sorting_pop = df_group_sorting.loc[(df_group_sorting['sort_pop'] == 1) & (df_group_sorting['user_id'] == organizer)]
            df_organizer_sorting_fit = df_group_sorting.loc[(df_group_sorting['sort_fit'] == 1) & (df_group_sorting['user_id'] == organizer)]
            df_organizer_sorting_sim = df_group_sorting.loc[(df_group_sorting['sort_sim'] == 1) & (df_group_sorting['user_id'] == organizer)]
            temp_list = [len(df_organizer_sorting_pop),len(df_organizer_sorting_fit), len(df_organizer_sorting_sim)]
            if len(group_type_rating_dict[group_type]) == 0:
                group_type_rating_dict[group_type] = temp_list
            else:
                group_type_rating_dict[group_type] += temp_list
            group_type_counter_dict[group_type] += 1
            pop_list[list(group_type_counter_dict.keys()).index(group_type)] += len(df_organizer_sorting_pop)
            fit_list[list(group_type_counter_dict.keys()).index(group_type)] += len(df_organizer_sorting_fit)
            sim_list[list(group_type_counter_dict.keys()).index(group_type)] += len(df_organizer_sorting_sim)

        width = 0.25
        ind = np.arange(len(pop_list)) 
        bar1 = plt.bar(ind-width, [int(b) / int(m) for b,m in zip(pop_list, list(group_type_counter_dict.values()))], width, color = 'r')
        bar2 = plt.bar(ind, [int(b) / int(m) for b,m in zip(fit_list, list(group_type_counter_dict.values()))], width, color='g')
        bar3 = plt.bar(ind+width, [int(b) / int(m) for b,m in zip(sim_list, list(group_type_counter_dict.values()))], width, color = 'b')
        N = 3
        ind = np.arange(N) 
        plt.xlabel("Frequency")
        plt.ylabel('Group Types')
        plt.title("Group Type Frequence")
        plt.xticks(np.arange(12)+width,list(group_type_counter_dict.keys()))
        plt.legend( (bar1, bar2, bar3), ('Popularity', 'Fitness', 'Similarity') )
        plt.savefig('plots/sorting_visited.png')
        
        plt.clf()
        width = 0.25
        ind = np.arange(4) 
        bar1 = plt.bar(ind-0.25, [int(b) / int(m) for b,m in zip(pop_list, list(group_type_counter_dict.values()))][0:4], width, color = 'r')
        bar2 = plt.bar(ind, [int(b) / int(m) for b,m in zip(fit_list, list(group_type_counter_dict.values()))][0:4], width, color='g')
        bar3 = plt.bar(ind+0.25, [int(b) / int(m) for b,m in zip(sim_list, list(group_type_counter_dict.values()))][0:4], width, color = 'b')
        N = 3
        ind = np.arange(N) 
        plt.xlabel("Frequency")
        plt.ylabel('Group Types')
        plt.title("Group Type Frequence")
        plt.xticks(np.arange(4),list(group_type_counter_dict.keys())[0:4])
        plt.legend( (bar1, bar2, bar3), ('Popularity', 'Fitness', 'Similarity') )
        plt.savefig('plots/sorting_visited_l1.png')
        
        plt.clf()
        width = 0.25
        ind = np.arange(4) 
        bar1 = plt.bar(ind-0.25, [int(b) / int(m) for b,m in zip(pop_list, list(group_type_counter_dict.values()))][4:8], width, color = 'r')
        bar2 = plt.bar(ind, [int(b) / int(m) for b,m in zip(fit_list, list(group_type_counter_dict.values()))][4:8], width, color='g')
        bar3 = plt.bar(ind+0.25, [int(b) / int(m) for b,m in zip(sim_list, list(group_type_counter_dict.values()))][4:8], width, color = 'b')
        N = 3
        ind = np.arange(N) 
        plt.xlabel("Frequency")
        plt.ylabel('Group Types')
        plt.title("Group Type Frequence")
        plt.xticks(np.arange(4),list(group_type_counter_dict.keys())[4:8])
        plt.legend( (bar1, bar2, bar3), ('Popularity', 'Fitness', 'Similarity') )
        plt.savefig('plots/sorting_visited_l2.png')
        
        plt.clf()
        width = 0.25
        ind = np.arange(4) 
        bar1 = plt.bar(ind-0.25, [int(b) / int(m) for b,m in zip(pop_list, list(group_type_counter_dict.values()))][8:12], width, color = 'r')
        bar2 = plt.bar(ind, [int(b) / int(m) for b,m in zip(fit_list, list(group_type_counter_dict.values()))][8:12], width, color='g')
        bar3 = plt.bar(ind+0.25, [int(b) / int(m) for b,m in zip(sim_list, list(group_type_counter_dict.values()))][8:12], width, color = 'b')
        N = 3
        ind = np.arange(N) 
        plt.xlabel("Frequency")
        plt.ylabel('Group Types')
        plt.title("Group Type Frequence")
        plt.xticks(np.arange(4),list(group_type_counter_dict.keys())[8:12])
        plt.legend( (bar1, bar2, bar3), ('Popularity', 'Fitness', 'Similarity') )
        plt.savefig('plots/sorting_visited_l3.png')
            
    def sorting_type_for_booked(self):
        group_type_rating_dict = {'G1':list(), 'G2':list(), 'G3':list(), 'G4':list(), 'G5':list(), 'G6':list(), 'G7':list(), 'G8':list(), 'G9':list(), 'G10':list(), 'G11':list(), 'G12':list()}
        group_type_counter_dict = {'G1':1, 'G2':1, 'G3':1, 'G4':1, 'G5':1, 'G6':1, 'G7':1, 'G8':1, 'G9':1, 'G10':1, 'G11':1, 'G12':1}
        df_groups_type = pd.read_csv("OutPuts/group_organizer_type.csv")
        df_group_sorting = pd.read_csv("OutPuts/organizer_booked.csv")  
        pop_list = [0,0,0,0,0,0,0,0,0,0,0,0]
        fit_list = [0,0,0,0,0,0,0,0,0,0,0,0]
        sim_list = [0,0,0,0,0,0,0,0,0,0,0,0]
        counter_list_pop = [0,0,0,0,0,0,0,0,0,0,0,0]
        counter_list_fit = [0,0,0,0,0,0,0,0,0,0,0,0]
        counter_list_sim = [0,0,0,0,0,0,0,0,0,0,0,0]
      
        for index, row in df_groups_type.iterrows():
            organizer = row['organizer']
            group_type = row['type']
            df_organizer_sorting_pop = df_group_sorting.loc[(df_group_sorting['sort_pop'] == 1) & (df_group_sorting['user_id'] == organizer)]
            df_organizer_sorting_fit = df_group_sorting.loc[(df_group_sorting['sort_fit'] == 1) & (df_group_sorting['user_id'] == organizer)]
            df_organizer_sorting_sim = df_group_sorting.loc[(df_group_sorting['sort_sim'] == 1) & (df_group_sorting['user_id'] == organizer)]
            temp_list = [len(df_organizer_sorting_pop),len(df_organizer_sorting_fit), len(df_organizer_sorting_sim)]
            if len(group_type_rating_dict[group_type]) == 0:
                group_type_rating_dict[group_type] = temp_list
            else:
                group_type_rating_dict[group_type] += temp_list
            group_type_counter_dict[group_type] += 1
            counter_list_pop[list(group_type_counter_dict.keys()).index(group_type)] += len(df_organizer_sorting_pop)
            counter_list_fit[list(group_type_counter_dict.keys()).index(group_type)] += len(df_organizer_sorting_fit)
            counter_list_sim[list(group_type_counter_dict.keys()).index(group_type)] += len(df_organizer_sorting_sim)
            pop_list[list(group_type_counter_dict.keys()).index(group_type)] += len(df_organizer_sorting_pop)
            fit_list[list(group_type_counter_dict.keys()).index(group_type)] += len(df_organizer_sorting_fit)
            sim_list[list(group_type_counter_dict.keys()).index(group_type)] += len(df_organizer_sorting_sim)

        ind = np.arange(len(pop_list)) 
        width = 0.2
        bar1 = plt.bar(ind-width, [int(b) / (int(m) ) for b,m,n in zip(pop_list, list(group_type_counter_dict.values()),counter_list_pop)], width, color = 'r', label = 'pop')
        bar2 = plt.bar(ind, [int(b) / (int(m)) for b,m,n in zip(fit_list, list(group_type_counter_dict.values()),counter_list_fit)], width, color='g', label = 'fit')
        bar3 = plt.bar(ind+width, [ int(b) / (int(m)) if int(m) != 0 and int(n) != 0 else 0 for b,m,n in zip(sim_list, list(group_type_counter_dict.values()),counter_list_sim)], width, color = 'b', label = 'sim')
        
        
        plt.xlabel("Frequency")
        plt.ylabel('Group Types')
        plt.title("Group Type Frequence")
        plt.xticks(np.arange(12),list(group_type_counter_dict.keys()))
        plt.legend( (bar1, bar2, bar3), ('Popularity', 'Fitness', 'Similarity') )
        plt.savefig('plots/sorting_booked.png')
        
        plt.clf()
        width = 0.25
        ind = np.arange(4) 
        bar1 = plt.bar(ind-0.25, [int(b) / int(m) for b,m in zip(pop_list, list(group_type_counter_dict.values()))][0:4], width, color = 'r')
        bar2 = plt.bar(ind, [int(b) / int(m) for b,m in zip(fit_list, list(group_type_counter_dict.values()))][0:4], width, color='g')
        bar3 = plt.bar(ind+0.25, [int(b) / int(m) for b,m in zip(sim_list, list(group_type_counter_dict.values()))][0:4], width, color = 'b')
        N = 3
        ind = np.arange(N) 
        plt.xlabel("Frequency")
        plt.ylabel('Group Types')
        plt.title("Group Type Frequence")
        plt.xticks(np.arange(4),list(group_type_counter_dict.keys())[0:4])
        plt.legend( (bar1, bar2, bar3), ('Popularity', 'Fitness', 'Similarity') )
        plt.savefig('plots/sorting_booked_l1.png')
        
        plt.clf()
        width = 0.25
        ind = np.arange(4) 
        bar1 = plt.bar(ind-0.25, [int(b) / int(m) for b,m in zip(pop_list, list(group_type_counter_dict.values()))][4:8], width, color = 'r')
        bar2 = plt.bar(ind, [int(b) / int(m) for b,m in zip(fit_list, list(group_type_counter_dict.values()))][4:8], width, color='g')
        bar3 = plt.bar(ind+0.25, [int(b) / int(m) for b,m in zip(sim_list, list(group_type_counter_dict.values()))][4:8], width, color = 'b')
        N = 3
        ind = np.arange(N) 
        plt.xlabel("Frequency")
        plt.ylabel('Group Types')
        plt.title("Group Type Frequence")
        plt.xticks(np.arange(4),list(group_type_counter_dict.keys())[4:8])
        plt.legend( (bar1, bar2, bar3), ('Popularity', 'Fitness', 'Similarity') )
        plt.savefig('plots/sorting_booked_l2.png')
        
        plt.clf()
        width = 0.25
        ind = np.arange(4) 
        bar1 = plt.bar(ind-0.25, [int(b) / int(m) for b,m in zip(pop_list, list(group_type_counter_dict.values()))][8:12], width, color = 'r')
        bar2 = plt.bar(ind, [int(b) / int(m) for b,m in zip(fit_list, list(group_type_counter_dict.values()))][8:12], width, color='g')
        bar3 = plt.bar(ind+0.25, [int(b) / int(m) for b,m in zip(sim_list, list(group_type_counter_dict.values()))][8:12], width, color = 'b')
        N = 3
        ind = np.arange(N) 
        plt.xlabel("Frequency")
        plt.ylabel('Group Types')
        plt.title("Group Type Frequence")
        plt.xticks(np.arange(4),list(group_type_counter_dict.keys())[8:12])
        plt.legend( (bar1, bar2, bar3), ('Popularity', 'Fitness', 'Similarity') )
        plt.savefig('plots/sorting_booked_l3.png')
    
    def explantion_type_frequency(self):
        group_type_rating_dict = {'G1':list(), 'G2':list(), 'G3':list(), 'G4':list(), 'G5':list(), 'G6':list(), 'G7':list(), 'G8':list(), 'G9':list(), 'G10':list(), 'G11':list(), 'G12':list()}
        group_type_counter_dict = {'G1':1, 'G2':1, 'G3':1, 'G4':1, 'G5':1, 'G6':1, 'G7':1, 'G8':1, 'G9':1, 'G10':1, 'G11':1, 'G12':1}
        df_groups_type = pd.read_csv("OutPuts/group_organizer_type.csv")
        df_group_explanations = pd.read_csv("OutPuts/organizer_explanasions.csv")  
        pop_list = [0,0,0,0,0,0,0,0,0,0,0,0]
        fit_list = [0,0,0,0,0,0,0,0,0,0,0,0]
        sim_list = [0,0,0,0,0,0,0,0,0,0,0,0]
        trip_list = [0,0,0,0,0,0,0,0,0,0,0,0]
        category_list = [0,0,0,0,0,0,0,0,0,0,0,0]
        dish_list = [0,0,0,0,0,0,0,0,0,0,0,0]
        
        for index, row in df_groups_type.iterrows():
            organizer = row['organizer']
            group_type = row['type']
            df_organizer_sorting_pop = df_group_explanations.loc[(df_group_explanations['type'] == 'pop') & (df_group_explanations['user_id'] == organizer)]
            df_organizer_sorting_fit = df_group_explanations.loc[(df_group_explanations['type'] == 'fit') & (df_group_explanations['user_id'] == organizer)]
            df_organizer_sorting_sim = df_group_explanations.loc[(df_group_explanations['type'] == 'sim') & (df_group_explanations['user_id'] == organizer)]
            df_organizer_sorting_trip = df_group_explanations.loc[(df_group_explanations['type'] == 'trip') & (df_group_explanations['user_id'] == organizer)]
            df_organizer_sorting_category = df_group_explanations.loc[(df_group_explanations['type'] == 'category') & (df_group_explanations['user_id'] == organizer)]
            df_organizer_sorting_dish = df_group_explanations.loc[(df_group_explanations['type'] == 'dish') & (df_group_explanations['user_id'] == organizer)]
            temp_list = [len(df_organizer_sorting_pop),len(df_organizer_sorting_fit), len(df_organizer_sorting_sim), len(df_organizer_sorting_trip), len(df_organizer_sorting_category), len(df_organizer_sorting_dish)]
            if len(group_type_rating_dict[group_type]) == 0:
                group_type_rating_dict[group_type] = temp_list
            else:
                group_type_rating_dict[group_type] += temp_list
            group_type_counter_dict[group_type] += 1
            pop_list[list(group_type_counter_dict.keys()).index(group_type)] += len(df_organizer_sorting_pop)
            fit_list[list(group_type_counter_dict.keys()).index(group_type)] += len(df_organizer_sorting_fit)
            sim_list[list(group_type_counter_dict.keys()).index(group_type)] += len(df_organizer_sorting_sim)
            trip_list[list(group_type_counter_dict.keys()).index(group_type)] += len(df_organizer_sorting_trip)
            category_list[list(group_type_counter_dict.keys()).index(group_type)] += len(df_organizer_sorting_category)
            dish_list[list(group_type_counter_dict.keys()).index(group_type)] += len(df_organizer_sorting_dish)

        width = 0.13
        ind = np.arange(len(pop_list)) 
        bar1 = plt.bar(ind-0.2, [int(b) / int(m) for b,m in zip(pop_list, list(group_type_counter_dict.values()))], width, color = 'r')
        bar2 = plt.bar(ind-0.1, [int(b) / int(m) for b,m in zip(fit_list, list(group_type_counter_dict.values()))], width, color='g')
        bar3 = plt.bar(ind+0, [int(b) / int(m) for b,m in zip(sim_list, list(group_type_counter_dict.values()))], width, color = 'b')
        bar4 = plt.bar(ind+0.1, [int(b) / int(m) for b,m in zip(trip_list, list(group_type_counter_dict.values()))], width, color = 'c')
        bar5 = plt.bar(ind+0.2, [int(b) / int(m) for b,m in zip(category_list, list(group_type_counter_dict.values()))], width, color='m')
        bar6 = plt.bar(ind+0.3, [int(b) / int(m) for b,m in zip(dish_list, list(group_type_counter_dict.values()))], width, color = 'y')
        plt.xlabel("Frequency")
        plt.ylabel('Group Types')
        plt.title("Group Type Frequence")
        plt.xticks(np.arange(12),list(group_type_counter_dict.keys()))
        plt.legend( (bar1, bar2, bar3, bar4, bar5, bar6), ('Popularity', 'Fitness', 'Similarity', 'trip', 'category', 'dish') )
        plt.savefig('plots/used_explansion.png')  
        
        plt.clf()
        width = 0.13
        ind = np.arange(4) 
        bar1 = plt.bar(ind-0.2, [int(b) / int(m) for b,m in zip(pop_list, list(group_type_counter_dict.values()))][0:4], width, color = 'r')
        bar2 = plt.bar(ind-0.1, [int(b) / int(m) for b,m in zip(fit_list, list(group_type_counter_dict.values()))][0:4], width, color='g')
        bar3 = plt.bar(ind+0, [int(b) / int(m) for b,m in zip(sim_list, list(group_type_counter_dict.values()))][0:4], width, color = 'b')
        bar4 = plt.bar(ind+0.1, [int(b) / int(m) for b,m in zip(trip_list, list(group_type_counter_dict.values()))][0:4], width, color = 'c')
        bar5 = plt.bar(ind+0.2, [int(b) / int(m) for b,m in zip(category_list, list(group_type_counter_dict.values()))][0:4], width, color='m')
        bar6 = plt.bar(ind+0.3, [int(b) / int(m) for b,m in zip(dish_list, list(group_type_counter_dict.values()))][0:4], width, color = 'y')
        plt.xlabel("Frequency")
        plt.ylabel('Group Types')
        plt.title("Group Type Frequence")
        plt.xticks(np.arange(4),list(group_type_counter_dict.keys())[0:4])
        plt.legend( (bar1, bar2, bar3, bar4, bar5, bar6), ('Popularity', 'Fitness', 'Similarity', 'trip', 'category', 'dish') )
        plt.savefig('plots/used_explansion_l1.png')
        
        plt.clf()
        width = 0.13
        ind = np.arange(4) 
        bar1 = plt.bar(ind-0.2, [int(b) / int(m) for b,m in zip(pop_list, list(group_type_counter_dict.values()))][4:8], width, color = 'r')
        bar2 = plt.bar(ind-0.1, [int(b) / int(m) for b,m in zip(fit_list, list(group_type_counter_dict.values()))][4:8], width, color='g')
        bar3 = plt.bar(ind+0, [int(b) / int(m) for b,m in zip(sim_list, list(group_type_counter_dict.values()))][4:8], width, color = 'b')
        bar4 = plt.bar(ind+0.1, [int(b) / int(m) for b,m in zip(trip_list, list(group_type_counter_dict.values()))][4:8], width, color = 'c')
        bar5 = plt.bar(ind+0.2, [int(b) / int(m) for b,m in zip(category_list, list(group_type_counter_dict.values()))][4:8], width, color='m')
        bar6 = plt.bar(ind+0.3, [int(b) / int(m) for b,m in zip(dish_list, list(group_type_counter_dict.values()))][4:8], width, color = 'y')
        plt.xlabel("Frequency")
        plt.ylabel('Group Types')
        plt.title("Group Type Frequence")
        plt.xticks(np.arange(4),list(group_type_counter_dict.keys())[4:8])
        plt.legend( (bar1, bar2, bar3, bar4, bar5, bar6), ('Popularity', 'Fitness', 'Similarity', 'trip', 'category', 'dish') )
        plt.savefig('plots/used_explansion_l2.png')
        
        plt.clf()
        width = 0.13
        ind = np.arange(4) 
        bar1 = plt.bar(ind-0.2, [int(b) / int(m) for b,m in zip(pop_list, list(group_type_counter_dict.values()))][8:12], width, color = 'r')
        bar2 = plt.bar(ind-0.1, [int(b) / int(m) for b,m in zip(fit_list, list(group_type_counter_dict.values()))][8:12], width, color='g')
        bar3 = plt.bar(ind+0, [int(b) / int(m) for b,m in zip(sim_list, list(group_type_counter_dict.values()))][8:12], width, color = 'b')
        bar4 = plt.bar(ind+0.1, [int(b) / int(m) for b,m in zip(trip_list, list(group_type_counter_dict.values()))][8:12], width, color = 'c')
        bar5 = plt.bar(ind+0.2, [int(b) / int(m) for b,m in zip(category_list, list(group_type_counter_dict.values()))][8:12], width, color='m')
        bar6 = plt.bar(ind+0.3, [int(b) / int(m) for b,m in zip(dish_list, list(group_type_counter_dict.values()))][8:12], width, color = 'y')
        plt.xlabel("Frequency")
        plt.ylabel('Group Types')
        plt.title("Group Type Frequence")
        plt.xticks(np.arange(4),list(group_type_counter_dict.keys())[8:12])
        plt.legend( (bar1, bar2, bar3, bar4, bar5, bar6), ('Popularity', 'Fitness', 'Similarity', 'trip', 'category', 'dish') )
        plt.savefig('plots/used_explansion_l3.png')
                   
    def visited_page_ranking(self):
        group_type_rating_dict = {'G1':list(), 'G2':list(), 'G3':list(), 'G4':list(), 'G5':list(), 'G6':list(), 'G7':list(), 'G8':list(), 'G9':list(), 'G10':list(), 'G11':list(), 'G12':list()}
        
        group_type_counter_dict = {'G1':1, 'G2':1, 'G3':1, 'G4':1, 'G5':1, 'G6':1, 'G7':1, 'G8':1, 'G9':1, 'G10':1, 'G11':1, 'G12':1}
        df_groups_type = pd.read_csv("OutPuts/group_organizer_type.csv")
        df_group_explanations = pd.read_csv("OutPuts/organizer_visiting.csv")  
        pop_list = [0,0,0,0,0,0,0,0,0,0,0,0]
        fit_list = [0,0,0,0,0,0,0,0,0,0,0,0]
        sim_list = [0,0,0,0,0,0,0,0,0,0,0,0]
        counter_list_pop = [0,0,0,0,0,0,0,0,0,0,0,0]
        counter_list_fit = [0,0,0,0,0,0,0,0,0,0,0,0]
        counter_list_sim = [0,0,0,0,0,0,0,0,0,0,0,0]
        
        for index, row in df_groups_type.iterrows():
            organizer = row['organizer']
            group_type = row['type']
            df_organizer_sorting_pop = df_group_explanations.loc[(df_group_explanations['user_id'] == organizer), 'pop_rank']
            df_organizer_sorting_fit = df_group_explanations.loc[(df_group_explanations['user_id'] == organizer), 'fit_rank']
            df_organizer_sorting_sim = df_group_explanations.loc[(df_group_explanations['user_id'] == organizer), 'sim_rank']
            temp_list = [df_organizer_sorting_pop.values,df_organizer_sorting_fit.values,df_organizer_sorting_sim.values]
            if len(group_type_rating_dict[group_type]) == 0:
                group_type_rating_dict[group_type] = temp_list
            else:
                group_type_rating_dict[group_type] += temp_list
            group_type_counter_dict[group_type] += 1
            counter_list_pop[list(group_type_counter_dict.keys()).index(group_type)] += len(df_organizer_sorting_pop)
            counter_list_fit[list(group_type_counter_dict.keys()).index(group_type)] += len(df_organizer_sorting_fit)
            counter_list_sim[list(group_type_counter_dict.keys()).index(group_type)] += len(df_organizer_sorting_sim)
            pop_list[list(group_type_counter_dict.keys()).index(group_type)] += sum([item for item in df_organizer_sorting_pop.values if item > 0])
            fit_list[list(group_type_counter_dict.keys()).index(group_type)] += sum([item for item in df_organizer_sorting_fit.values if item > 0])
            sim_list[list(group_type_counter_dict.keys()).index(group_type)] += sum([item for item in df_organizer_sorting_sim.values if item > 0])
        
        ind = np.arange(len(pop_list)) 
        width = 0.2
        bar1 = plt.bar(ind+width, [int(b) / (int(m) + int(n)) for b,m,n in zip(pop_list, list(group_type_counter_dict.values()),counter_list_pop)], width, color = 'r', label = 'pop')
        bar2 = plt.bar(ind+width*2, [int(b) / (int(m) + int(n)) for b,m,n in zip(fit_list, list(group_type_counter_dict.values()),counter_list_fit)], width, color='g', label = 'fit')
        bar3 = plt.bar(ind+width*3, [int(b) / (int(m) + int(n)) for b,m,n in zip(sim_list, list(group_type_counter_dict.values()),counter_list_sim)], width, color = 'b', label = 'sim')
        
        
        plt.xlabel("Frequency")
        plt.ylabel('Group Types')
        plt.title("Group Type Frequence")
        plt.xticks(np.arange(12),list(group_type_counter_dict.keys()))
        plt.legend( (bar1, bar2, bar3), ('Popularity', 'Fitness', 'Similarity') )
        plt.savefig('plots/visited_rankings.png')  
        
        plt.clf()
        width = 0.25
        ind = np.arange(4) 
        bar1 = plt.bar(ind-0.25, [int(b) / int(m) for b,m in zip(pop_list, list(group_type_counter_dict.values()))][0:4], width, color = 'r')
        bar2 = plt.bar(ind, [int(b) / int(m) for b,m in zip(fit_list, list(group_type_counter_dict.values()))][0:4], width, color='g')
        bar3 = plt.bar(ind+0.25, [int(b) / int(m) for b,m in zip(sim_list, list(group_type_counter_dict.values()))][0:4], width, color = 'b')
        N = 3
        ind = np.arange(N) 
        plt.xlabel("Frequency")
        plt.ylabel('Group Types')
        plt.title("Group Type Frequence")
        plt.xticks(np.arange(4),list(group_type_counter_dict.keys())[0:4])
        plt.legend( (bar1, bar2, bar3), ('Popularity', 'Fitness', 'Similarity') )
        plt.savefig('plots/visited_rankings_l1.png')
        
        plt.clf()
        width = 0.25
        ind = np.arange(4) 
        bar1 = plt.bar(ind-0.25, [int(b) / int(m) for b,m in zip(pop_list, list(group_type_counter_dict.values()))][4:8], width, color = 'r')
        bar2 = plt.bar(ind, [int(b) / int(m) for b,m in zip(fit_list, list(group_type_counter_dict.values()))][4:8], width, color='g')
        bar3 = plt.bar(ind+0.25, [int(b) / int(m) for b,m in zip(sim_list, list(group_type_counter_dict.values()))][4:8], width, color = 'b')
        N = 3
        ind = np.arange(N) 
        plt.xlabel("Frequency")
        plt.ylabel('Group Types')
        plt.title("Group Type Frequence")
        plt.xticks(np.arange(4),list(group_type_counter_dict.keys())[4:8])
        plt.legend( (bar1, bar2, bar3), ('Popularity', 'Fitness', 'Similarity') )
        plt.savefig('plots/visited_rankings_l2.png')
        
        plt.clf()
        width = 0.25
        ind = np.arange(4) 
        bar1 = plt.bar(ind-0.25, [int(b) / int(m) for b,m in zip(pop_list, list(group_type_counter_dict.values()))][8:12], width, color = 'r')
        bar2 = plt.bar(ind, [int(b) / int(m) for b,m in zip(fit_list, list(group_type_counter_dict.values()))][8:12], width, color='g')
        bar3 = plt.bar(ind+0.25, [int(b) / int(m) for b,m in zip(sim_list, list(group_type_counter_dict.values()))][8:12], width, color = 'b')
        N = 3
        ind = np.arange(N) 
        plt.xlabel("Frequency")
        plt.ylabel('Group Types')
        plt.title("Group Type Frequence")
        plt.xticks(np.arange(4),list(group_type_counter_dict.keys())[8:12])
        plt.legend( (bar1, bar2, bar3), ('Popularity', 'Fitness', 'Similarity') )
        plt.savefig('plots/visited_rankings_l3.png')      
    
    def booked_page_ranking(self):
        group_type_rating_dict = {'G1':list(), 'G2':list(), 'G3':list(), 'G4':list(), 'G5':list(), 'G6':list(), 'G7':list(), 'G8':list(), 'G9':list(), 'G10':list(), 'G11':list(), 'G12':list()}
        
        group_type_counter_dict = {'G1':1, 'G2':1, 'G3':1, 'G4':1, 'G5':1, 'G6':1, 'G7':1, 'G8':1, 'G9':1, 'G10':1, 'G11':1, 'G12':1}
        df_groups_type = pd.read_csv("OutPuts/group_organizer_type.csv")
        df_group_explanations = pd.read_csv("OutPuts/organizer_booked.csv")  
        pop_list = [0,0,0,0,0,0,0,0,0,0,0,0]
        fit_list =  [0,0,0,0,0,0,0,0,0,0,0,0]
        sim_list = [0,0,0,0,0,0,0,0,0,0,0,0]
        counter_list_pop = [0,0,0,0,0,0,0,0,0,0,0,0]
        counter_list_fit = [0,0,0,0,0,0,0,0,0,0,0,0]
        counter_list_sim =  [0,0,0,0,0,0,0,0,0,0,0,0]
        
        for index, row in df_groups_type.iterrows():
            organizer = row['organizer']
            group_type = row['type']
            df_organizer_sorting_pop = df_group_explanations.loc[(df_group_explanations['user_id'] == organizer), 'pop_rank']
            df_organizer_sorting_fit = df_group_explanations.loc[(df_group_explanations['user_id'] == organizer), 'fit_rank']
            df_organizer_sorting_sim = df_group_explanations.loc[(df_group_explanations['user_id'] == organizer), 'sim_rank']
            temp_list = [df_organizer_sorting_pop.values,df_organizer_sorting_fit.values,df_organizer_sorting_sim.values]
            if len(group_type_rating_dict[group_type]) == 0:
                group_type_rating_dict[group_type] = temp_list
            else:
                group_type_rating_dict[group_type] += temp_list
            group_type_counter_dict[group_type] += 1
            counter_list_pop[list(group_type_counter_dict.keys()).index(group_type)] += len(df_organizer_sorting_pop)
            counter_list_fit[list(group_type_counter_dict.keys()).index(group_type)] += len(df_organizer_sorting_fit)
            counter_list_sim[list(group_type_counter_dict.keys()).index(group_type)] += len(df_organizer_sorting_sim)
            pop_list[list(group_type_counter_dict.keys()).index(group_type)] += sum([item for item in df_organizer_sorting_pop.values if item > 0])
            fit_list[list(group_type_counter_dict.keys()).index(group_type)] += sum([item for item in df_organizer_sorting_fit.values if item > 0])
            sim_list[list(group_type_counter_dict.keys()).index(group_type)] += sum([item for item in df_organizer_sorting_sim.values if item > 0])
        
        ind = np.arange(len(pop_list)) 
        width = 0.2
        bar1 = plt.bar(ind+width, [int(b) / (int(m) + int(n)) for b,m,n in zip(pop_list, list(group_type_counter_dict.values()),counter_list_pop)], width, color = 'r', label = 'pop')
        bar2 = plt.bar(ind+width*2, [int(b) / (int(m) + int(n)) for b,m,n in zip(fit_list, list(group_type_counter_dict.values()),counter_list_fit)], width, color='g', label = 'fit')
        bar3 = plt.bar(ind+width*3, [int(b) / (int(m) + int(n)) for b,m,n in zip(sim_list, list(group_type_counter_dict.values()),counter_list_sim)], width, color = 'b', label = 'sim')
        
        
        plt.xlabel("Frequency")
        plt.ylabel('Group Types')
        plt.title("Group Type Frequence")
        plt.xticks(np.arange(12),list(group_type_counter_dict.keys()))
        plt.legend( (bar1, bar2, bar3), ('Popularity', 'Fitness', 'Similarity') )
        plt.savefig('plots/booked_rankings.png')  
        
        plt.clf()
        width = 0.25
        ind = np.arange(4) 
        bar1 = plt.bar(ind-0.25, [int(b) / int(m) for b,m in zip(pop_list, list(group_type_counter_dict.values()))][0:4], width, color = 'r')
        bar2 = plt.bar(ind, [int(b) / int(m) for b,m in zip(fit_list, list(group_type_counter_dict.values()))][0:4], width, color='g')
        bar3 = plt.bar(ind+0.25, [int(b) / int(m) for b,m in zip(sim_list, list(group_type_counter_dict.values()))][0:4], width, color = 'b')
        N = 3
        ind = np.arange(N) 
        plt.xlabel("Frequency")
        plt.ylabel('Group Types')
        plt.title("Group Type Frequence")
        plt.xticks(np.arange(4),list(group_type_counter_dict.keys())[0:4])
        plt.legend( (bar1, bar2, bar3), ('Popularity', 'Fitness', 'Similarity') )
        plt.savefig('plots/booked_rankings_l1.png')
        
        plt.clf()
        width = 0.25
        ind = np.arange(4) 
        bar1 = plt.bar(ind-0.25, [int(b) / int(m) for b,m in zip(pop_list, list(group_type_counter_dict.values()))][4:8], width, color = 'r')
        bar2 = plt.bar(ind, [int(b) / int(m) for b,m in zip(fit_list, list(group_type_counter_dict.values()))][4:8], width, color='g')
        bar3 = plt.bar(ind+0.25, [int(b) / int(m) for b,m in zip(sim_list, list(group_type_counter_dict.values()))][4:8], width, color = 'b')
        N = 3
        ind = np.arange(N) 
        plt.xlabel("Frequency")
        plt.ylabel('Group Types')
        plt.title("Group Type Frequence")
        plt.xticks(np.arange(4),list(group_type_counter_dict.keys())[4:8])
        plt.legend( (bar1, bar2, bar3), ('Popularity', 'Fitness', 'Similarity') )
        plt.savefig('plots/booked_rankings_l2.png')
        
        plt.clf()
        width = 0.25
        ind = np.arange(4) 
        bar1 = plt.bar(ind-0.25, [int(b) / int(m) for b,m in zip(pop_list, list(group_type_counter_dict.values()))][8:12], width, color = 'r')
        bar2 = plt.bar(ind, [int(b) / int(m) for b,m in zip(fit_list, list(group_type_counter_dict.values()))][8:12], width, color='g')
        bar3 = plt.bar(ind+0.25, [int(b) / int(m) for b,m in zip(sim_list, list(group_type_counter_dict.values()))][8:12], width, color = 'b')
        N = 3
        ind = np.arange(N) 
        plt.xlabel("Frequency")
        plt.ylabel('Group Types')
        plt.title("Group Type Frequence")
        plt.xticks(np.arange(4),list(group_type_counter_dict.keys())[8:12])
        plt.legend( (bar1, bar2, bar3), ('Popularity', 'Fitness', 'Similarity') )
        plt.savefig('plots/booked_rankings_l3.png')      
        
    def visited_page_explantion_scores(self):
        group_type_rating_dict = {'G1':list(), 'G2':list(), 'G3':list(), 'G4':list(), 'G5':list(), 'G6':list(), 'G7':list(), 'G8':list(), 'G9':list(), 'G10':list(), 'G11':list(), 'G12':list()}
        
        group_type_counter_dict = {'G1':1, 'G2':1, 'G3':1, 'G4':1, 'G5':1, 'G6':1, 'G7':1, 'G8':1, 'G9':1, 'G10':1, 'G11':1, 'G12':1}
        df_groups_type = pd.read_csv("OutPuts/group_organizer_type.csv")
        df_group_explanations = pd.read_csv("OutPuts/organizer_visiting_cleaned.csv")  
        pop_list = [0,0,0,0,0,0,0,0,0,0,0,0]
        fit_list = [0,0,0,0,0,0,0,0,0,0,0,0]
        sim_list = [0,0,0,0,0,0,0,0,0,0,0,0]
        trip_list = [0,0,0,0,0,0,0,0,0,0,0,0]
        category_list = [0,0,0,0,0,0,0,0,0,0,0,0]
        dish_list = [0,0,0,0,0,0,0,0,0,0,0,0]
        counter_list_pop = [0,0,0,0,0,0,0,0,0,0,0,0]
        counter_list_fit = [0,0,0,0,0,0,0,0,0,0,0,0]
        counter_list_sim = [0,0,0,0,0,0,0,0,0,0,0,0]
        counter_list_trip = [0,0,0,0,0,0,0,0,0,0,0,0]
        counter_list_category = [0,0,0,0,0,0,0,0,0,0,0,0]
        counter_list_dish = [0,0,0,0,0,0,0,0,0,0,0,0]
        
        for index, row in df_groups_type.iterrows():
            organizer = row['organizer']
            group_type = row['type']
            # df_organizer_sorting_pop = df_group_explanations.loc[(df_group_explanations['user_id'] == organizer), 'pop_rank']
            df_organizer_sorting_fit = df_group_explanations.loc[(df_group_explanations['user_id'] == organizer), 'fit_score']
            df_organizer_sorting_sim = df_group_explanations.loc[(df_group_explanations['user_id'] == organizer), 'sim_score']
            df_organizer_sorting_trip = df_group_explanations.loc[(df_group_explanations['user_id'] == organizer), 'tip']
            df_organizer_sorting_category = df_group_explanations.loc[(df_group_explanations['user_id'] == organizer), 'category']
            df_organizer_sorting_dish = df_group_explanations.loc[(df_group_explanations['user_id'] == organizer), 'dish']
            temp_list = [self.get_popularity(list(df_group_explanations.loc[(df_group_explanations['user_id'] == organizer), 'rest_id'].values)),df_organizer_sorting_fit.values,df_organizer_sorting_sim.values]
            if len(group_type_rating_dict[group_type]) == 0:
                group_type_rating_dict[group_type] = temp_list
            else:
                group_type_rating_dict[group_type] += temp_list
            group_type_counter_dict[group_type] += 1
            counter_list_pop[list(group_type_counter_dict.keys()).index(group_type)] += len(df_organizer_sorting_fit)
            counter_list_fit[list(group_type_counter_dict.keys()).index(group_type)] += len(df_organizer_sorting_fit)
            counter_list_sim[list(group_type_counter_dict.keys()).index(group_type)] += len(df_organizer_sorting_sim)
            counter_list_trip[list(group_type_counter_dict.keys()).index(group_type)] += len(df_organizer_sorting_trip)
            counter_list_category[list(group_type_counter_dict.keys()).index(group_type)] += len(df_organizer_sorting_category)
            counter_list_dish[list(group_type_counter_dict.keys()).index(group_type)] += len(df_organizer_sorting_dish)
            pop_list[list(group_type_counter_dict.keys()).index(group_type)] += sum(self.get_popularity(list(df_group_explanations.loc[(df_group_explanations['user_id'] == organizer), 'rest_id'].values)))
            fit_list[list(group_type_counter_dict.keys()).index(group_type)] += sum([item for item in df_organizer_sorting_fit.values if item > 0])
            sim_list[list(group_type_counter_dict.keys()).index(group_type)] += sum([item for item in df_organizer_sorting_sim.values if item > 0])
            trip_list[list(group_type_counter_dict.keys()).index(group_type)] += sum([item for item in df_organizer_sorting_trip.values if item > 0])
            category_list[list(group_type_counter_dict.keys()).index(group_type)] += sum([item for item in df_organizer_sorting_category.values if item > 0])
            dish_list[list(group_type_counter_dict.keys()).index(group_type)] += sum([item for item in df_organizer_sorting_dish.values if item > 0])
        
        
        ind = np.arange(len(pop_list)) 
        width = 0.14
        bar1 = plt.bar(ind-0.2, [int(b) / (int(m) + int(n)) for b,m,n in zip(pop_list, list(group_type_counter_dict.values()),counter_list_pop)], width, color = 'r', label = 'pop')
        bar2 = plt.bar(ind-0.1, [int(b) / (int(m) + int(n)) for b,m,n in zip(fit_list, list(group_type_counter_dict.values()),counter_list_fit)], width, color='g', label = 'fit')
        bar3 = plt.bar(ind, [int(b) / (int(m) + int(n)) for b,m,n in zip(sim_list, list(group_type_counter_dict.values()),counter_list_sim)], width, color = 'b', label = 'sim')
        bar4 = plt.bar(ind+0.1, [int(b) / (int(m) + int(n)) for b,m,n in zip(trip_list, list(group_type_counter_dict.values()),counter_list_trip)], width, color = 'c')
        bar5 = plt.bar(ind+0.2, [int(b) / (int(m) + int(n)) for b,m,n in zip(category_list, list(group_type_counter_dict.values()),counter_list_category)], width, color='m')
        # bar6 = plt.bar(ind+0.3, [int(b) / (int(m) + int(n)) for b,m,n in zip(dish_list, list(group_type_counter_dict.values()),counter_list_dish)], width, color = 'y')
        plt.xlabel("Frequency")
        plt.ylabel('Group Types')
        plt.title("Group Type Frequence")
        plt.xticks(np.arange(12),list(group_type_counter_dict.keys()))
        # plt.legend( (bar1, bar2, bar3, bar4, bar5, bar6), ('Popularity', 'Fitness', 'Similarity', 'trip', 'category', 'dish'))
        plt.legend( (bar1, bar2, bar3, bar4, bar5), ('Popularity', 'Fitness', 'Similarity', 'trip', 'category') )
        plt.savefig('plots/visited_scores.png')      
        
        plt.clf()
        width = 0.13
        ind = np.arange(4) 
        bar1 = plt.bar(ind-0.2, [int(b) / (int(m) + int(n)) for b,m,n in zip(pop_list, list(group_type_counter_dict.values()),counter_list_pop)][0:4], width, color = 'r')
        bar2 = plt.bar(ind-0.1, [int(b) / (int(m) + int(n)) for b,m,n in zip(fit_list, list(group_type_counter_dict.values()),counter_list_pop)][0:4], width, color='g')
        bar3 = plt.bar(ind+0, [int(b) / int(m) for b,m in zip(sim_list, list(group_type_counter_dict.values()))][0:4], width, color = 'b')
        bar4 = plt.bar(ind+0.1, [int(b) / (int(m) + int(n)) for b,m,n in zip(trip_list, list(group_type_counter_dict.values()),counter_list_pop)][0:4], width, color = 'c')
        bar5 = plt.bar(ind+0.2, [int(b) / (int(m) + int(n)) for b,m,n in zip(category_list, list(group_type_counter_dict.values()),counter_list_pop)][0:4], width, color='m')
        # bar6 = plt.bar(ind+0.3, [int(b) / int(m) for b,m in zip(dish_list, list(group_type_counter_dict.values()))][0:4], width, color = 'y')
        plt.xlabel("Frequency")
        plt.ylabel('Group Types')
        plt.title("Group Type Frequence")
        plt.xticks(np.arange(4),list(group_type_counter_dict.keys())[0:4])
        # plt.legend( (bar1, bar2, bar3, bar4, bar5, bar6), ('Popularity', 'Fitness', 'Similarity', 'trip', 'category', 'dish') )
        plt.legend( (bar1, bar2, bar3, bar4, bar5), ('Popularity', 'Fitness', 'Similarity', 'trip', 'category') )
        plt.savefig('plots/visited_scores_l1.png')
        
        plt.clf()
        width = 0.13
        ind = np.arange(4) 
        bar1 = plt.bar(ind-0.2, [int(b) / (int(m) + int(n)) for b,m,n in zip(pop_list, list(group_type_counter_dict.values()),counter_list_pop)][4:8], width, color = 'r')
        bar2 = plt.bar(ind-0.1, [int(b) / (int(m) + int(n)) for b,m,n in zip(fit_list, list(group_type_counter_dict.values()),counter_list_pop)][4:8], width, color='g')
        bar3 = plt.bar(ind+0, [int(b) / (int(m) + int(n)) for b,m,n in zip(sim_list, list(group_type_counter_dict.values()),counter_list_pop)][4:8], width, color = 'b')
        bar4 = plt.bar(ind+0.1, [int(b) / (int(m) + int(n)) for b,m,n in zip(trip_list, list(group_type_counter_dict.values()),counter_list_pop)][4:8], width, color = 'c')
        bar5 = plt.bar(ind+0.2, [int(b) / (int(m) + int(n)) for b,m,n in zip(category_list, list(group_type_counter_dict.values()),counter_list_pop)][4:8], width, color='m')
        # bar6 = plt.bar(ind+0.3, [int(b) / (int(m) + int(n)) for b,m,n in zip(dish_list, list(group_type_counter_dict.values()),counter_list_pop)][4:8], width, color = 'y')
        plt.xlabel("Frequency")
        plt.ylabel('Group Types')
        plt.title("Group Type Frequence")
        plt.xticks(np.arange(4),list(group_type_counter_dict.keys())[4:8])
        plt.legend( (bar1, bar2, bar3, bar4, bar5), ('Popularity', 'Fitness', 'Similarity', 'trip', 'category'))
        # plt.legend( (bar1, bar2, bar3, bar4, bar5, bar6), ('Popularity', 'Fitness', 'Similarity', 'trip', 'category', 'dish') )
        plt.savefig('plots/visited_scores_l2.png')
        
        plt.clf()
        width = 0.13
        ind = np.arange(4) 
        bar1 = plt.bar(ind-0.2, [int(b) / (int(m) + int(n)) for b,m,n in zip(pop_list, list(group_type_counter_dict.values()),counter_list_pop)][8:12], width, color = 'r')
        bar2 = plt.bar(ind-0.1, [int(b) / (int(m) + int(n)) for b,m,n in zip(fit_list, list(group_type_counter_dict.values()),counter_list_pop)][8:12], width, color='g')
        bar3 = plt.bar(ind+0, [int(b) / (int(m) + int(n)) for b,m,n in zip(sim_list, list(group_type_counter_dict.values()),counter_list_pop)][8:12], width, color = 'b')
        bar4 = plt.bar(ind+0.1, [int(b) / (int(m) + int(n)) for b,m,n in zip(trip_list, list(group_type_counter_dict.values()),counter_list_pop)][8:12], width, color = 'c')
        bar5 = plt.bar(ind+0.2, [int(b) / (int(m) + int(n)) for b,m,n in zip(category_list, list(group_type_counter_dict.values()),counter_list_pop)][8:12], width, color='m')
        # bar6 = plt.bar(ind+0.3, [int(b) / (int(m) + int(n)) for b,m,n in zip(dish_list, list(group_type_counter_dict.values()),counter_list_pop)][8:12], width, color = 'y')
        plt.xlabel("Frequency")
        plt.ylabel('Group Types')
        plt.title("Group Type Frequence")
        plt.xticks(np.arange(4),list(group_type_counter_dict.keys())[8:12])
        # plt.legend( (bar1, bar2, bar3, bar4, bar5, bar6), ('Popularity', 'Fitness', 'Similarity', 'trip', 'category', 'dish') )
        plt.legend( (bar1, bar2, bar3, bar4, bar5), ('Popularity', 'Fitness', 'Similarity', 'trip', 'category') )
        plt.savefig('plots/visited_scores_l3.png')
            
    def booked_page_explantion_scores(self):
        group_type_rating_dict = {'G1':list(), 'G2':list(), 'G3':list(), 'G4':list(), 'G5':list(), 'G6':list(), 'G7':list(), 'G8':list(), 'G9':list(), 'G10':list(), 'G11':list(), 'G12':list()}
        
        group_type_counter_dict = {'G1':1, 'G2':1, 'G3':1, 'G4':1, 'G5':1, 'G6':1, 'G7':1, 'G8':1, 'G9':1, 'G10':1, 'G11':1, 'G12':1}
        df_groups_type = pd.read_csv("OutPuts/group_organizer_type.csv")
        df_group_explanations = pd.read_csv("OutPuts/organizer_booked_cleaned.csv")  
        pop_list = [0,0,0,0,0,0,0,0,0,0,0,0]
        fit_list = [0,0,0,0,0,0,0,0,0,0,0,0]
        sim_list = [0,0,0,0,0,0,0,0,0,0,0,0]
        trip_list = [0,0,0,0,0,0,0,0,0,0,0,0]
        category_list = [0,0,0,0,0,0,0,0,0,0,0,0]
        dish_list = [0,0,0,0,0,0,0,0,0,0,0,0]
        counter_list_pop = [1,1,1,1,1,1,1,1,1,1,1,1]
        counter_list_fit = [1,1,1,1,1,1,1,1,1,1,1,1]
        counter_list_sim = [1,1,1,1,1,1,1,1,1,1,1,1]
        counter_list_trip = [1,1,1,1,1,1,1,1,1,1,1,1]
        counter_list_category = [1,1,1,1,1,1,1,1,1,1,1,1]
        counter_list_dish = [1,1,1,1,1,1,1,1,1,1,1,1]
        
        for index, row in df_groups_type.iterrows():
            organizer = row['organizer']
            group_type = row['type']
            # df_organizer_sorting_pop = df_group_explanations.loc[(df_group_explanations['user_id'] == organizer), 'pop_rank']
            df_organizer_sorting_fit = df_group_explanations.loc[(df_group_explanations['user_id'] == organizer), 'fit_score']
            df_organizer_sorting_sim = df_group_explanations.loc[(df_group_explanations['user_id'] == organizer), 'sim_score']
            df_organizer_sorting_trip = df_group_explanations.loc[(df_group_explanations['user_id'] == organizer), 'tip']
            df_organizer_sorting_category = df_group_explanations.loc[(df_group_explanations['user_id'] == organizer), 'category']
            df_organizer_sorting_dish = df_group_explanations.loc[(df_group_explanations['user_id'] == organizer), 'dish']
            temp_list = [self.get_popularity(list(df_group_explanations.loc[(df_group_explanations['user_id'] == organizer), 'rest_id'].values)),df_organizer_sorting_fit.values,df_organizer_sorting_sim.values]
            if len(group_type_rating_dict[group_type]) == 0:
                group_type_rating_dict[group_type] = temp_list
            else:
                group_type_rating_dict[group_type] += temp_list
            group_type_counter_dict[group_type] += 1
            counter_list_pop[list(group_type_counter_dict.keys()).index(group_type)] += len(df_organizer_sorting_fit)
            counter_list_fit[list(group_type_counter_dict.keys()).index(group_type)] += len(df_organizer_sorting_fit)
            counter_list_sim[list(group_type_counter_dict.keys()).index(group_type)] += len(df_organizer_sorting_sim)
            counter_list_trip[list(group_type_counter_dict.keys()).index(group_type)] += len(df_organizer_sorting_trip)
            counter_list_category[list(group_type_counter_dict.keys()).index(group_type)] += len(df_organizer_sorting_category)
            counter_list_dish[list(group_type_counter_dict.keys()).index(group_type)] += len(df_organizer_sorting_dish)
            pop_list[list(group_type_counter_dict.keys()).index(group_type)] += sum(self.get_popularity(list(df_group_explanations.loc[(df_group_explanations['user_id'] == organizer), 'rest_id'].values)))
            fit_list[list(group_type_counter_dict.keys()).index(group_type)] += sum([item for item in df_organizer_sorting_fit.values if item > 0])
            sim_list[list(group_type_counter_dict.keys()).index(group_type)] += sum([item for item in df_organizer_sorting_sim.values if item > 0])
            trip_list[list(group_type_counter_dict.keys()).index(group_type)] += sum([item for item in df_organizer_sorting_trip.values if item > 0])
            category_list[list(group_type_counter_dict.keys()).index(group_type)] += sum([item for item in df_organizer_sorting_category.values if item > 0])
            dish_list[list(group_type_counter_dict.keys()).index(group_type)] += sum([item for item in df_organizer_sorting_dish.values if item > 0])
        
        
        ind = np.arange(len(pop_list)) 
        width = 0.14
        bar1 = plt.bar(ind-0.2, [int(b) / (int(m) + int(n)) for b,m,n in zip(pop_list, list(group_type_counter_dict.values()),counter_list_pop)], width, color = 'r', label = 'pop')
        bar2 = plt.bar(ind-0.1, [int(b) / (int(m) + int(n)) for b,m,n in zip(fit_list, list(group_type_counter_dict.values()),counter_list_fit)], width, color='g', label = 'fit')
        bar3 = plt.bar(ind, [int(b) / (int(m) + int(n)) for b,m,n in zip(sim_list, list(group_type_counter_dict.values()),counter_list_sim)], width, color = 'b', label = 'sim')
        bar4 = plt.bar(ind+0.1, [int(b) / (int(m) + int(n)) for b,m,n in zip(trip_list, list(group_type_counter_dict.values()),counter_list_trip)], width, color = 'c')
        bar5 = plt.bar(ind+0.2, [int(b) / (int(m) + int(n)) for b,m,n in zip(category_list, list(group_type_counter_dict.values()),counter_list_category)], width, color='m')
        bar6 = plt.bar(ind+0.3, [int(b) / (int(m) + int(n)) for b,m,n in zip(dish_list, list(group_type_counter_dict.values()),counter_list_dish)], width, color = 'y')
        plt.xlabel("Frequency")
        plt.ylabel('Group Types')
        plt.title("Group Type Frequence")
        plt.xticks(np.arange(12),list(group_type_counter_dict.keys()))
        plt.legend( (bar1, bar2, bar3, bar4, bar5, bar6), ('Popularity', 'Fitness', 'Similarity', 'trip', 'category', 'dish') )
        plt.savefig('plots/booked_scores.png')    
        
        plt.clf()
        width = 0.13
        ind = np.arange(4) 
        bar1 = plt.bar(ind-0.2, [int(b) / (int(m) + int(n)) for b,m,n in zip(pop_list, list(group_type_counter_dict.values()),counter_list_pop)][0:4], width, color = 'r')
        bar2 = plt.bar(ind-0.1, [int(b) / (int(m) + int(n)) for b,m,n in zip(fit_list, list(group_type_counter_dict.values()),counter_list_pop)][0:4], width, color='g')
        bar3 = plt.bar(ind+0, [int(b) / int(m) for b,m in zip(sim_list, list(group_type_counter_dict.values()))][0:4], width, color = 'b')
        bar4 = plt.bar(ind+0.1, [int(b) / (int(m) + int(n)) for b,m,n in zip(trip_list, list(group_type_counter_dict.values()),counter_list_pop)][0:4], width, color = 'c')
        bar5 = plt.bar(ind+0.2, [int(b) / (int(m) + int(n)) for b,m,n in zip(category_list, list(group_type_counter_dict.values()),counter_list_pop)][0:4], width, color='m')
        # bar6 = plt.bar(ind+0.3, [int(b) / int(m) for b,m in zip(dish_list, list(group_type_counter_dict.values()))][0:4], width, color = 'y')
        plt.xlabel("Frequency")
        plt.ylabel('Group Types')
        plt.title("Group Type Frequence")
        plt.xticks(np.arange(4),list(group_type_counter_dict.keys())[0:4])
        # plt.legend( (bar1, bar2, bar3, bar4, bar5, bar6), ('Popularity', 'Fitness', 'Similarity', 'trip', 'category', 'dish') )
        plt.legend( (bar1, bar2, bar3, bar4, bar5), ('Popularity', 'Fitness', 'Similarity', 'trip', 'category') )
        plt.savefig('plots/booked_scores_l1.png')
        
        plt.clf()
        width = 0.13
        ind = np.arange(4) 
        bar1 = plt.bar(ind-0.2, [int(b) / (int(m) + int(n)) for b,m,n in zip(pop_list, list(group_type_counter_dict.values()),counter_list_pop)][4:8], width, color = 'r')
        bar2 = plt.bar(ind-0.1, [int(b) / (int(m) + int(n)) for b,m,n in zip(fit_list, list(group_type_counter_dict.values()),counter_list_pop)][4:8], width, color='g')
        bar3 = plt.bar(ind+0, [int(b) / (int(m) + int(n)) for b,m,n in zip(sim_list, list(group_type_counter_dict.values()),counter_list_pop)][4:8], width, color = 'b')
        bar4 = plt.bar(ind+0.1, [int(b) / (int(m) + int(n)) for b,m,n in zip(trip_list, list(group_type_counter_dict.values()),counter_list_pop)][4:8], width, color = 'c')
        bar5 = plt.bar(ind+0.2, [int(b) / (int(m) + int(n)) for b,m,n in zip(category_list, list(group_type_counter_dict.values()),counter_list_pop)][4:8], width, color='m')
        # bar6 = plt.bar(ind+0.3, [int(b) / (int(m) + int(n)) for b,m,n in zip(dish_list, list(group_type_counter_dict.values()),counter_list_pop)][4:8], width, color = 'y')
        plt.xlabel("Frequency")
        plt.ylabel('Group Types')
        plt.title("Group Type Frequence")
        plt.xticks(np.arange(4),list(group_type_counter_dict.keys())[4:8])
        plt.legend( (bar1, bar2, bar3, bar4, bar5), ('Popularity', 'Fitness', 'Similarity', 'trip', 'category'))
        # plt.legend( (bar1, bar2, bar3, bar4, bar5, bar6), ('Popularity', 'Fitness', 'Similarity', 'trip', 'category', 'dish') )
        plt.savefig('plots/booked_scores_l2.png')
        
        plt.clf()
        width = 0.13
        ind = np.arange(4) 
        bar1 = plt.bar(ind-0.2, [int(b) / (int(m) + int(n)) for b,m,n in zip(pop_list, list(group_type_counter_dict.values()),counter_list_pop)][8:12], width, color = 'r')
        bar2 = plt.bar(ind-0.1, [int(b) / (int(m) + int(n)) for b,m,n in zip(fit_list, list(group_type_counter_dict.values()),counter_list_pop)][8:12], width, color='g')
        bar3 = plt.bar(ind+0, [int(b) / (int(m) + int(n)) for b,m,n in zip(sim_list, list(group_type_counter_dict.values()),counter_list_pop)][8:12], width, color = 'b')
        bar4 = plt.bar(ind+0.1, [int(b) / (int(m) + int(n)) for b,m,n in zip(trip_list, list(group_type_counter_dict.values()),counter_list_pop)][8:12], width, color = 'c')
        bar5 = plt.bar(ind+0.2, [int(b) / (int(m) + int(n)) for b,m,n in zip(category_list, list(group_type_counter_dict.values()),counter_list_pop)][8:12], width, color='m')
        # bar6 = plt.bar(ind+0.3, [int(b) / (int(m) + int(n)) for b,m,n in zip(dish_list, list(group_type_counter_dict.values()),counter_list_pop)][8:12], width, color = 'y')
        plt.xlabel("Frequency")
        plt.ylabel('Group Types')
        plt.title("Group Type Frequence")
        plt.xticks(np.arange(4),list(group_type_counter_dict.keys())[8:12])
        # plt.legend( (bar1, bar2, bar3, bar4, bar5, bar6), ('Popularity', 'Fitness', 'Similarity', 'trip', 'category', 'dish') )
        plt.legend( (bar1, bar2, bar3, bar4, bar5), ('Popularity', 'Fitness', 'Similarity', 'trip', 'category') )
        plt.savefig('plots/booked_scores_l3.png')
              
    def get_popularity(self, rest_list):
        popularity_list = []
        for rest in rest_list:
            popularity_list.append(Explanations(None, self.mysql_conn).pupularity(rest))
        return popularity_list
    
     
            