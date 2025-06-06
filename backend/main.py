import json
import random
from http.client import HTTPException
from InteractionModel import InteractionModel
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
import ExplanationModel
from NewRestaurants import CreateNewDB
from Recommendations import Recommendations
from Explanations import Explanations
from Supplementary import Supplementary
import BookmarkModel
from Bookmark import Bookmark
import GroupModel
from Groups import Groups
import PreferenceModel
from UserInfo import UserInfoClass
from Users import Users
import UserModel
from Connection import Connection
from Explanations import Explanations
from ExtractFromPostgre import ExtractFromPostgre
from Preference import Preference
from PutInMysql import PutInMysql
from fastapi import FastAPI, Request
import uvicorn
from supplementary.Restaurant import Restaurant
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from Interactions import Interaction
from SignUp import SingUpClass
from SignupModel import SingUp
from LoginModel import Login
from LogIn import LogInClass
from UserInfoModel import UserInfoModelClass
from UserInfoModel import UserSupportModelClass
from IndividualUserAttractiveness import IndividualAttractivenessClass
from UserRestaurantRatingModel import UserRatingoModelClass
from UserRestaurantRating import UserRestaurantRatingClass
from ProgressModel import ProgressModelClass
from Progress import ProgressClass
from GroupConstruction import GroupConstructionClass
from PrePostRestaurants import PrePostRatingClass
from PreferenceExpansion import ExpandPreference
from PreferenceExpansionModel import RememberingModel
from InteractionModel import SortingModel
from InteractionModel import RemeberUsageModel
from InteractionModel import RemberingModel
from InteractionModel import ExplainModel
from InteractionModel import ConflictUsageModel
from InteractionModel import ConflictModel
from InteractionModel import BookModel
from EvaluationPrepration import DataPrepration
from EvaluationChoices import DataEvaluation
from EvaluationLogs import Evaluations
from EvaluationRemeber import Remebering
from DataPreprationSingle.PreparingDataForSingle import SingleUserData
from SingleAccountDataPrepration.EvaluationPreprationSingle import DataPreprationSingle
from SingleAccountDataPrepration.EvaluationChoicesSingle import DataEvaluationSingle
from ModelTest.RememberingTest import RememberingModels
# from GroupModel import SelectedOrganizer

origins = [
    "http://localhost:8081",
    "http://localhost:8050",
    "http://46.18.25.97:8080",
    "http://46.18.25.97:8085",
    "http://46.18.25.97:8050",
    "http://localhost:8080",
    "http://46.18.25.1:8050",
    "http://myfoodgrs.inf.unibz.it:8080",
    "http://myfoodgrs.inf.unibz.it:8085",
]
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

connectionPost = Connection().connectPost()
connectionMysql = Connection().connectMysql()


@app.get("/bookmarked/{group_id}")
async def get_bookmark(group_id: int):
    bookmarked_list = Bookmark(connectionMysql).get_bookmark(group_id)
    # print(bookmarked_list)
    return bookmarked_list


@app.post("/bookmarked")
async def insert_in_bookmark(bookmark: BookmarkModel.BookmarkModel):
    bookmark = jsonable_encoder(bookmark)
    return Bookmark(connectionMysql).insert_bookmark(bookmark)


@app.put("/bookmarked/delete")
async def delete_from_bookmark(bookmark: BookmarkModel.BookmarkModel):
    bookmark = jsonable_encoder(bookmark)
    Bookmark(connectionMysql).remove_bookmark(bookmark)
    # print(bookmarked_list)
    return 'deleted'


@app.get("/group/{group_id}")
async def get_bookmark(group_id: int):
    group_info = Groups(connectionMysql).get_group(group_id)
    # print(group_info)
    return group_info

@app.get("/group/distance/{group_id}")
async def get_bookmark(group_id: int):
    group_info = Groups(connectionMysql).get_distance(group_id)
    return group_info


@app.get("/group")
async def insert_in_group():
    return Groups(connectionMysql).insert_group()

@app.post("/group/result")
async def insert_final_result(result: GroupModel.GroupResults):
    result = jsonable_encoder(result)
    return Groups(connectionMysql).insert_group_result(result)


@app.post("/group/{group_id}{restaurant_id}")
async def insert_in_group(group: GroupModel.GroupModel, group_id, restaurant_id):
    Groups(connectionMysql).update_preference(group, group_id, restaurant_id)
    return "Done"


@app.get("/users/{group_id}")
async def get_users(group_id: int):
    group_info = Users(connectionMysql).get_users(group_id)
    return group_info


