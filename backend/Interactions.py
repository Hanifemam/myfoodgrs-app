from InteractionModel import InteractionModel
from InteractionModel import SortingModel
from InteractionModel import RemeberUsageModel
from InteractionModel import RemberingModel
from InteractionModel import ExplainModel
from InteractionModel import ConflictUsageModel
from InteractionModel import ConflictModel
from InteractionModel import BookModel
class Interaction(object):
    def __init__(self, connection_mysql):
        self.mysql_conn = connection_mysql

    def submit_interaction(self, interaction:InteractionModel):
        my_cursor = self.mysql_conn.cursor(buffered=True)
        query = "INSERT INTO interaction (group_id, interaction) " \
                "VALUES (%(group_id)s, %(interaction)s)"
        my_cursor.execute(query, interaction)
        self.mysql_conn.commit()
        
    def sorting_storage(self, sorting:SortingModel):
        my_cursor = self.mysql_conn.cursor(buffered=True)
        query = "INSERT INTO log_sorting_type (user_id, group_id,sorting_book,sorting_fit,sorting_sim) " \
                "VALUES (%(user_id)s,%(group_id)s,%(sorting_book)s,%(sorting_fit)s, %(sorting_sim)s)"
        my_cursor.execute(query, sorting)
        self.mysql_conn.commit()
        
    def remembering_usage_storage(self, remember:RemeberUsageModel):
        my_cursor = self.mysql_conn.cursor(buffered=True)
        query = "INSERT INTO log_rembering_usage (user_id, group_id,rembering_id,CROSTACEI_E_MOLLUSCHI,FUNGHI,FORMAGGI,VERDURE,PESCE,RISO,PASTA,INTERIORA,LEGUMI,TORTELLINI,GNOCCHI,CARNE,PIZZA,SALUMI,avialble_before,avialble_after,user_available_before,user_available_after) VALUES (%(user_id)s, %(group_id)s,%(rembering_id)s,%(CROSTACEI_E_MOLLUSCHI)s,%(FUNGHI)s,%(FORMAGGI)s,%(VERDURE)s,%(PESCE)s,%(RISO)s,%(PASTA)s,%(INTERIORA)s,%(LEGUMI)s,%(TORTELLINI)s,%(GNOCCHI)s,%(CARNE)s,%(PIZZA)s,%(SALUMI)s,%(avialble_before)s,%(avialble_after)s,%(user_available_before)s,%(user_available_after)s)"
        my_cursor.execute(query, remember)
        self.mysql_conn.commit()
        
    def remembring_storage(self, remeber:RemberingModel):
        my_cursor = self.mysql_conn.cursor(buffered=True)
        query = "INSERT INTO log_rembering (user_id, group_id,remembring_pop,remembring_detialed,remebr_user_id) VALUES (%(user_id)s,%(group_id)s,%(remembring_pop)s,%(remembring_detialed)s, %(remebr_user_id)s)"
        my_cursor.execute(query, remeber)
        self.mysql_conn.commit()
        
    def explain_storage(self, explain:ExplainModel):
        my_cursor = self.mysql_conn.cursor(buffered=True)
        query = "INSERT INTO log_explanasion_type (user_id, group_id,popularity,fitness,sim,trip,category,dish) VALUES (%(user_id)s,%(group_id)s,%(popularity)s,%(fitness)s, %(sim)s, %(trip)s, %(category)s, %(dish)s)"
        my_cursor.execute(query, explain)
        self.mysql_conn.commit()
        
    def conflict_usage_storage(self, conflict:ConflictUsageModel):
        my_cursor = self.mysql_conn.cursor(buffered=True)
        query = "INSERT INTO log_conflict_usage (user_id, group_id,vconflict_id,limiting_member,CROSTACEI_E_MOLLUSCHI,FUNGHI,FORMAGGI,VERDURE,PESCE,RISO,PASTA,INTERIORA,LEGUMI,TORTELLINI,GNOCCHI,CARNE,PIZZA,SALUMI,revision_number,avialble_before,avialble_after,user_available_before,user_available_after) VALUES (%(user_id)s, %(group_id)s,%(vconflict_id)s,%(limiting_member)s,%(CROSTACEI_E_MOLLUSCHI)s,%(FUNGHI)s,%(FORMAGGI)s,%(VERDURE)s,%(PESCE)s,%(RISO)s,%(PASTA)s,%(INTERIORA)s,%(LEGUMI)s,%(TORTELLINI)s,%(GNOCCHI)s,%(CARNE)s,%(PIZZA)s,%(SALUMI)s,%(revision_number)s,%(avialble_before)s,%(avialble_after)s,%(user_available_before)s,%(user_available_after)s)"
        my_cursor.execute(query, conflict)
        self.mysql_conn.commit()
        
    def conflict_storage(self, conflict:ConflictModel):
        my_cursor = self.mysql_conn.cursor(buffered=True)
        query = "INSERT INTO log_conflict (user_id, group_id,user_to_add_id) VALUES (%(user_id)s,%(group_id)s,%(user_to_add_id)s)"
        my_cursor.execute(query, conflict)
        self.mysql_conn.commit()
        
    def book_storage(self, booked:BookModel):
        my_cursor = self.mysql_conn.cursor(buffered=True)
        query = "INSERT INTO log_booked (user_id, group_id,rest_id,avialble_rest,sort_pop,sort_fit,sort_sim,fit_score,sim_score,c1_fit,c2_fit,c3_fit,c4_fit,c5_fit,fit_rank,sim_rank,pop_rank,tip,category,dish,price) VALUES (%(user_id)s, %(group_id)s,%(rest_id)s,%(avialble_rest)s,%(sort_pop)s,%(sort_fit)s,%(sort_sim)s,%(fit_score)s,%(sim_score)s,%(c1_fit)s,%(c2_fit)s,%(c3_fit)s,%(c4_fit)s,%(c5_fit)s,%(fit_rank)s,%(sim_rank)s,%(pop_rank)s,%(tip)s,%(category)s,%(dish)s,%(price)s)"
        my_cursor.execute(query, booked)
        self.mysql_conn.commit()
        
    def visited_storage(self, booked:BookModel):
        my_cursor = self.mysql_conn.cursor(buffered=True)
        query = "INSERT INTO log_visited_rest (user_id, group_id,rest_id,avialble_rest,sort_pop,sort_fit,sort_sim,fit_score,sim_score,c1_fit,c2_fit,c3_fit,c4_fit,c5_fit,fit_rank,sim_rank,pop_rank,tip,category,dish,price) VALUES (%(user_id)s, %(group_id)s,%(rest_id)s,%(avialble_rest)s,%(sort_pop)s,%(sort_fit)s,%(sort_sim)s,%(fit_score)s,%(sim_score)s,%(c1_fit)s,%(c2_fit)s,%(c3_fit)s,%(c4_fit)s,%(c5_fit)s,%(fit_rank)s,%(sim_rank)s,%(pop_rank)s,%(tip)s,%(category)s,%(dish)s,%(price)s)"
        my_cursor.execute(query, booked)
        self.mysql_conn.commit()
           
    






























