from fpgrowth_py import fpgrowth
import pandas as pd
from itertools import chain, combinations

class ExpandPreference(object):
    def __init__(self, connection_mysql):
        self.my_cursor = connection_mysql
    
    def expand_preferences_contradiction_association_rules_train(self):
        user_list_current = []
        query_user = f"SELECT user_id FROM singin"
        cursor_user = self.my_cursor.cursor(buffered=True)
        cursor_user.execute(query_user)
        returing_dict = dict()
        for user in cursor_user:
            user_list_current.append(int(user[0]))
        preference_list = []
        for user in user_list_current:
            temp_dict = dict()
            user_preference_current = []
            my_cursor = self.my_cursor.cursor(buffered=True)
            query = f"SELECT id, PASTA, CARNE, PIZZA, TORTELLINI, SALUMI, PESCE, " \
                    f"LEGUMI, FUNGHI, CROSTACEI_E_MOLLUSCHI, VERDURE, GNOCCHI, " \
                    f"INTERIORA, FORMAGGI, RISO FROM user_info WHERE user_id = {user};"
            my_cursor.execute(query)
            fetched = my_cursor.fetchone()
            if fetched != None:
                if int(fetched[1]):
                    user_preference_current.append("PASTA")
                if int(fetched[2]):
                    user_preference_current.append("CARNE")
                if int(fetched[3]):
                    user_preference_current.append("PIZZA")
                if int(fetched[4]):
                    user_preference_current.append("TORTELLINI")
                if int(fetched[5]):
                    user_preference_current.append("SALUMI")
                if int(fetched[6]):
                    user_preference_current.append("PESCE")
                if int(fetched[7]):
                    user_preference_current.append("LEGUMI")
                if int(fetched[8]):
                    user_preference_current.append("FUNGHI")
                if int(fetched[9]):
                    user_preference_current.append("CROSTACEI_E_MOLLUSCHI")
                if int(fetched[10]):
                    user_preference_current.append("VERDURE")
                if int(fetched[11]):
                    user_preference_current.append("GNOCCHI")
                if int(fetched[12]):
                    user_preference_current.append("INTERIORA")
                if int(fetched[13]):
                    user_preference_current.append("FORMAGGI")
                if int(fetched[14]):
                    user_preference_current.append("RISO")
                preference_list.append(user_preference_current)
        freqItemSet, rules = fpgrowth(preference_list, minSupRatio=0.005, minConf=0.3)
        association=pd.DataFrame(rules,columns =['basket','next_product','proba']) 
        association=association.sort_values(by='proba',ascending=False)
        association.to_csv('supplementary/associated_rules.csv')
        
    def expand_preferences_contradiction_association_rules(self, group_id):
        association = pd.read_csv('supplementary/associated_rules.csv')
        user_list_current = []
        query_user = f"SELECT id FROM user WHERE group_id = {group_id}"
        cursor_user = self.my_cursor.cursor(buffered=True)
        cursor_user.execute(query_user)
        returing_dict = dict()
        for user in cursor_user:
            user_list_current.append(int(user[0]))
        
        for user in user_list_current:
            temp_dict = {"PASTA": 0, "CARNE": 0, "PIZZA": 0, "TORTELLINI": 0, "SALUMI": 0, "PESCE": 0, "LEGUMI": 0, "FUNGHI": 0, "CROSTACEI_E_MOLLUSCHI": 0, "VERDURE": 0, "GNOCCHI": 0,"INTERIORA":0, "FORMAGGI":0, "RISO":0}
            user_preference_current = []
            preference_list = []
            my_cursor = self.my_cursor.cursor(buffered=True)
            query = f"SELECT id, PASTA, CARNE, PIZZA, TORTELLINI, SALUMI, PESCE, " \
                    f"LEGUMI, FUNGHI, CROSTACEI_E_MOLLUSCHI, VERDURE, GNOCCHI, " \
                    f"INTERIORA, FORMAGGI, RISO FROM preference WHERE user_id = {user};"
            my_cursor.execute(query)
            fetched = my_cursor.fetchone()
            if fetched != None:
                if int(fetched[1]):
                    user_preference_current.append("PASTA")
                if int(fetched[2]):
                    user_preference_current.append("CARNE")
                if int(fetched[3]):
                    user_preference_current.append("PIZZA")
                if int(fetched[4]):
                    user_preference_current.append("TORTELLINI")
                if int(fetched[5]):
                    user_preference_current.append("SALUMI")
                if int(fetched[6]):
                    user_preference_current.append("PESCE")
                if int(fetched[7]):
                    user_preference_current.append("LEGUMI")
                if int(fetched[8]):
                    user_preference_current.append("FUNGHI")
                if int(fetched[9]):
                    user_preference_current.append("CROSTACEI_E_MOLLUSCHI")
                if int(fetched[10]):
                    user_preference_current.append("VERDURE")
                if int(fetched[11]):
                    user_preference_current.append("GNOCCHI")
                if int(fetched[12]):
                    user_preference_current.append("INTERIORA")
                if int(fetched[13]):
                    user_preference_current.append("FORMAGGI")
                if int(fetched[14]):
                    user_preference_current.append("RISO")
                preference_list.extend(user_preference_current)
                # print(user)
                # print(preference_list)
                for list_item in list(chain.from_iterable(combinations(preference_list, r) for r in range(1,len(preference_list)+1))):
                    if len(list_item) > 0:
                        result = self.compute_next_best_product(list_item)
                        if (result != 0):
                            temp_dict[result[0][0]] = temp_dict[result[0][0]] + result[1] * 10000
                returing_dict[user] = temp_dict
        # print(returing_dict)
        return returing_dict
    
    
    def compute_next_best_product(self, test):
        association = pd.read_csv('supplementary/associated_rules.csv')
        for k in test: 
            k = str({k})
            next_pdt = []
            if len(association[association['basket']==k].values) !=0: 
                next_pdt=[association[association['basket']==k]['next_product'].values[0]] 
                next_pdt_processed = []
                for item_to_process in next_pdt:
                    next_pdt_processed.extend(item_to_process.replace("\"", "").replace("{", "").replace("}", "").replace("'", "").split(", "))
                next_pdt = next_pdt_processed
                if not all(element in test for element in next_pdt):
                
                    proba=association[association['basket']==k]['proba'].values[0] 
                    return(next_pdt,proba)
                
        return 0
    
    def expand_preferences_contradiction(self,group_id):
        association_roles = self.expand_preferences_contradiction_association_rules(group_id)
        user_list_current = []
        query_user = f"SELECT id FROM user WHERE group_id = {group_id}"
        cursor_user = self.my_cursor.cursor(buffered=True)
        cursor_user.execute(query_user)
        returing_dict = dict()
        for user in cursor_user:
            user_list_current.append(int(user[0]))
        for user in user_list_current:
            temp_dict = dict()
            user_preference_current = []
            my_cursor = self.my_cursor.cursor(buffered=True)
            query = f"SELECT id, PASTA, CARNE, PIZZA, TORTELLINI, SALUMI, PESCE, " \
                    f"LEGUMI, FUNGHI, CROSTACEI_E_MOLLUSCHI, VERDURE, GNOCCHI, " \
                    f"INTERIORA, FORMAGGI, RISO FROM preference WHERE user_id = {user};"
            my_cursor.execute(query)
            fetched = my_cursor.fetchone()
            if fetched != None:
                if int(fetched[1]):
                    user_preference_current.append("PASTA")
                if int(fetched[2]):
                    user_preference_current.append("CARNE")
                if int(fetched[3]):
                    user_preference_current.append("PIZZA")
                if int(fetched[4]):
                    user_preference_current.append("TORTELLINI")
                if int(fetched[5]):
                    user_preference_current.append("SALUMI")
                if int(fetched[6]):
                    user_preference_current.append("PESCE")
                if int(fetched[7]):
                    user_preference_current.append("LEGUMI")
                if int(fetched[8]):
                    user_preference_current.append("FUNGHI")
                if int(fetched[9]):
                    user_preference_current.append("CROSTACEI_E_MOLLUSCHI")
                if int(fetched[10]):
                    user_preference_current.append("VERDURE")
                if int(fetched[11]):
                    user_preference_current.append("GNOCCHI")
                if int(fetched[12]):
                    user_preference_current.append("INTERIORA")
                if int(fetched[13]):
                    user_preference_current.append("FORMAGGI")
                if int(fetched[14]):
                    user_preference_current.append("RISO")
            coocuurence_count_all = {'CROSTACEI_E_MOLLUSCHI': 0, 'FUNGHI': 0, 'FORMAGGI': 0, 'VERDURE': 0, 'PESCE': 0, 'RISO': 0, 'PASTA': 0, 'INTERIORA': 0, 'LEGUMI': 0, 'TORTELLINI': 0, 'GNOCCHI': 0, 'CARNE': 0, 'PIZZA': 0, 'SALUMI': 0}
            for preference in user_preference_current:
                coocuurence_count = {'CROSTACEI_E_MOLLUSCHI': 0, 'FUNGHI': 0, 'FORMAGGI': 0, 'VERDURE': 0, 'PESCE': 0, 'RISO': 0, 'PASTA': 0, 'INTERIORA': 0, 'LEGUMI': 0, 'TORTELLINI': 0, 'GNOCCHI': 0, 'CARNE': 0, 'PIZZA': 0, 'SALUMI': 0}
                query_user = f"SELECT CROSTACEI_E_MOLLUSCHI,FUNGHI,FORMAGGI,VERDURE,PESCE,RISO,PASTA,INTERIORA,LEGUMI,TORTELLINI,GNOCCHI,CARNE,PIZZA,SALUMI FROM preference WHERE {preference} != 0"
                cursor_user = self.my_cursor.cursor(buffered=True,dictionary=True)
                cursor_user.execute(query_user)
                result = [dict([key, int(value)]
                            for key, value in dicts.items())
                            for dicts in cursor_user.fetchall()]
                for dictionary in result:
                    coocuurence_count = {i: coocuurence_count.get(i, 0) + dictionary.get(i, 0)
                        for i in set(coocuurence_count).union(dictionary)}
                coocuurence_count.pop(preference)
                coocuurence_count_all.pop(preference)
                coocuurence_count_all = {k: coocuurence_count_all.get(k, 0) + coocuurence_count.get(k, 0) for k in set(coocuurence_count_all)}
                coocuurence_count = sorted(coocuurence_count.items(), key=lambda x:x[1], reverse=True)
                converted_dict = dict(coocuurence_count)
                temp_dict[preference] = converted_dict
                # print(coocuurence_count_all)
                for key, value in coocuurence_count_all.items():
                    coocuurence_count_all[key] = association_roles[user][key] + value
                # print(coocuurence_count_all)
                coocuurence_count_all = sorted(coocuurence_count_all.items(), key=lambda x:x[1], reverse=True)
                coocuurence_count_all = dict(coocuurence_count_all)
            returing_dict[user] = temp_dict
            returing_dict[user] = coocuurence_count_all
        return returing_dict
    
    def remembering_expansion(self, user_info):
        current_user = user_info
        preference_dictionary = {"TORTELLINI":0,"PESCE":0,"CARNE":0,"GNOCCHI":0,"PIZZA":0,"RISO":0,"FORMAGGI":0,"LEGUMI":0,"VERDURE":0,"INTERIORA":0,"FUNGHI":0,"CROSTACEI_E_MOLLUSCHI":0,"PASTA":0}
        name = user_info.pop("name")
        id = user_info.pop("id")
        if current_user["age"] == 0:
            current_user["age"] = "Z"
        elif current_user["age"] <= 10:
            current_user["age"] = "A"
        elif int(current_user["age"]) <= 15:
            current_user["age"] = "B"
        elif int(current_user["age"]) <= 20:
            current_user["age"] = "C"
        elif int(current_user["age"]) <= 25:
            current_user["age"] = "D"
        elif int(current_user["age"]) <= 30:
            current_user["age"] = "E"
        elif int(current_user["age"]) <= 35:
            current_user["age"] = "F"
        elif int(current_user["age"]) <= 40:
            current_user["age"] = "G"
        elif int(current_user["age"]) <= 45:
            current_user["age"] = "H"
        elif int(current_user["age"]) <= 50:
            current_user["age"] = "I"
        elif int(current_user["age"]) <= 55:
            current_user["age"] = "J"
        elif int(current_user["age"]) <= 60:
            current_user["age"] = "L"
        elif int(current_user["age"]) <= 65:
            current_user["age"] = "M"
        elif int(current_user["age"]) <= 70:
            current_user["age"] = "N"
        else:
            current_user["age"] == "O"
        my_cursor = self.my_cursor.cursor(buffered=True, dictionary=True)
        query = f"SELECT gender,nationality,age,TORTELLINI,PESCE,CARNE,GNOCCHI,PIZZA,RISO,FORMAGGI,LEGUMI,VERDURE,INTERIORA,FUNGHI,CROSTACEI_E_MOLLUSCHI,PASTA,SALUMI,french,chinese,jpan,italian,greek,indian,spain,lebanan,moroccan,turkish,thai FROM user_info;"
        my_cursor.execute(query)
        for user in my_cursor.fetchall():
            sim_counter = 0
            sim_value = 0
            if user["age"] == 0:
                user["age"] = "Q"
            elif user["age"] <= 10:
                user["age"] = "A"
            elif int(user["age"]) <= 15:
                user["age"] = "B"
            elif int(user["age"]) <= 20:
                user["age"] = "C"
            elif int(user["age"]) <= 25:
                user["age"] = "D"
            elif int(user["age"]) <= 30:
                user["age"] = "E"
            elif int(user["age"]) <= 35:
                user["age"] ="F"
            elif int(user["age"]) <= 40:
                user["age"] = "G"
            elif int(user["age"]) <= 45:
                user["age"] = "H"
            elif int(user["age"]) <= 50:
                user["age"] = "I"
            elif int(user["age"]) <= 55:
                user["age"] = "J"
            elif int(user["age"]) <= 60:
                user["age"] = "L"
            elif int(user["age"]) <= 65:
                user["age"] = "M"
            elif int(user["age"]) <= 70:
                user["age"] = "N"
            else:
                user["age"] = "O"
            for key, value in current_user.items():
                if (key != "age" and key != "nationality" and key != "gender"):
                    if (user[key] == None):
                        user[key] = False
                    if (int(value) == int(user[key])):
                        sim_counter += 1
                else:
                    if (value == user[key]):
                        sim_counter += 1
            sim_value = sim_counter / len(current_user)
            for key, value in preference_dictionary.items():
                preference_dictionary[key] = sim_value * int(user[key]) + value
        coocuurence_count = sorted(preference_dictionary.items(), key=lambda x:x[1], reverse=True)
        converted_dict = dict(coocuurence_count)
        return converted_dict
    
    
    def remembering_expansion_pop(self):
        preference_dictionary = {"TORTELLINI":0,"PESCE":0,"CARNE":0,"GNOCCHI":0,"PIZZA":0,"RISO":0,"FORMAGGI":0,"LEGUMI":0,"VERDURE":0,"INTERIORA":0,"FUNGHI":0,"CROSTACEI_E_MOLLUSCHI":0,"PASTA":0}
        my_cursor = self.my_cursor.cursor(buffered=True, dictionary=True)
        query = f"SELECT TORTELLINI,PESCE,CARNE,GNOCCHI,PIZZA,RISO,FORMAGGI,LEGUMI,VERDURE,INTERIORA,FUNGHI,CROSTACEI_E_MOLLUSCHI,PASTA,SALUMI FROM user_info;"
        my_cursor.execute(query)
        for user in my_cursor.fetchall():
            for key, value in preference_dictionary.items():
                preference_dictionary[key] = int(user[key]) + value
        coocuurence_count = sorted(preference_dictionary.items(), key=lambda x:x[1], reverse=True)
        converted_dict = dict(coocuurence_count)
        return converted_dict
    
                