@app.get("/users/location/{group_id}")
async def get_users_location(group_id: int):
    group_info = Users(connectionMysql).get_users_location(group_id)
    return group_info


@app.get("/users/location/front/{group_id}")
async def get_users_location(group_id: int):
    group_info = Users(connectionMysql).get_users_location_front(group_id)
    return group_info


@app.post("/users/organizer")
async def insert_organizer(organizer: UserModel.Organizer):
    json_compatible_item_data = jsonable_encoder(organizer)
    return Users(connectionMysql).insert_organizer(json_compatible_item_data)


@app.post("/users/update/organizer/{user_id}")
async def update_organizer(organizer: UserModel.Organizer, user_id: int):
    return Users(connectionMysql).update_organizer(organizer, user_id)

@app.post("/users/update/organizer/groupid/{user_id}")
async def update_organizer(organizer: UserModel.Organizer, user_id: int):
    return Users(connectionMysql).update_organizer_group_id(organizer, user_id)


@app.post("/users/companion")
async def insert_companion(companion: UserModel.Companion):
    return Users(connectionMysql).insert_companion(companion)


@app.delete("/users/companion/delete/{user_id}") 
async def insert_companion(user_id: int):
    return Users(connectionMysql).remove_member_companion(user_id)

@app.delete("/users/organizer/delete/{user_id}")
async def insert_companion(user_id: int):
    return Users(connectionMysql).remove_member_organizer(user_id)


@app.post("/users/location/{user_id}")
async def update_companion(companion: UserModel.Companion, user_id: int):
    return Users(connectionMysql).update_location(companion, user_id)


@app.post("/users/location/address/{user_id}")
async def update_companion(address: UserModel.Address, user_id: int):
    address = jsonable_encoder(address)
    return Users(connectionMysql).update_location_by_address(address, user_id)


@app.delete("/users/companion/{user_id}")
async def delete_from_bookmark(user_id):
    result = Users(connectionMysql).remove_member_companion(user_id)
    return result


@app.get("/preferences/{group_id}")
async def get_preferences(group_id: int):
    preferences_dict = Preference(connectionPost, connectionMysql).get_preference(group_id)
    return preferences_dict


@app.post("/preferences")
async def insert_preferences(preference: PreferenceModel.PreferenceModel):
    result = Preference(connectionPost, connectionMysql).insert_preference(preference)
    return result


@app.post("/preferences/group/{group_id}")
async def update_preference_group(group_model: GroupModel.GroupModel, group_id):
    group_model = jsonable_encoder(group_model)
    group_id = jsonable_encoder(group_id)
    result = Preference(connectionPost, connectionMysql).update_preference_group(group_model, group_id)
    return result


@app.post("/preferences/group/price/{group_id}")
async def update_preference_group(group_model: GroupModel.GroupModel, group_id):
    group_model = jsonable_encoder(group_model)
    group_id = jsonable_encoder(group_id)
    result = Preference(connectionPost, connectionMysql).update_preference_price_group(group_model, group_id)
    return result


@app.post("/preferences/group/distance/{group_id}")
async def update_preference_group(group_model: GroupModel.GroupModel, group_id):
    group_model = jsonable_encoder(group_model)
    group_id = jsonable_encoder(group_id)
    result = Preference(connectionPost, connectionMysql).update_preference_distance_group(group_model, group_id)
    return result


@app.post("/preferences/group/delivery/{group_id}")
async def update_preference_group(group_model: GroupModel.GroupModel, group_id):
    group_model = jsonable_encoder(group_model)
    group_id = jsonable_encoder(group_id)
    result = Preference(connectionPost, connectionMysql).update_preference_delivery_group(group_model, group_id)
    return result

@app.delete("/preferences/{preference_id}")
async def delete_from_preference(preference_id):
    result = Preference(connectionPost, connectionMysql).remove_preference(preference_id)
    return result

@app.post("/preferences/{preference_id}")
async def insert_preferences(preference: PreferenceModel.PreferenceModel, preference_id):
    result = Preference(connectionPost, connectionMysql).update_preference(preference, preference_id)
    return result

@app.get("/recommendations/popularity")
async def get_popularity():
    return Recommendations(connectionPost, connectionMysql).popularity(-1)

@app.get("/recommendations/popularity/{group_id}")
async def get_popularity(group_id):
    return Recommendations(connectionPost, connectionMysql).popularity(group_id)

