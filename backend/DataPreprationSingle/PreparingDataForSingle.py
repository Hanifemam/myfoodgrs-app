from ast import Str
import pandas as pd

class SingleUserData():
    def __init__(self):
        pass
    
    def get_signin_file(self):
        return pd.read_csv("./OutPuts/SignIn.csv")
        
    def user_list_stdID_list(self):
        signin_df = self.get_signin_file()
        user_name_list = list(signin_df["email"].values)
        cleaned_user_name_list = []
        for email in user_name_list:
            if "STAA" in email:
                cleaned_user_name_list.append(email[:len(email) - 2])
            elif "STBB" in email:
                cleaned_user_name_list.append(email[:len(email) - 2])
            elif "STA" in email:
                cleaned_user_name_list.append(email[:len(email) - 1])
            elif "STB" in email:
                cleaned_user_name_list.append(email[:len(email) - 1])
            elif email[- 1].isalpha():
                cleaned_user_name_list.append(email[:len(email) - 1])
            else:
                cleaned_user_name_list.append(email)
        return cleaned_user_name_list
    
    def coupled_user_id(self):
        signin_df = self.get_signin_file()
        user_stdId_list = self.user_list_stdID_list()
        coupled_user_id_dict = dict()
        for stdId in user_stdId_list:
            coupled_user_id_dict[stdId] = set()
        
        for row in signin_df.to_dict('records'):
            for stdId in user_stdId_list:
                string_stdId = str(stdId)
                string_row_name = str(row['email'])
                if string_stdId in string_row_name:
                    coupled_user_id_dict[stdId].add(row['user_id'])
                    
        return coupled_user_id_dict
    
    def get_selected_file(self):
        return pd.read_csv("./OutPuts/Selected_with_id.csv")
        
    def single_user_selected_file(self):
        selected_item_file = self.get_selected_file()
        coupled_accounts = self.coupled_user_id()
        final_df = pd.DataFrame()
        final_selected_list = []
        for user_ids in coupled_accounts.values():
            first_item_falg = True
            first_user_choice = pd.DataFrame()
            second_user_choice = pd.DataFrame()
            for user_id in user_ids:
                if first_item_falg:
                    if len(selected_item_file.loc[(selected_item_file["user_id"] == int(user_id))]['id'].values) > 0:
                        first_user_choice = selected_item_file.loc[(selected_item_file["user_id"] == user_id) & (selected_item_file["id"] == min(selected_item_file.loc[(selected_item_file["user_id"] == int(user_id))]['id'].values))]
                        first_item_falg = False
                else:
                    if len(selected_item_file.loc[(selected_item_file["user_id"] == int(user_id))]['id'].values) > 0:
                        second_user_choice = selected_item_file.loc[(selected_item_file["user_id"] == user_id) & (selected_item_file["id"] == min(selected_item_file.loc[(selected_item_file["user_id"] == int(user_id))]['id'].values))]
                        if second_user_choice['id'].values[0] < first_user_choice['id'].values[0]:
                            first_user_choice = second_user_choice
            final_df = final_df.append(first_user_choice)
        final_df.drop(['id','organizer', 'member'], axis=1).to_csv("./OutPuts/Selected_first.csv")
                    
        
        
        
        