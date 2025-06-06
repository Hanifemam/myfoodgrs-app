import csv
from typing import get_type_hints
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class Remebering(object):
    def __init__(self,connection_mysql):
        self.mysql_conn = connection_mysql
        
    def remebering_usage_ration(self):
        organizer_dict = dict()
        df_groups_type = pd.read_csv("OutPuts/group_organizer_type.csv")
        df_group_remembering = pd.read_csv("OutPuts/organizer_remeber.csv")  
        group_type_counter_dict = {'G2':0, 'G4':0, 'G6':0, 'G8':0, 'G10':0, 'G12':0}
        group_type_usage_dict = {'G2':0, 'G4':0, 'G6':0, 'G8':0, 'G10':0, 'G12':0}
        
        group_type_counter_dict_all = {'G1':0, 'G2':0}
        group_type_usage_dict_all = {'G1':0, 'G2':0}
        usage_list = [0,0,0,0,0,0]
        usage_list_all = [0,0]
        for index, row in df_groups_type.iterrows():
            if row['type'] in ['G2','G4','G6','G8','G10','G12']:
                organizer = row['organizer']
                group_type = row['type']
                group_type_counter_dict[group_type] += 1
                df_organizer_usage = df_group_remembering.loc[df_group_remembering['user_id'] == organizer]
                
                if organizer not in organizer_dict.keys():
                   organizer_dict[organizer] = len(list(df_organizer_usage.values))
                else:
                    organizer_dict[organizer] = organizer_dict[organizer] + len(list(df_organizer_usage.values))
                
                group_type_usage_dict[group_type] += len(list(df_organizer_usage.values))
                if group_type == 'G2' or group_type == 'G6' or group_type == 'G10':
                    group_type_counter_dict_all['G1'] += 1
                    group_type_usage_dict_all['G1'] += len(list(df_organizer_usage.values))
                    usage_list_all[0] += len(df_organizer_usage)
                else:
                    group_type_usage_dict_all['G2'] += len(list(df_organizer_usage.values))
                    group_type_counter_dict_all['G2'] += 1
                    usage_list_all[1] += len(df_organizer_usage)
                usage_list[list(group_type_counter_dict.keys()).index(group_type)] += len(df_organizer_usage)
        
        width = 0.13
        ind = np.arange(len(usage_list)) 
        bar1 = plt.bar(ind-0.1, [int(b) / int(m) for b,m in zip(usage_list, list(group_type_counter_dict.values()))], width, color = 'r')
        
        N = 3
        ind = np.arange(N) 
        plt.xlabel("Frequency")
        plt.ylabel('Group Types')
        plt.title("Group Type Frequence")
        plt.xticks(np.arange(len(usage_list)),list(group_type_counter_dict.keys()))
        plt.savefig('plots/remebering_usage_ratio.png')
        
        plt.clf
        width = 0.13
        ind = np.arange(len(usage_list_all)) 
        bar1 = plt.bar(ind-0.1, [int(b) / int(m) for b,m in zip(usage_list_all, list(group_type_counter_dict_all.values()))], width, color = 'r')
        print("Remebring")
        print([int(b) / int(m) for b,m in zip(usage_list_all, list(group_type_counter_dict_all.values()))])
        N = 3
        ind = np.arange(N) 
        plt.xlabel("Frequency")
        plt.ylabel('Group Types')
        plt.title("Group Type Frequence")
        plt.xticks(np.arange(len(usage_list_all)),["R", "RI"])
        plt.savefig('plots/remebering_usage_ratio_all.png')
        print("Recalling")
        print(organizer_dict)
        print(len(organizer_dict.keys()))
        print(len({k:v for (k,v) in organizer_dict.items() if v > 0}))
        print(sum(organizer_dict.values()))
        
    def remebering_usage_pop_ration(self):
        df_groups_type = pd.read_csv("OutPuts/group_organizer_type.csv")
        df_group_remembering = pd.read_csv("OutPuts/organizer_remeber.csv")  
        group_type_counter_dict = {'G2':1, 'G4':1, 'G6':1, 'G8':1, 'G10':1, 'G12':1}
        group_type_usage_dict = {'G2':0, 'G4':0, 'G6':0, 'G8':0, 'G10':0, 'G12':0}
        usage_list = [0,0,0,0,0,0]
        for index, row in df_groups_type.iterrows():
            if row['type'] in ['G2','G4','G6','G8','G10','G12']:
                organizer = row['organizer']
                group_type = row['type']
                group_type_counter_dict[group_type] += 1
                df_organizer_usage = df_group_remembering.loc[(df_group_remembering['user_id'] == organizer) & (df_group_remembering['type'] == 'pop')]
                group_type_usage_dict[group_type] += len(list(df_organizer_usage.values))
                usage_list[list(group_type_counter_dict.keys()).index(group_type)] += len(df_organizer_usage)
        
        width = 0.13
        ind = np.arange(len(usage_list)) 
        bar1 = plt.bar(ind-0.1, [int(b) / int(m) for b,m in zip(usage_list, list(group_type_counter_dict.values()))], width, color = 'r')
        
        N = 3
        ind = np.arange(N) 
        plt.xlabel("Frequency")
        plt.ylabel('Group Types')
        plt.title("Group Type Frequence")
        plt.xticks(np.arange(len(usage_list)),list(group_type_counter_dict.keys()))
        plt.savefig('plots/remebering_pop_usage.png')
        
    def remebering_usage_info_ration(self):
        df_groups_type = pd.read_csv("OutPuts/group_organizer_type.csv")
        df_group_remembering = pd.read_csv("OutPuts/organizer_remeber.csv")  
        group_type_counter_dict = {'G2':1, 'G4':1, 'G6':1, 'G8':1, 'G10':1, 'G12':1}
        group_type_usage_dict = {'G2':0, 'G4':0, 'G6':0, 'G8':0, 'G10':0, 'G12':0}
        usage_list = [0,0,0,0,0,0]
        for index, row in df_groups_type.iterrows():
            if row['type'] in ['G2','G4','G6','G8','G10','G12']:
                organizer = row['organizer']
                group_type = row['type']
                group_type_counter_dict[group_type] += 1
                df_organizer_usage = df_group_remembering.loc[(df_group_remembering['user_id'] == organizer) & (df_group_remembering['type'] == 'info')]
                group_type_usage_dict[group_type] += len(list(df_organizer_usage.values))
                usage_list[list(group_type_counter_dict.keys()).index(group_type)] += len(df_organizer_usage)
        
        width = 0.13
        ind = np.arange(len(usage_list)) 
        bar1 = plt.bar(ind-0.1, [int(b) / int(m) for b,m in zip(usage_list, list(group_type_counter_dict.values()))], width, color = 'r')
        
        N = 3
        ind = np.arange(N) 
        plt.xlabel("Frequency")
        plt.ylabel('Group Types')
        plt.title("Group Type Frequence")
        plt.xticks(np.arange(len(usage_list)),list(group_type_counter_dict.keys()))
        plt.savefig('plots/remebering_info_usage.png')
        
    def group_rest_remember_increase_individual(self):
        df_groups_type = pd.read_csv("OutPuts/group_organizer_type.csv")
        df_group_remembering = pd.read_csv("OutPuts/organizer_usage_remeber.csv")  
        group_type_counter_dict = {'G2':1, 'G4':1, 'G6':1, 'G8':1, 'G10':1, 'G12':1}
        group_type_usage_dict = {'G2':0, 'G4':0, 'G6':0, 'G8':0, 'G10':0, 'G12':0}
        usage_list = [0,0,0,0,0,0]
        for index, row in df_groups_type.iterrows():
            if row['type'] in ['G2','G4','G6','G8','G10','G12']:
                organizer = row['organizer']
                group_type = row['type']
                group_type_counter_dict[group_type] += 1
                df_organizer_usage_before = df_group_remembering.loc[(df_group_remembering['user_id'] == organizer) & 
                                                              ((df_group_remembering['CROSTACEI_E_MOLLUSCHI'] == 1) 
                                                               | (df_group_remembering['FUNGHI'] == 1) 
                                                               | (df_group_remembering['FORMAGGI'] == 1) 
                                                               | (df_group_remembering['VERDURE'] == 1) 
                                                               | (df_group_remembering['PESCE'] == 1) 
                                                               | (df_group_remembering['RISO'] == 1) 
                                                               | (df_group_remembering['PASTA'] == 1) 
                                                               | (df_group_remembering['INTERIORA'] == 1) 
                                                               | (df_group_remembering['LEGUMI'] == 1) 
                                                               | (df_group_remembering['TORTELLINI'] == 1) 
                                                               | (df_group_remembering['GNOCCHI'] == 1) 
                                                               | (df_group_remembering['CARNE'] == 1) 
                                                               | (df_group_remembering['PIZZA'] == 1) 
                                                               | (df_group_remembering['SALUMI'] == 1)),'user_available_before']
                df_organizer_usage_after = df_group_remembering.loc[(df_group_remembering['user_id'] == organizer) & 
                                                              ((df_group_remembering['CROSTACEI_E_MOLLUSCHI'] == 1) 
                                                               | (df_group_remembering['FUNGHI'] == 1) 
                                                               | (df_group_remembering['FORMAGGI'] == 1) 
                                                               | (df_group_remembering['VERDURE'] == 1) 
                                                               | (df_group_remembering['PESCE'] == 1) 
                                                               | (df_group_remembering['RISO'] == 1) 
                                                               | (df_group_remembering['PASTA'] == 1) 
                                                               | (df_group_remembering['INTERIORA'] == 1) 
                                                               | (df_group_remembering['LEGUMI'] == 1) 
                                                               | (df_group_remembering['TORTELLINI'] == 1) 
                                                               | (df_group_remembering['GNOCCHI'] == 1) 
                                                               | (df_group_remembering['CARNE'] == 1) 
                                                               | (df_group_remembering['PIZZA'] == 1) 
                                                               | (df_group_remembering['SALUMI'] == 1)), 'user_available_after']
                group_type_usage_dict[group_type] += len(list(df_organizer_usage_after.values))
                usage_list[list(group_type_counter_dict.keys()).index(group_type)] += sum([after - before for before, after in zip(df_organizer_usage_before.values, df_organizer_usage_after.values)])
        
        width = 0.13
        ind = np.arange(len(usage_list)) 
        plt.bar(ind, [int(b) / int(m) for b,m in zip(usage_list, list(group_type_counter_dict.values()))], width, color = 'r')
        
        N = 3
        ind = np.arange(N) 
        plt.xlabel("Frequency")
        plt.ylabel('Group Types')
        plt.title("Group Type Frequence")
        plt.xticks(np.arange(len(usage_list)),list(group_type_counter_dict.keys()))
        plt.savefig('plots/remebering_rest_increase_individual.png')
        
    def group_rest_remember_increase_group(self):
        df_groups_type = pd.read_csv("OutPuts/group_organizer_type.csv")
        df_group_remembering = pd.read_csv("OutPuts/organizer_usage_remeber.csv")  
        group_type_counter_dict = {'G2':1, 'G4':1, 'G6':1, 'G8':1, 'G10':1, 'G12':1}
        group_type_usage_dict = {'G2':0, 'G4':0, 'G6':0, 'G8':0, 'G10':0, 'G12':0}
        usage_list = [0,0,0,0,0,0]
        for index, row in df_groups_type.iterrows():
            if row['type'] in ['G2','G4','G6','G8','G10','G12']:
                organizer = row['organizer']
                group_type = row['type']
                group_type_counter_dict[group_type] += 1
                df_organizer_usage_before = df_group_remembering.loc[(df_group_remembering['user_id'] == organizer) & 
                                                              ((df_group_remembering['CROSTACEI_E_MOLLUSCHI'] == 1) 
                                                               | (df_group_remembering['FUNGHI'] == 1) 
                                                               | (df_group_remembering['FORMAGGI'] == 1) 
                                                               | (df_group_remembering['VERDURE'] == 1) 
                                                               | (df_group_remembering['PESCE'] == 1) 
                                                               | (df_group_remembering['RISO'] == 1) 
                                                               | (df_group_remembering['PASTA'] == 1) 
                                                               | (df_group_remembering['INTERIORA'] == 1) 
                                                               | (df_group_remembering['LEGUMI'] == 1) 
                                                               | (df_group_remembering['TORTELLINI'] == 1) 
                                                               | (df_group_remembering['GNOCCHI'] == 1) 
                                                               | (df_group_remembering['CARNE'] == 1) 
                                                               | (df_group_remembering['PIZZA'] == 1) 
                                                               | (df_group_remembering['SALUMI'] == 1)),'avialble_before']
                df_organizer_usage_after = df_group_remembering.loc[(df_group_remembering['user_id'] == organizer) & 
                                                              ((df_group_remembering['CROSTACEI_E_MOLLUSCHI'] == 1) 
                                                               | (df_group_remembering['FUNGHI'] == 1) 
                                                               | (df_group_remembering['FORMAGGI'] == 1) 
                                                               | (df_group_remembering['VERDURE'] == 1) 
                                                               | (df_group_remembering['PESCE'] == 1) 
                                                               | (df_group_remembering['RISO'] == 1) 
                                                               | (df_group_remembering['PASTA'] == 1) 
                                                               | (df_group_remembering['INTERIORA'] == 1) 
                                                               | (df_group_remembering['LEGUMI'] == 1) 
                                                               | (df_group_remembering['TORTELLINI'] == 1) 
                                                               | (df_group_remembering['GNOCCHI'] == 1) 
                                                               | (df_group_remembering['CARNE'] == 1) 
                                                               | (df_group_remembering['PIZZA'] == 1) 
                                                               | (df_group_remembering['SALUMI'] == 1)), 'avialble_after']
                group_type_usage_dict[group_type] += len(list(df_organizer_usage_after.values))
                print(df_organizer_usage_before)
                print(df_organizer_usage_after)
                usage_list[list(group_type_counter_dict.keys()).index(group_type)] += sum([after - before for before, after in zip(df_organizer_usage_before.values, df_organizer_usage_after.values)])
        print(usage_list)
        
        width = 0.13
        ind = np.arange(len(usage_list)) 
        plt.bar(ind, [int(b) / int(m) for b,m in zip(usage_list, list(group_type_counter_dict.values()))], width, color = 'r')
        
        N = 3
        ind = np.arange(N) 
        plt.xlabel("Frequency")
        plt.ylabel('Group Types')
        plt.title("Group Type Frequence")
        plt.xticks(np.arange(len(usage_list)),list(group_type_counter_dict.keys()))
        plt.savefig('plots/remebering_rest_increase_group.png')
    
    def success_ratio_remebering(self):
        pass
     
    def conflict_usage_ration(self):
        organizer_dict = dict()
        df_groups_type = pd.read_csv("OutPuts/group_organizer_type.csv")
        df_group_remembering = pd.read_csv("OutPuts/organizer_conflict.csv")  
        group_type_counter_dict = {'G3':0, 'G4':0, 'G7':0, 'G8':0, 'G11':0, 'G12':0}
        group_type_usage_dict = {'G3':0, 'G4':0, 'G7':0, 'G8':0, 'G11':0, 'G12':0}
        # group_type_counter_dict_all = {'G3':0, 'G4':0, 'G7':0, 'G8':0, 'G11':0, 'G12':0}
        # group_type_usage_dict_all = {'G3':0, 'G4':0, 'G7':0, 'G8':0, 'G11':0, 'G12':0}
        group_type_counter_dict_all = {'G1':0, 'G2':0}
        group_type_usage_dict_all = {'G1':0, 'G2':0}
        usage_list = [0,0,0,0,0,0]
        usage_list_all = [0,0]
        for index, row in df_groups_type.iterrows():
            if row['type'] in ['G3','G4','G7','G8','G11','G12']:
                organizer = row['organizer']
                group_type = row['type']
                group_type_counter_dict[group_type] += 1
                df_organizer_usage = df_group_remembering.loc[df_group_remembering['user_id'] == organizer]
                group_type_usage_dict[group_type] += len(list(df_organizer_usage.values))
                usage_list[list(group_type_counter_dict.keys()).index(group_type)] += len(df_organizer_usage)
                if organizer not in organizer_dict.keys():
                   organizer_dict[organizer] = len(list(df_organizer_usage.values))
                else:
                    organizer_dict[organizer] = organizer_dict[organizer] + len(list(df_organizer_usage.values))
                if group_type == 'G3' or group_type == 'G7' or group_type == 'G11':
                    group_type_counter_dict_all['G1'] += 1
                    group_type_usage_dict_all['G1'] += len(list(df_organizer_usage.values))
                    usage_list_all[0] += len(df_organizer_usage)
                else:
                    group_type_counter_dict_all['G2'] += 1
                    group_type_usage_dict_all['G2'] += len(list(df_organizer_usage.values))
                    usage_list_all[1] += len(df_organizer_usage)
        
        width = 0.13
        ind = np.arange(len(usage_list)) 
        bar1 = plt.bar(ind-0.1, [int(b) / int(m) for b,m in zip(usage_list, list(group_type_counter_dict.values()))], width, color = 'r')
        
        print("Incompatible")
        print(organizer_dict)
        print(len(organizer_dict.keys()))
        print(len({k:v for (k,v) in organizer_dict.items() if v > 0}))
        print(sum(organizer_dict.values()))
        N = 3
        ind = np.arange(N) 
        plt.xlabel("Frequency")
        plt.ylabel('Group Types')
        plt.title("Group Type Frequence")
        plt.xticks(np.arange(len(usage_list)),list(group_type_counter_dict.keys()))
        plt.savefig('plots/confict_usage_ration.png')
        
        plt.clf
        width = 0.13
        ind = np.arange(len(usage_list_all)) 
        bar1 = plt.bar(ind-0.1, [int(b) / int(m) for b,m in zip(usage_list_all, list(group_type_counter_dict_all.values()))], width, color = 'r')
        print("Conflict")
        print([int(b) / int(m) for b,m in zip(usage_list_all, list(group_type_counter_dict_all.values()))])
        N = 3
        ind = np.arange(N) 
        plt.xlabel("Frequency")
        plt.ylabel('Group Types')
        plt.title("Group Type Frequence")
        plt.xticks(np.arange(len(usage_list_all)),["R", "RI"])
        plt.savefig('plots/confict_usage_ration_all.png')
              
    def group_rest_conflict_increase_individual(self):
        df_groups_type = pd.read_csv("OutPuts/group_organizer_type.csv")
        df_group_remembering = pd.read_csv("OutPuts/organizer_usage_conflict.csv")  
        group_type_counter_dict = {'G1':0, 'G3':0, 'G5':0, 'G7':0, 'G9':0, 'G11':0}
        group_type_usage_dict = {'G1':0, 'G3':0, 'G5':0, 'G7':0, 'G9':0, 'G11':0}
        usage_list = [0,0,0,0,0,0]
        for index, row in df_groups_type.iterrows():
            if row['type'] in ['G1','G3','G5','G7','G19','G11']:
                organizer = row['organizer']
                group_type = row['type']
                group_type_counter_dict[group_type] += 1
                df_organizer_usage_before = df_group_remembering.loc[(df_group_remembering['user_id'] == organizer) & 
                                                              ((df_group_remembering['CROSTACEI_E_MOLLUSCHI'] == 1) 
                                                               | (df_group_remembering['FUNGHI'] == 1) 
                                                               | (df_group_remembering['FORMAGGI'] == 1) 
                                                               | (df_group_remembering['VERDURE'] == 1) 
                                                               | (df_group_remembering['PESCE'] == 1) 
                                                               | (df_group_remembering['RISO'] == 1) 
                                                               | (df_group_remembering['PASTA'] == 1) 
                                                               | (df_group_remembering['INTERIORA'] == 1) 
                                                               | (df_group_remembering['LEGUMI'] == 1) 
                                                               | (df_group_remembering['TORTELLINI'] == 1) 
                                                               | (df_group_remembering['GNOCCHI'] == 1) 
                                                               | (df_group_remembering['CARNE'] == 1) 
                                                               | (df_group_remembering['PIZZA'] == 1) 
                                                               | (df_group_remembering['SALUMI'] == 1)),'user_available_before']
                df_organizer_usage_after = df_group_remembering.loc[(df_group_remembering['user_id'] == organizer) & 
                                                              ((df_group_remembering['CROSTACEI_E_MOLLUSCHI'] == 1) 
                                                               | (df_group_remembering['FUNGHI'] == 1) 
                                                               | (df_group_remembering['FORMAGGI'] == 1) 
                                                               | (df_group_remembering['VERDURE'] == 1) 
                                                               | (df_group_remembering['PESCE'] == 1) 
                                                               | (df_group_remembering['RISO'] == 1) 
                                                               | (df_group_remembering['PASTA'] == 1) 
                                                               | (df_group_remembering['INTERIORA'] == 1) 
                                                               | (df_group_remembering['LEGUMI'] == 1) 
                                                               | (df_group_remembering['TORTELLINI'] == 1) 
                                                               | (df_group_remembering['GNOCCHI'] == 1) 
                                                               | (df_group_remembering['CARNE'] == 1) 
                                                               | (df_group_remembering['PIZZA'] == 1) 
                                                               | (df_group_remembering['SALUMI'] == 1)), 'user_available_after']
                group_type_usage_dict[group_type] += len(list(df_organizer_usage_after.values))
                usage_list[list(group_type_counter_dict.keys()).index(group_type)] += sum([after - before for before, after in zip(df_organizer_usage_before.values, df_organizer_usage_after.values)])
        
        width = 0.13
        ind = np.arange(len(usage_list)) 
        plt.bar(ind, [int(b) / int(m) for b,m in zip(usage_list, list(group_type_counter_dict.values()))], width, color = 'r')
        
        N = 3
        ind = np.arange(N) 
        plt.xlabel("Frequency")
        plt.ylabel('Group Types')
        plt.title("Group Type Frequence")
        plt.xticks(np.arange(len(usage_list)),list(group_type_counter_dict.keys()))
        plt.savefig('plots/conflict_rest_increase_individual.png')
        
    def group_rest_conflict_increase_individual(self):
        df_groups_type = pd.read_csv("OutPuts/group_organizer_type.csv")
        df_group_remembering = pd.read_csv("OutPuts/organizer_usage_conflict.csv")  
        group_type_counter_dict = {'G1':0, 'G3':0, 'G5':0, 'G7':0, 'G9':0, 'G11':0}
        group_type_usage_dict = {'G1':0, 'G3':0, 'G5':0, 'G7':0, 'G9':0, 'G11':0}
        usage_list = [0,0,0,0,0,0]
        for index, row in df_groups_type.iterrows():
            if row['type'] in ['G1','G3','G5','G7','G19','G11']:
                organizer = row['organizer']
                group_type = row['type']
                group_type_counter_dict[group_type] += 1
                df_organizer_usage_before = df_group_remembering.loc[(df_group_remembering['user_id'] == organizer) & 
                                                              ((df_group_remembering['CROSTACEI_E_MOLLUSCHI'] == 1) 
                                                               | (df_group_remembering['FUNGHI'] == 1) 
                                                               | (df_group_remembering['FORMAGGI'] == 1) 
                                                               | (df_group_remembering['VERDURE'] == 1) 
                                                               | (df_group_remembering['PESCE'] == 1) 
                                                               | (df_group_remembering['RISO'] == 1) 
                                                               | (df_group_remembering['PASTA'] == 1) 
                                                               | (df_group_remembering['INTERIORA'] == 1) 
                                                               | (df_group_remembering['LEGUMI'] == 1) 
                                                               | (df_group_remembering['TORTELLINI'] == 1) 
                                                               | (df_group_remembering['GNOCCHI'] == 1) 
                                                               | (df_group_remembering['CARNE'] == 1) 
                                                               | (df_group_remembering['PIZZA'] == 1) 
                                                               | (df_group_remembering['SALUMI'] == 1)),'user_available_before']
                df_organizer_usage_after = df_group_remembering.loc[(df_group_remembering['user_id'] == organizer) & 
                                                              ((df_group_remembering['CROSTACEI_E_MOLLUSCHI'] == 1) 
                                                               | (df_group_remembering['FUNGHI'] == 1) 
                                                               | (df_group_remembering['FORMAGGI'] == 1) 
                                                               | (df_group_remembering['VERDURE'] == 1) 
                                                               | (df_group_remembering['PESCE'] == 1) 
                                                               | (df_group_remembering['RISO'] == 1) 
                                                               | (df_group_remembering['PASTA'] == 1) 
                                                               | (df_group_remembering['INTERIORA'] == 1) 
                                                               | (df_group_remembering['LEGUMI'] == 1) 
                                                               | (df_group_remembering['TORTELLINI'] == 1) 
                                                               | (df_group_remembering['GNOCCHI'] == 1) 
                                                               | (df_group_remembering['CARNE'] == 1) 
                                                               | (df_group_remembering['PIZZA'] == 1) 
                                                               | (df_group_remembering['SALUMI'] == 1)), 'user_available_after']
                group_type_usage_dict[group_type] += len(list(df_organizer_usage_after.values))
                usage_list[list(group_type_counter_dict.keys()).index(group_type)] += sum([after - before for before, after in zip(df_organizer_usage_before.values, df_organizer_usage_after.values)])
        
        width = 0.13
        ind = np.arange(len(usage_list)) 
        plt.bar(ind, [int(b) / int(m) if int(m)else 0 for b,m in zip(usage_list, list(group_type_counter_dict.values()))], width, color = 'r')
        
        N = 3
        ind = np.arange(N) 
        plt.xlabel("Frequency")
        plt.ylabel('Group Types')
        plt.title("Group Type Frequence")
        plt.xticks(np.arange(len(usage_list)),list(group_type_counter_dict.keys()))
        plt.savefig('plots/conflict_rest_increase_individual.png')
    
    def group_rest_conflict_increase_group(self):
        df_groups_type = pd.read_csv("OutPuts/group_organizer_type.csv")
        df_group_remembering = pd.read_csv("OutPuts/organizer_usage_conflict.csv")  
        group_type_counter_dict = {'G1':0, 'G3':0, 'G5':0, 'G7':0, 'G9':0, 'G11':0}
        group_type_usage_dict = {'G1':0, 'G3':0, 'G5':0, 'G7':0, 'G9':0, 'G11':0}
        usage_list = [0,0,0,0,0,0]
        for index, row in df_groups_type.iterrows():
            if row['type'] in ['G1','G3','G5','G7','G9','G11']:
                organizer = row['organizer']
                group_type = row['type']
                group_type_counter_dict[group_type] += 1
                df_organizer_usage_before = df_group_remembering.loc[(df_group_remembering['user_id'] == organizer) & 
                                                              ((df_group_remembering['CROSTACEI_E_MOLLUSCHI'] == 1) 
                                                               | (df_group_remembering['FUNGHI'] == 1) 
                                                               | (df_group_remembering['FORMAGGI'] == 1) 
                                                               | (df_group_remembering['VERDURE'] == 1) 
                                                               | (df_group_remembering['PESCE'] == 1) 
                                                               | (df_group_remembering['RISO'] == 1) 
                                                               | (df_group_remembering['PASTA'] == 1) 
                                                               | (df_group_remembering['INTERIORA'] == 1) 
                                                               | (df_group_remembering['LEGUMI'] == 1) 
                                                               | (df_group_remembering['TORTELLINI'] == 1) 
                                                               | (df_group_remembering['GNOCCHI'] == 1) 
                                                               | (df_group_remembering['CARNE'] == 1) 
                                                               | (df_group_remembering['PIZZA'] == 1) 
                                                               | (df_group_remembering['SALUMI'] == 1)),'avialble_before']
                df_organizer_usage_after = df_group_remembering.loc[(df_group_remembering['user_id'] == organizer) & 
                                                              ((df_group_remembering['CROSTACEI_E_MOLLUSCHI'] == 1) 
                                                               | (df_group_remembering['FUNGHI'] == 1) 
                                                               | (df_group_remembering['FORMAGGI'] == 1) 
                                                               | (df_group_remembering['VERDURE'] == 1) 
                                                               | (df_group_remembering['PESCE'] == 1) 
                                                               | (df_group_remembering['RISO'] == 1) 
                                                               | (df_group_remembering['PASTA'] == 1) 
                                                               | (df_group_remembering['INTERIORA'] == 1) 
                                                               | (df_group_remembering['LEGUMI'] == 1) 
                                                               | (df_group_remembering['TORTELLINI'] == 1) 
                                                               | (df_group_remembering['GNOCCHI'] == 1) 
                                                               | (df_group_remembering['CARNE'] == 1) 
                                                               | (df_group_remembering['PIZZA'] == 1) 
                                                               | (df_group_remembering['SALUMI'] == 1)), 'avialble_after']
                group_type_usage_dict[group_type] += len(list(df_organizer_usage_after.values))
                print(df_organizer_usage_before)
                print(df_organizer_usage_after)
                usage_list[list(group_type_counter_dict.keys()).index(group_type)] += sum([after - before for before, after in zip(df_organizer_usage_before.values, df_organizer_usage_after.values)])
        width = 0.13
        ind = np.arange(len(usage_list)) 
        plt.bar(ind, [int(b) / int(m) if int(m)else 0 for b,m in zip(usage_list, list(group_type_counter_dict.values()))], width, color = 'r')
        
        N = 3
        ind = np.arange(N) 
        plt.xlabel("Frequency")
        plt.ylabel('Group Types')
        plt.title("Group Type Frequence")
        plt.xticks(np.arange(len(usage_list)),list(group_type_counter_dict.keys()))
        plt.savefig('plots/conflict_rest_increase_group.png')
        
    def success_ration_conflict(self):
        pass
    
    