@app.get("/recommendations/popularity/withoutfiltering/{group_id}")
async def get_relevance(group_id):
    results = Recommendations(connectionPost, connectionMysql).popularity_without_filtering(group_id)
    return results

@app.get("/recommendations/relevance/{group_id}")
async def get_relevance(group_id):
    results = Recommendations(connectionPost, connectionMysql).relevance(group_id)
    return results

@app.get("/recommendations/relevance/withoutfiltering/{group_id}")
async def get_relevance(group_id):
    results = Recommendations(connectionPost, connectionMysql).relevance_without_filtering(group_id)
    return results

@app.get("/recommendations/attractiveness/{group_id}")
async def get_relevance(group_id):
    results = Explanations(connectionPost, connectionMysql).attractiveness(group_id)
    return results

@app.get("/recommendations/get/popularity/count")  
async def get_relevance():
    results = Explanations(connectionPost, connectionMysql).get_popularity_count()
    return results

@app.get("/recommendations/critiquing/{group_id}")
async def get_critiquings(group_id, group_model: GroupModel.GroupModel):
    results = Recommendations(connectionPost, connectionMysql).critiquing(group_id, group_model)
    return results 

@app.post("/similarity")
async def group_similarity(group_rest_info: ExplanationModel.ExplanationModel):
    group_rest_info = jsonable_encoder(group_rest_info)
    return Explanations(connectionPost, connectionMysql).similarity(group_rest_info)

@app.post("/similarity/all") 
async def group_similarity(group_rest_info: ExplanationModel.ExplanationModelAll):
    group_rest_info = jsonable_encoder(group_rest_info)
    return Explanations(connectionPost, connectionMysql).similarity_group(group_rest_info)

@app.post("/similarity/explanation") 
async def group_similarity(group_rest_info: ExplanationModel.ExplanationModel):
    group_rest_info = jsonable_encoder(group_rest_info)
    return Explanations(connectionPost, connectionMysql).get_similarity_explanation(group_rest_info)


@app.get("/restaurant/{restaurant_id}")
async def get_restaurant(restaurant_id: int):  
    return Restaurant(connectionMysql).get_restaurant(restaurant_id)


@app.get("/restaurant/menu/{restaurant_id}")
async def get_restaurant(restaurant_id: int):
    return Restaurant(connectionMysql).get_restaurant_menu(restaurant_id)

@app.get("/restaurant/menu/id/{restaurant_id}")    
async def get_restaurant(restaurant_id: int):
    return Restaurant(connectionMysql).get_restaurant_menu_id(restaurant_id)

@app.post("/interaction")   
async def group_interaction(interaction:InteractionModel):
    interaction = jsonable_encoder(interaction)
    return Interaction(connectionMysql).submit_interaction(interaction)

@app.post("/interaction/sort/storage")   
async def group_interaction(sorting:SortingModel):
    sorting = jsonable_encoder(sorting)
    return Interaction(connectionMysql).sorting_storage(sorting)

@app.post("/interaction/remebring/usage/storage")   
async def group_interaction(remember:RemeberUsageModel):
    remember = jsonable_encoder(remember)
    return Interaction(connectionMysql).remembering_usage_storage(remember)

@app.post("/interaction/remebring/storage")   
async def group_interaction(remeber:RemberingModel):
    remeber = jsonable_encoder(remeber)
    return Interaction(connectionMysql).remembring_storage(remeber)

@app.post("/interaction/explain/storage")   
async def group_interaction(explain:ExplainModel):
    explain = jsonable_encoder(explain)
    return Interaction(connectionMysql).explain_storage(explain)

@app.post("/interaction/conflict/usage/storage")   
async def group_interaction(conflict:ConflictUsageModel):
    conflict = jsonable_encoder(conflict)
    return Interaction(connectionMysql).conflict_usage_storage(conflict)

@app.post("/interaction/conflict/storage")   
async def group_interaction(conflict:ConflictModel):
    conflict = jsonable_encoder(conflict)
    return Interaction(connectionMysql).conflict_storage(conflict)

@app.post("/interaction/book/storage")   
async def group_interaction(booked:BookModel):
    booked = jsonable_encoder(booked)
    return Interaction(connectionMysql).book_storage(booked)

@app.post("/interaction/visited/storage")    
async def group_interaction(booked:BookModel):
    booked = jsonable_encoder(booked)
    return Interaction(connectionMysql).visited_storage(booked)

@app.get("/restaurant/popularity/{restaurant_id}")
async def get_restaurant_popularity(restaurant_id: int):
    return Explanations(connectionPost, connectionMysql).pupularity(restaurant_id)

