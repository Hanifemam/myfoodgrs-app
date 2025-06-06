from Supplementary import Supplementary

class IndividualAttractivenessClass(object):
    def __init__(self, connection_post, connection_mysql):
        self.mysql_conn = connection_mysql
        self.post_conn = connection_post

    def individual_attractiveness(self, user_id):
        restaurant_ids = []
        restaurant_json = []
        user_list = [user_id]
        member_preference_dict = dict()
        user_relevance_dict = dict()
        my_cursor = self.mysql_conn.cursor(buffered=True)
        for user in user_list:
            user_preference = []
            query = f"SELECT id, PASTA, CARNE, PIZZA, TORTELLINI, SALUMI, PESCE, " \
                    f"LEGUMI, FUNGHI, CROSTACEI_E_MOLLUSCHI, VERDURE, GNOCCHI, " \
                    f"INTERIORA, FORMAGGI, RISO FROM user_info WHERE user_id = {user};"
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
                member_preference_dict[user] = user_preference
        relevance_score = 0
        for user, preference in member_preference_dict.items():
            relevance_score_normalized = dict()
            if (len(preference) > 0):
                relevance_score = dict()
                for item in preference:
                    if len(relevance_score)  == 0:
                        relevance_score = Supplementary(self.post_conn, self.mysql_conn).relevance_score(preference=item)
                    else:
                        a_counter = Supplementary(self.post_conn, self.mysql_conn).relevance_score(preference=item)
                        b_counter = relevance_score
                        for key, value in a_counter.items():
                            relevance_score[key] = value + b_counter[key]
                    # relevance_score = relevance_score + Supplementary(self.post_conn, self.mysql_conn).relevance_score(preference=item)
                # user_relevance_dict[user] = relevance_score
                max_val = relevance_score[max(relevance_score, key=relevance_score.get)]
                min_val = relevance_score[min(relevance_score, key=relevance_score.get)]
                for k, value in relevance_score.items():
                    if value != 0:
                        if max_val - min_val == 0:
                            relevance_score_normalized[k] = 1
                        else:
                            relevance_score_normalized[k] = (value - min_val) / (max_val - min_val)
                relevance_score_normalized = dict(sorted(relevance_score_normalized.items(), key=lambda item: item[1], reverse=True))
                user_relevance_dict[user] = relevance_score_normalized
        return user_relevance_dict
