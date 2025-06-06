import os

class GroupConstructionClass(object):
    def __init__(self, connection_mysql):
        self.mysql_conn = connection_mysql
            
    def registiration_id(self, user_id):
        my_cursor = self.mysql_conn.cursor(buffered=True)
        query = f"SELECT id FROM singin WHERE user_id = {int(user_id)};"
        my_cursor.execute(query)
        first_user =  my_cursor.fetchone()
        return int(first_user[0]) 
    
    def group_construction(self, member_id):
        current_size_file = open("./supplementary/group_info_current.txt","r")
        max_size_file = open("./supplementary/group_info_next.txt","r")
        current_size = int(current_size_file.readlines()[0]) + 1
        max_size = int(max_size_file.readlines()[0])
        members_id_file = open("./supplementary/members_id.txt","a")
        members_id_file.write( str(member_id) + ',')
        members_id_file.close()
        members_id_file = open("./supplementary/members_id.txt","r")
        
        members_id_list = members_id_file.readline().split(',')[1:-1]

        if len(members_id_list) >= max_size:  
            members_id_list = members_id_list[0: max_size ] 
            # members_id_list =[number for number in  members_id_file.readline().split(',')[:-1]]
            current_size_file = open("./supplementary/group_info_current.txt","w")
            max_size_file = open("./supplementary/group_info_next.txt","w")
            current_size_file.write('0')
            if max_size == 2:
                max_size_file.write('3')
            elif max_size == 3:
                max_size_file.write('4')
            elif max_size == 4:
                max_size_file.write('5')
            elif max_size == 5:
                max_size_file.write('2')
            for organizer_id in members_id_list:
                for member_id in members_id_list:
                    if organizer_id != member_id:
                        my_cursor = self.mysql_conn.cursor()
                        query = f"INSERT INTO user_group_membership (user_id,member_id) VALUES ({int(organizer_id)}, {int(member_id)});"
                        my_cursor.execute(query)
                        self.mysql_conn.commit()
            current_size_file.close()
            max_size_file.close()
            members_id_file.close()
            with open("./supplementary/members_id.txt", "r") as input:
                with open("./supplementary/members_id_temp.txt", "w") as output:
                    for line in input:
                        for word in members_id_list:
                            line = line.replace(','+word+',', ",")
                        output.write(line)
            os.replace("./supplementary/members_id_temp.txt", "./supplementary/members_id.txt")

        else:
            current_size_file = open("./supplementary/group_info_current.txt","w")
            current_size_file.write(str(current_size))
            current_size_file.close()
            max_size_file.close()
            members_id_file.close()
        
    def get_group(self, user_id):
        my_cursor = self.mysql_conn.cursor(buffered=True)
        query = f"SELECT member_id FROM user_group_membership  WHERE user_id = {int(user_id)};"
        my_cursor.execute(query)
        first_user =  my_cursor.fetchone()
        if first_user == None:
            return "Wait for your group."
        members = [first_user[0]]
        for user in my_cursor:
            members.append(user[0])
        return self.get_member_preference(members)
    
    def get_group_members(self, group_id):
        my_cursor = self.mysql_conn.cursor(buffered=True)
        query = f"SELECT id FROM user  WHERE group_id = {int(group_id)};"
        my_cursor.execute(query)
        first_user =  my_cursor.fetchone()
        if (first_user != None):
            members = [int(first_user[0])]
            for user in my_cursor:
                members.append(int(user[0]))
        else:
            members = []
        return members

    def get_member_preference(self, members):
        member_info = dict()
        for member in members:
            member_temp = dict()
            my_cursor_name = self.mysql_conn.cursor(buffered=True)
            query_name = f"SELECT name FROM MyFoodGRS.singin  WHERE user_id = {int(member)};"
            my_cursor_name.execute(query_name)
            name = my_cursor_name.fetchone()[0]
            member_temp['name'] = name
            my_cursor = self.mysql_conn.cursor(buffered=True)
            query = f"SELECT user_id, gender,nationality,age,TORTELLINI,PESCE,CARNE,GNOCCHI,PIZZA,RISO,FORMAGGI,LEGUMI,VERDURE,INTERIORA,FUNGHI,CROSTACEI_E_MOLLUSCHI,PASTA,SALUMI,french,chinese,jpan,italian,greek,indian,spain,lebanan,moroccan,turkish,thai FROM MyFoodGRS.user_info  WHERE user_id = {int(member)};"
            my_cursor.execute(query)
            member_data = my_cursor.fetchone()
            member_temp['gender'] = member_data[1]
            member_temp['nationality'] = member_data[2]
            member_temp['age'] = member_data[3]
            member_preferences = []
            if int(member_data[4]) == 1: 
                member_preferences.append('TORTELLINI')
            if int(member_data[5]) == 1: 
                member_preferences.append('PESCE')
            if int(member_data[6]) == 1: 
                member_preferences.append('CARNE')
            if int(member_data[7]) == 1: 
                member_preferences.append('GNOCCHI')
            if int(member_data[8]) == 1: 
                member_preferences.append('PIZZA')
            if int(member_data[9]) == 1: 
                member_preferences.append('RISO')
            if int(member_data[10]) == 1: 
                member_preferences.append('FORMAGGI')
            if int(member_data[11]) == 1: 
                member_preferences.append('LEGUMI')
            if int(member_data[12]) == 1: 
                member_preferences.append('VERDURE')
            if int(member_data[13]) == 1: 
                member_preferences.append('INTERIORA')
            if int(member_data[14]) == 1: 
                member_preferences.append('FUNGHI')
            if int(member_data[15]) == 1: 
                member_preferences.append('CROSTACEI_E_MOLLUSCHI')
            if int(member_data[16]) == 1: 
                member_preferences.append('PASTA')
            if int(member_data[17]) == 1: 
                member_preferences.append('SALUMI')
            member_temp['preference'] = member_preferences
            member_cuisine = []
            if int(member_data[18]) == 1: 
                member_cuisine.append('french')
            if int(member_data[19]) == 1: 
                member_cuisine.append('chinese')
            if int(member_data[20]) == 1: 
                member_cuisine.append('jpan')
            if int(member_data[21]) == 1: 
                member_cuisine.append('italian')
            if int(member_data[22]) == 1: 
                member_cuisine.append('greek')
            if int(member_data[23]) == 1: 
                member_cuisine.append('indian')
            if int(member_data[24]) == 1: 
                member_cuisine.append('spain')
            if int(member_data[25]) == 1: 
                member_cuisine.append('lebanan')
            if int(member_data[26]) == 1: 
                member_cuisine.append('moroccan')
            if int(member_data[27]) == 1: 
                member_cuisine.append('turkish')
            if int(member_data[28]) == 1: 
                member_cuisine.append('thai')
            member_temp['cuisine'] = member_cuisine
            member_info[member] = member_temp
        return member_info