@app.get("/restaurant/popularity/dict/{restaurant_id}")
async def get_restaurant_popularity(restaurant_id: int):
    return Explanations(connectionPost, connectionMysql).pupularity_dict(restaurant_id)

@app.get("/restaurant/select/popularity/{restaurant_id}")
async def get_restaurant_popularity(restaurant_id: int):
    return Explanations(connectionPost, connectionMysql).select_popularity(restaurant_id)

@app.post("/selected")
async def group_selection(selected:GroupModel.Selected):
    selected = jsonable_encoder(selected)
    return Groups(connectionMysql).insert_to_selected(selected)

@app.post("/organizer/selected") 
async def group_selection(selected:GroupModel.SelectedOrganizer):
    selected = jsonable_encoder(selected)
    return Groups(connectionMysql).insert_to_selected_organizer(selected)

@app.post("/sus")
async def group_selection(sus:GroupModel.SUS):
    sus = jsonable_encoder(sus)
    return Groups(connectionMysql).insert_to_SUS(sus)

@app.post("/registration") 
async def registration(user_info: SingUp):
    user_info = jsonable_encoder(user_info)
    return SingUpClass(connectionMysql).register_new_user(user_info)

@app.post("/login") 
async def login(user_info: Login):
    user_info = jsonable_encoder(user_info)
    return LogInClass(connectionMysql).user_login(user_info)

@app.get("/get/registeration/id/{user_id}") 
async def registiration_id(user_id: int):
    return GroupConstructionClass(connectionMysql).registiration_id(user_id)

@app.post("/userinfovalidity") 
async def userinfovalidity(user_info: UserInfoModelClass):
    user_info = jsonable_encoder(user_info)
    return UserInfoClass(connectionMysql).get_validity(user_info)

@app.post("/setuserinfo")
async def userinfovalidity(user_info: UserInfoModelClass):
    user_info = jsonable_encoder(user_info)
    return UserInfoClass( connectionMysql).set_info(user_info)

@app.post("/set/user/support") 
async def user_support(user_info: UserSupportModelClass):
    user_info = jsonable_encoder(user_info)
    return UserInfoClass( connectionMysql).set_supports(user_info)

@app.get("/individual/attractiveness/{user_id}")
async def get_individual_attractiveness(user_id: int):
    return IndividualAttractivenessClass(connectionPost, connectionMysql).individual_attractiveness(user_id)

@app.post("/user/pre/rating")
async def pre_rating(user_rating: UserRatingoModelClass): 
    user_rating = jsonable_encoder(user_rating)
    return UserRestaurantRatingClass( connectionMysql).insert_pre_rating(user_rating)

@app.post("/user/post/rating")
async def post_rating(user_rating: UserRatingoModelClass):
    user_rating = jsonable_encoder(user_rating)
    return UserRestaurantRatingClass( connectionMysql).insert_post_rating(user_rating)

@app.post("/user/update/progress")
async def pregress_update(progress: ProgressModelClass):
    progress = jsonable_encoder(progress)
    return ProgressClass(connectionMysql).pregress_update(progress)

@app.get("/user/set/progress/{user_id}")
async def set_progress(user_id: int):
    return ProgressClass(connectionMysql).pregress_set_row(user_id)

@app.get("/user/get/progress/{user_id}")
async def get_progress(user_id: int):
    return ProgressClass(connectionMysql).get_progress(user_id)

@app.get("/user/get/group/{user_id}")
async def get_group(user_id: int):
    return GroupConstructionClass(connectionMysql).get_group(user_id)

@app.get("/user/get/group/members/{group_id}")   
async def get_group_members(group_id: int):
    return GroupConstructionClass(connectionMysql).get_group_members(group_id)

@app.get("/user/restaurant/individual/rating/{user_id}")
async def individual_rating_for_group(user_id: int):
    return PrePostRatingClass(connectionMysql).get_individual_rating(user_id)

@app.get("/user/restaurant/waiting/check/{user_id}")
async def individual_rating_for_group(user_id: int):
    return PrePostRatingClass(connectionMysql).get_waiting_check(user_id)

@app.get("/user/restaurant/group/rating/{user_id}")  
async def individual_rating_for_group(user_id: int):
    return PrePostRatingClass(connectionMysql).get_group_rating(user_id)     

@app.get("/contradiction/expansion/{group_id}")     
async def contradict_expan(group_id: int):
    return ExpandPreference(connectionMysql).expand_preferences_contradiction(group_id)

@app.post("/contradiction/remember/")
async def contradict_expan(user_info: RememberingModel):
    user_info = jsonable_encoder(user_info)  
    return ExpandPreference(connectionMysql).remembering_expansion(user_info)

@app.get("/contradiction/remember/pop")
async def contradict_expan(): 
    return ExpandPreference(connectionMysql).remembering_expansion_pop()   

if __name__ == "__main__":
    connectionMysql = Connection().connectMysql() 
    # obj = DataEvaluationSingle(connectionMysql)
    # obj.get_group_size_average_without_info_level()
    # obj.group_member_size()
    obj = RememberingModels(connectionMysql)
    # obj.class_feature_correlation_binary_continous()
    # obj.class_feature_correlation_binary_binary()
    # obj.class_feature_correlation_binary_categorical()
    # obj.class_feature_correlation()
    # print("***********BINARY******************")
    obj.sign_test_scores()
    # obj.class_feature_correlation_binary_binary()
    # obj.class_feature_correlation_binary_categorical()
    # # obj.single_class_correlation()
    # print("***********Categorical******************")
    # obj.class_feature_correlation_categorical_categorical()
    # obj.get_df_user_data()
    # obj = DataEvaluation(connectionMysql)
    # obj.avr_individual_loss()
    # obj.get_group_average()
    # obj.remebering_usage_ration()
    # obj.item_fairness()
    # obj.get_group_average()
    # obj.box_plot_loss()
    # obj.box_plot_avr()
    # obj.get_group_average()
    # obj.avr_individual_loss()
    # obj = DataPrepration(connectionMysql)
    # obj.get_group_choices()
    # obj.get_demographic_info()
    # obj = DataPrepration(connectionMysql)
    # obj.fetch_groups()
    # obj.sus_score()
    # obj.groups_sizes()
    # obj.fetch_groups()
    # obj.fetch_groups_members()
    # obj.get_individual_ratings()
    # obj.get_group_ratings()
    # obj.get_user_support()
    # obj.group_organizer_type()
    # obj.get_organizer_visited_rest()
    # obj.get_organizer_booked_rest()
    # obj.get_organizer_used_sorting()
    # obj.get_organizer_used_explanasion()
    # obj.get_organizer_conflict()
    # obj.get_organizer_remember()
    # obj.get_organizer_usage_conflict()
    # obj.get_organizer_usage_remember()
    # obj.update_individual_scores()
    # obj.update_rest_info()
    # obj = GroupConstructionClass(connectionMysql)
    # obj.register_from_google_sheet()
    # obj = ExpandPreference(connectionMysql)
    # obj.expand_preferences_contradiction_association_rules_train()
    # obj.expand_preferences_contradiction(36470)
    # my_cursor = connectionMysql.cursor(buffered=True)
    # query = "SELECT user_id FROM MyFoodGRS.progress WHERE decision_making = 0 and id > 74;"
    # my_cursor.execute(query)
    # counter = 0
    # for user in my_cursor:
    #     my_cursor = connectionMysql.cursor(buffered=True)
        
    #     query = f"SELECT email FROM MyFoodGRS.singin WHERE user_id = {user[0]};"
    #     my_cursor.execute(query)
    #     temp = my_cursor.fetchone()
    #     if temp != None:
    #         counter += 1
    #         print(temp[0])
    # print(counter)
    # DataEvaluation(connectionMysql).get_group_average()
    # DataEvaluation(connectionMysql).get_group_size_average()
    # DataEvaluation(connectionMysql).avr_individual_loss()
    # DataEvaluation(connectionMysql).avr_individual_loss_size()
    # DataEvaluation(connectionMysql).item_fairness()
    # DataEvaluation(connectionMysql).item_fairness_size()
    # my_cursor = connectionMysql.cursor(buffered=True)
    # query = "SELECT user_id FROM MyFoodGRS.progress WHERE post_rating = 0 and user_id > 14638;"
    # my_cursor.execute(query)
    # counter = 0
    # for user in my_cursor:
    #     my_cursor = connectionMysql.cursor(buffered=True)
        
    #     query = f"SELECT email FROM MyFoodGRS.singin WHERE user_id = {user[0]};"
    #     my_cursor.execute(query)
    #     temp = my_cursor.fetchone()
    #     if temp != None:
    #         counter += 1
    #         print(temp[0])
    # print(counter)
    # obj = Remebering(connectionMysql)
    # obj.remebering_usage_info_ration()