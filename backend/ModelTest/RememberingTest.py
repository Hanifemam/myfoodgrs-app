from dataclasses import replace
from random import random
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder
import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.svm import LinearSVC
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import make_classification
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import RandomizedSearchCV
from sklearn.neural_network import MLPClassifier
from sklearn.multioutput import MultiOutputClassifier
from sklearn.decomposition import PCA
from sklearn.feature_selection import VarianceThreshold
from imblearn.under_sampling import NearMiss
from scipy.stats import wilcoxon
import matplotlib.pyplot as plt
import random
from pandas.api.types import CategoricalDtype
from scipy import stats
from scipy.spatial import distance
from scipy.stats import chi2_contingency


class RememberingModels(object):
    def __init__(self, connection_mysql):
        self.my_cursor = connection_mysql
        
    def remembering_expansion(self, user_info):
        current_user = user_info
        preference_dictionary = {"TORTELLINI":0,"PESCE":0,"CARNE":0,"GNOCCHI":0,"PIZZA":0,"RISO":0,"FORMAGGI":0,"LEGUMI":0,"VERDURE":0,"INTERIORA":0,"FUNGHI":0,"CROSTACEI_E_MOLLUSCHI":0,"PASTA":0}
        final_preference_dictionary = {1:0, 2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0,10:0,11:0,12:0,13:0,14:0}
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
        query = f"SELECT gender,nationality,age,TORTELLINI,PESCE,CARNE,GNOCCHI,PIZZA,RISO,FORMAGGI,LEGUMI,VERDURE,INTERIORA,FUNGHI,CROSTACEI_E_MOLLUSCHI,PASTA,SALUMI,french,chinese,jpan,italian,greek,indian,spain,lebanan,moroccan,turkish,thai, id FROM user_info;"
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
            if sim_value > 0:
                for key, value in preference_dictionary.items():
                    if 'TORTELLINI' == key:
                        final_preference_dictionary[1] = sim_value * int(user[key]) + final_preference_dictionary[1]
                    if 'PESCE' == key:
                        final_preference_dictionary[2] = sim_value * int(user[key]) + final_preference_dictionary[2]
                    if 'CARNE' == key:
                        final_preference_dictionary[3] = sim_value * int(user[key]) + final_preference_dictionary[3]
                    if 'GNOCCHI' == key:
                        final_preference_dictionary[4] = sim_value * int(user[key]) + final_preference_dictionary[4]
                    if 'PIZZA' == key:
                        final_preference_dictionary[5] = sim_value * int(user[key]) + final_preference_dictionary[5]
                    if 'RISO' == key:
                        final_preference_dictionary[6] = sim_value * int(user[key]) + final_preference_dictionary[6]
                    if 'FORMAGGI' == key:
                        final_preference_dictionary[7] = sim_value * int(user[key]) + final_preference_dictionary[7]
                    if 'LEGUMI' == key:
                        final_preference_dictionary[8] = sim_value * int(user[key]) + final_preference_dictionary[8]
                    if 'VERDURE' == key:
                        final_preference_dictionary[9] = sim_value * int(user[key]) + final_preference_dictionary[9]
                    if 'INTERIORA' == key:
                        final_preference_dictionary[10] = sim_value * int(user[key]) + final_preference_dictionary[10]
                    if 'FUNGHI' == key:
                        final_preference_dictionary[11] = sim_value * int(user[key]) + final_preference_dictionary[11]
                    if 'CROSTACEI_E_MOLLUSCHI' == key:
                        final_preference_dictionary[12] = sim_value * int(user[key]) + final_preference_dictionary[12]
                    if 'PASTA' == key:
                        final_preference_dictionary[13] = sim_value * int(user[key]) + final_preference_dictionary[13]
                    if 'SALUMI' == key:
                        final_preference_dictionary[14] = sim_value * int(user[key]) + final_preference_dictionary[14]
            
        coocurence_count = sorted(final_preference_dictionary.items(), key=lambda x:x[1], reverse=True)
        converted_dict = dict(coocurence_count)
        return converted_dict
        
    def SVM(self, X_train, y_train):
        # class_distribution = {'1':13, '12':13, '13':13, '2':13, '3':13, '4':13, '5':13, '6':13, '8':13, '9':13}
        # oversample = NearMiss(sampling_strategy=class_distribution)
        # X_train, y_train = oversample.fit_resample(X_train, y_train)
        # param_grid = {'C': [0.01, 0.1, 1, 10, 100], 'gamma': [0.001, 0.01, 0.1, 1], 'kernel':['linear','poly','rbf','sigmoid']}
        # clf = GridSearchCV(SVC(probability=True, random_state=2), param_grid, cv=4).fit(X_train, y_train)
        # print('Best Estimator')
        # print(clf.best_score_)
        # input()
        clf = SVC(kernel='linear', decision_function_shape='ovr', gamma=0.1,  probability=True, random_state=1)
        
        return clf.fit(X_train, y_train)
    
    def Logistic_remembering_expansion_ovr(self, X_train, y_train):
        # class_distribution = {'1':13, '12':13, '13':13, '2':13, '3':13, '4':13, '5':13, '6':13, '8':13, '9':13}
        # oversample = NearMiss(sampling_strategy=class_distribution)
        # X_train, y_train = oversample.fit_resample(X_train, y_train)
        param_grid = {'penalty': ['l1', 'l2']}
        clf = GridSearchCV(LogisticRegression(), param_grid, cv=4).fit(X_train, y_train)
        # clf = LogisticRegression(random_state=0)
        # print('Best Estimator')
        # print(clf.best_score_)
        # input()
        # print(clf.fit(X_train, y_train).coef_)
        # print(clf.fit(X_train, y_train).classes_)
        # print(X_train.columns)
        # input()
        return clf.fit(X_train, y_train)
    
    def QDA(self, X_train, y_train):
        clf = QuadraticDiscriminantAnalysis()
        return clf.fit(X_train, y_train)
    
    def AdaBoost(self, X_train, y_train):
        clf = AdaBoostClassifier(random_state=42)
        return clf.fit(X_train, y_train)
    
    def random_forest(self, X_train, y_train):
        clf = RandomForestClassifier(random_state=42)
        return clf.fit(X_train, y_train)
    
    def Gaussian(self, X_train, y_train):
        clf = GaussianProcessClassifier(kernel =1.0 * RBF(1.9), random_state=42)
        return clf.fit(X_train, y_train)
    
    def GaussianNB(self, X_train, y_train):
        clf = GaussianNB()
        return clf.fit(X_train, y_train)
    
    def KNN(self, X_train, y_train):
        clf = KNeighborsClassifier()
        return clf.fit(X_train, y_train)
    
    def MLP(self, X_train, y_train):
        parameters = {
            'solver': ['sgd', 'adam', 'lbfgs'],
            'activation': ['relu', 'tanh'],
            'alpha': [0.000000001,10]
        }
        iterations = 20
        
        clf = MLPClassifier(random_state=5)
        randomSearch = RandomizedSearchCV(clf, param_distributions=parameters, n_jobs=-1, n_iter=iterations, cv=3,random_state=5) 
        clf_fitted = randomSearch.fit(X_train,y_train)
        # params = randomSearch.best_params_
        # score = randomSearch.best_score_
        # print(params)
        # input()
        return clf_fitted
    
    def DT(self, X_train, y_train):
        clf = DecisionTreeClassifier()
        return clf.fit(X_train, y_train)
           
    def multioutput_models(self):
        df = self.get_df_user_data()
        df = df.reset_index()
        le = LabelEncoder()
        df['gender'] = le.fit_transform(df['gender'])
        df['nationality'] = le.fit_transform(df['nationality'])
        
        X = df[['user_id', 'gender','nationality','age', 'french','chinese','jpan','italian','greek','indian','spain','lebanan','moroccan','turkish','thai']]
        y = df[['TORTELLINI','PESCE','CARNE','GNOCCHI','PIZZA','RISO','FORMAGGI','LEGUMI','VERDURE','INTERIORA','FUNGHI','CROSTACEI_E_MOLLUSCHI','PASTA','SALUMI']]
        target = y
        target=target.astype(str)
        
        X_train, X_test, y_train, y_test = train_test_split(X, target, test_size=0.30, random_state=3)
        
        multi_target_forest = MultiOutputClassifier(MLPClassifier(random_state=5), n_jobs=2).fit(X_train, y_train)
    
    def train_test(self, random_state = 0):
        df = self.get_df_user_data()
        df = df.reset_index()
        le = LabelEncoder()
        df['gender'] = le.fit_transform(df['gender'])
        df['nationality'] = le.fit_transform(df['nationality'])
        
        X = df[['user_id', 'gender','nationality','age', 'french','chinese','jpan','italian','greek','indian','spain','lebanan','moroccan','turkish','thai']]
        y = df[['TORTELLINI','PESCE','CARNE','GNOCCHI','PIZZA','RISO','FORMAGGI','LEGUMI','VERDURE','INTERIORA','FUNGHI','CROSTACEI_E_MOLLUSCHI','PASTA','SALUMI']]
        user_ids = X['user_id']
        # selector = VarianceThreshold(0.17)
        # selector.fit(X)
        # # X = X[X.columns[selector.get_support(indices=True)]]
        # pca = PCA(n_components=4)
        # pca.fit(X)
        # X = pd.DataFrame(pca.transform(X))
        # X = pd.concat([user_ids,X], axis=1)
        # X.rename(columns={('user_id',):'user_id'}, inplace=True)
        # X = df[['user_id', 'gender','nationality','age']]
        # y = df[['TORTELLINI','PESCE','CARNE','GNOCCHI','PIZZA','RISO','FORMAGGI','LEGUMI','VERDURE','INTERIORA','FUNGHI','CROSTACEI_E_MOLLUSCHI','PASTA','SALUMI']]
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0)
        dict_test = self.get_preference_dict(X_test, y_test)
        # input("CF")
        # self.CF_test(X_test, y_test, dict_test)
        
        # X_train, y_train = self.transformer_partial(X_train, y_train)
        # X_test, y_test = self.transformer_partial(X_test, y_test)
        X_train, y_train = self.transformer(X_train, y_train)
        X_test, y_test = self.transformer(X_test, y_test)
        X_train = X_train.reset_index(drop=True)
        y_train = y_train.reset_index(drop=True)
        
        
        # input("SVM_learning")
        learning_size = np.arange(0.1, 1, 0.001).tolist()
        iteration = 30
        random_state_values =  np.arange(0,iteration).tolist()
        P1 = list(np.zeros(len(learning_size)))
        P2 = list(np.zeros(len(learning_size)))
        R1 = list(np.zeros(len(learning_size)))
        R2 = list(np.zeros(len(learning_size)))
        for rs_value in random_state_values:
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=rs_value * 2)
            dict_test = self.get_preference_dict(X_test, y_test)
            # input("CF")
            # self.CF_test(X_test, y_test, dict_test)
            
            # X_train, y_train = self.transformer_partial(X_train, y_train)
            # X_test, y_test = self.transformer_partial(X_test, y_test)
            X_train, y_train = self.transformer(X_train, y_train)
            X_test, y_test = self.transformer(X_test, y_test)
            X_train = X_train.reset_index(drop=True)
            y_train = y_train.reset_index(drop=True)
            for rate, index in zip(learning_size, range(len(learning_size))):        
                random.seed(0)
                picks = random.sample(list(X.index.values),int(len(X) * rate))
                result = self.test_prepration(self.Gaussian((X_train.iloc[picks].drop('user_id', axis=1)),np.array(y_train.iloc[picks]).ravel()), X_test, y_test, dict_test)
                # result = self.test_prepration(self.SVM((X_train.iloc[picks].drop('user_id', axis=1)),np.array(y_train.iloc[picks]).ravel()), X_test, y_test, dict_test)
                P1[index] = P1[index] + result[0]
                P2[index] = P2[index] + result[1]
                R1[index] = R1[index] + result[2]
                R2[index] = R2[index] + result[3]
        # P1[len(P1)-1] = P1[len(P1)-1] + 0.6
        P1 = np.array(P1) / iteration
        P2 = np.array(P2) / iteration
        R1 = np.array(R1) / iteration
        R2 = np.array(R2) / iteration
        plt.clf()
        plt.plot(learning_size, P1)
        plt.title("Gaussian P1")
        plt.ylim(0.3, 0.6)
        plt.savefig('plots/LearningCurve/Gaussian_P1.png')
        plt.clf()
        plt.plot(learning_size, P2)
        plt.ylim(0.3, 0.6)
        plt.title("Gaussian P2")
        plt.savefig('plots/LearningCurve/Gaussian_P2.png')
        plt.clf()
        plt.plot(learning_size, R1)
        plt.ylim(0.0, 0.3)
        plt.title("Gaussian R1")
        plt.savefig('plots/LearningCurve/Gaussian_R1.png')
        plt.clf()
        plt.plot(learning_size, R2)
        plt.title("Gaussian R2")
        plt.ylim(0.3, 0.6)
        plt.savefig('plots/LearningCurve/Gaussian_R2.png')
        plt.close()
        P1 = list(np.zeros(len(learning_size)))
        P2 = list(np.zeros(len(learning_size)))
        R1 = list(np.zeros(len(learning_size)))
        R2 = list(np.zeros(len(learning_size)))
        for rs_value in random_state_values:
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=rs_value * 2)
            dict_test = self.get_preference_dict(X_test, y_test)
            # input("CF")
            # self.CF_test(X_test, y_test, dict_test)
            
            # X_train, y_train = self.transformer_partial(X_train, y_train)
            # X_test, y_test = self.transformer_partial(X_test, y_test)
            X_train, y_train = self.transformer(X_train, y_train)
            X_test, y_test = self.transformer(X_test, y_test)
            X_train = X_train.reset_index(drop=True)
            y_train = y_train.reset_index(drop=True)
            for rate, index in zip(learning_size, range(len(learning_size))):        
                random.seed(0)
                picks = random.sample(list(X.index.values),int(len(X) * rate))
                # result = self.test_prepration(self.Gaussian((X_train.iloc[picks].drop('user_id', axis=1)),np.array(y_train.iloc[picks]).ravel()), X_test, y_test, dict_test)
                result = self.test_prepration(self.SVM((X_train.iloc[picks].drop('user_id', axis=1)),np.array(y_train.iloc[picks]).ravel()), X_test, y_test, dict_test)
                P1[index] = P1[index] + result[0]
                P2[index] = P2[index] + result[1]
                R1[index] = R1[index] + result[2]
                R2[index] = R2[index] + result[3]
        # P1[len(P1)-1] = P1[len(P1)-1] + 0.6
        P1 = np.array(P1) / iteration
        P2 = np.array(P2) / iteration
        R1 = np.array(R1) / iteration
        R2 = np.array(R2) / iteration
        plt.clf()
        plt.plot(learning_size, P1)
        plt.title("SVM P1")
        plt.ylim(0.3, 0.6)
        plt.savefig('plots/LearningCurve/SVM_P1.png')
        plt.clf()
        plt.plot(learning_size, P2)
        plt.ylim(0.3, 0.6)
        plt.title("SVM P2")
        plt.savefig('plots/LearningCurve/SVM_P2.png')
        plt.clf()
        plt.plot(learning_size, R1)
        plt.ylim(0.0, 0.3)
        plt.title("SVM R1")
        plt.savefig('plots/LearningCurve/SVM_R1.png')
        plt.clf()
        plt.plot(learning_size, R2)
        plt.title("SVM R2")
        plt.ylim(0.3, 0.6)
        plt.savefig('plots/LearningCurve/SVM_R2.png')
        plt.close()
        input("SVM")
        self.test_prepration(self.SVM((X_train.drop('user_id', axis=1)),np.array(y_train).ravel()), X_test, y_test, dict_test)
        input("LR")
        self.test_prepration(self.Logistic_remembering_expansion_ovr((X_train.drop('user_id', axis=1)),np.array(y_train).ravel()), X_test, y_test, dict_test)
        input("MLP")
        self.test_prepration(self.MLP((X_train.drop('user_id', axis=1)),np.array(y_train).ravel()), X_test, y_test, dict_test)
        input("QDA")
        self.test_prepration(self.QDA((X_train.drop('user_id', axis=1)),np.array(y_train).ravel()), X_test, y_test, dict_test)
        input("Ada")
        self.test_prepration(self.AdaBoost((X_train.drop('user_id', axis=1)),np.array(y_train).ravel()), X_test, y_test, dict_test)
        input("RF")
        self.test_prepration(self.random_forest((X_train.drop('user_id', axis=1)),np.array(y_train).ravel()), X_test, y_test, dict_test)
        input("Gaussian NB")
        self.test_prepration(self.GaussianNB((X_train.drop('user_id', axis=1)),np.array(y_train).ravel()), X_test, y_test, dict_test)
        input("Gaussian Classifier")
        self.test_prepration(self.Gaussian((X_train.drop('user_id', axis=1)),np.array(y_train).ravel()), X_test, y_test, dict_test)
        input("KNN")
        self.test_prepration(self.KNN((X_train.drop('user_id', axis=1)),np.array(y_train).ravel()), X_test, y_test, dict_test)
        input("Decision Tree")
        self.test_prepration(self.DT((X_train.drop('user_id', axis=1)),np.array(y_train).ravel()), X_test, y_test, dict_test)
    
    def train_test_sign(self, random_state = 0, model = 'SVM'):
        df = self.get_df_user_data()
        df = df.reset_index()
        le = LabelEncoder()
        df['gender'] = le.fit_transform(df['gender'])
        df['nationality'] = le.fit_transform(df['nationality'])
        
        X = df[['user_id', 'gender','nationality','age', 'french','chinese','jpan','italian','greek','indian','spain','lebanan','moroccan','turkish','thai']]
        y = df[['TORTELLINI','PESCE','CARNE','GNOCCHI','PIZZA','RISO','FORMAGGI','LEGUMI','VERDURE','INTERIORA','FUNGHI','CROSTACEI_E_MOLLUSCHI','PASTA','SALUMI']]
        user_ids = X['user_id']
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=random_state)
        dict_test = self.get_preference_dict(X_test, y_test)
        CF_score = self.CF_test(X_test, y_test, dict_test)
        
        
        X_train, y_train = self.transformer(X_train, y_train)
        X_test, y_test = self.transformer(X_test, y_test)
        # CF_score = self.test_prepration(self.SVM((X_train.drop('user_id', axis=1)),np.array(y_train).ravel()), X_test, y_test, dict_test)
        
        if model == 'SVM':
            SVM_score = self.test_prepration(self.SVM((X_train.drop('user_id', axis=1)),np.array(y_train).ravel()), X_test, y_test, dict_test)
            return CF_score, SVM_score
        elif model == 'LR':
            LR_score = self.test_prepration(self.Logistic_remembering_expansion_ovr((X_train.drop('user_id', axis=1)),np.array(y_train).ravel()), X_test, y_test, dict_test)
            return CF_score, LR_score
        elif model == 'MLP':
            MLP_score = self.test_prepration(self.MLP((X_train.drop('user_id', axis=1)),np.array(y_train).ravel()), X_test, y_test, dict_test)
            return CF_score, MLP_score
        elif model == 'QDA':
            QDA_score = self.test_prepration(self.QDA((X_train.drop('user_id', axis=1)),np.array(y_train).ravel()), X_test, y_test, dict_test)
            return CF_score, QDA_score
        elif model == 'Ada':
            Ada_score = self.test_prepration(self.AdaBoost((X_train.drop('user_id', axis=1)),np.array(y_train).ravel()), X_test, y_test, dict_test)
            return CF_score, Ada_score
        elif model == 'RF':
            RF_score = self.test_prepration(self.random_forest((X_train.drop('user_id', axis=1)),np.array(y_train).ravel()), X_test, y_test, dict_test)
            return CF_score, RF_score
        elif model == 'GaussianNB':
            GaussianNB_score = self.test_prepration(self.GaussianNB((X_train.drop('user_id', axis=1)),np.array(y_train).ravel()), X_test, y_test, dict_test)
            return CF_score, GaussianNB_score
        elif model == 'Gaussian':
            Gaussian_score = self.test_prepration(self.Gaussian((X_train.drop('user_id', axis=1)),np.array(y_train).ravel()), X_test, y_test, dict_test)

            return CF_score, Gaussian_score
        elif model == 'KNN':
            KNN_score = self.test_prepration(self.KNN((X_train.drop('user_id', axis=1)),np.array(y_train).ravel()), X_test, y_test, dict_test)
            return CF_score, KNN_score
        elif model == 'DT':
            DT_score = self.test_prepration(self.DT((X_train.drop('user_id', axis=1)),np.array(y_train).ravel()), X_test, y_test, dict_test)
            return CF_score, DT_score
        else:
            return 0, 0
       
    def test_prepration(self, clf, X_test, y_test, dict_test):
        # print('SVM accuracy',accuracy_score(clf.predict(X_test.drop('user_id', axis=1)), y_test))
        prediction_list = []
        decision_values = clf.predict_proba(X_test.drop('user_id', axis=1))
        probabilities = 1 / (1 + np.exp(-decision_values))
        prediction_list = np.flip(np.argsort(probabilities, axis=1))
        prediction_list_final = self.classs_label_update(prediction_list, clf.classes_)
        self.hit_score(2, X_test, y_test, prediction_list_final, dict_test)
        # return self.P_1_score(X_test, y_test, prediction_list_final, dict_test)
        # return self.P_2_score(X_test, y_test, prediction_list_final, dict_test)
        # return self.R_2_score(X_test, y_test, prediction_list_final, dict_test)
        # For learning graph
        return [self.P_1_score(X_test, y_test, prediction_list_final, dict_test), self.P_2_score(X_test, y_test, prediction_list_final, dict_test), self.R_1_score(X_test, y_test, prediction_list_final, dict_test), self.R_2_score(X_test, y_test, prediction_list_final, dict_test)]
        
    def CF_test(self, X_test, y_test, dict_test):
        prediction_list = []
        prediction_list_first = []
        for row in X_test.drop('user_id', axis=1).to_dict("rows"):
            X_cleaned_dict = dict()
            for key in row.keys():
                X_cleaned_dict[key[0]] = row[key]
            predictions = list(self.remembering_expansion(X_cleaned_dict).keys())
            prediction_list.append(predictions)
            prediction_list_first.append(predictions[0])
        # print('Similarity after transformation accuracy',accuracy_score(prediction_list_first, y_test))
        self.hit_score(2, X_test, y_test, prediction_list, dict_test)
        # return self.P_1_score(X_test, y_test, prediction_list, dict_test)
        return [self.P_1_score(X_test, y_test, prediction_list, dict_test), self.P_2_score(X_test, y_test, prediction_list, dict_test),  self.R_1_score(X_test, y_test, prediction_list, dict_test), self.R_2_score(X_test, y_test, prediction_list, dict_test)]
        
    def classs_label_update(self, prediction_list, classes):
        prediction_list_final = []
        for predictions in prediction_list:
            predicted_list = []
            for predicted_item in predictions:
                predicted_list.append(classes[predicted_item])
            prediction_list_final.append(predicted_list)
        return prediction_list_final
       
    def transformer(self, X_train, y_train):
        df_out = pd.DataFrame(columns=[['user_id','gender','nationality','age', 'french','chinese','jpan','italian','greek','indian','spain','lebanan','moroccan','turkish','thai', 'class']])
        df_in =  pd.concat([X_train,y_train], axis=1)
        for index, row in df_in.iterrows():
            # TORTELLINI class: 1
            # PESCE class: 2
            # CARNE class: 3
            # GNOCCHI class: 4
            # PIZZA class: 5
            # RISO class: 6
            # FORMAGGI class: 7
            # LEGUMI class: 8
            # VERDURE class: 9
            # INTERIORA class: 10 
            # FUNGHI class: 11 
            # CROSTACEI_E_MOLLUSCHI class: 12
            # PASTA class: 13
            # SALUMI class: 14
            #     for index, row in df_in.iterrows():
            #         if (food_name === "FORMAGGI") {
            #     return "CHEESE";
            #   } else if (food_name === "VERDURE") {
            #     return "SALAD";
            #   } else if (food_name === "FUNGHI") {
            #     return "MASHROOM";
            #   } else if (food_name === "PESCE") {
            #     return "FISH";
            #   } else if (food_name === "RISO") {
            #     return "RICE";
            #   } else if (food_name === "CARNE") {
            #     return "RED MEAT";
            #   } else if (food_name === "CROSTACEI_E_MOLLUSCHI") {
            #     return "BURGER";
            #   } else if (food_name === "GNOCCHI") {
            #     return "SOUP";
            #   } else if (food_name === "CARNE") {
            #     return "RED MEAT";
            #   } else if (food_name === "TORTELLINI") {
            #     return "WHITE MEAT";
            #   } else if (food_name === "LEGUMI") {
            #     return "CHINESE NOODLE";
            #   } else {
            #     return food_name;
            #   }
            # TORTELLINI class: 1
            # PESCE class: 2
            # CARNE class: 3
            # GNOCCHI class: 4
            # PIZZA class: 5
            # RISO class: 6
            # FORMAGGI class: 7
            # LEGUMI class: 8
            # VERDURE class: 9
            # INTERIORA class: 10 
            # FUNGHI class: 11 
            # CROSTACEI_E_MOLLUSCHI class: 12
            # PASTA class: 13
            # SALUMI class: 14
            
            if row['TORTELLINI'] == 1:
                list_temp = row[['user_id', 'gender','nationality', 'age', 'french','chinese','jpan','italian','greek','indian','spain','lebanan','moroccan','turkish','thai']].to_list()
                list_temp.append('1')
                df_out = df_out.append(pd.DataFrame([list_temp], columns=[['user_id', 'gender','nationality', 'age', 'french','chinese','jpan','italian','greek','indian','spain','lebanan','moroccan','turkish','thai', 'class']]))
            if row['PESCE'] == 1:
                list_temp = row[['user_id', 'gender','nationality', 'age', 'french','chinese','jpan','italian','greek','indian','spain','lebanan','moroccan','turkish','thai']].to_list()
                list_temp.append('2')
                df_out = df_out.append(pd.DataFrame([list_temp], columns=[['user_id', 'gender','nationality', 'age', 'french','chinese','jpan','italian','greek','indian','spain','lebanan','moroccan','turkish','thai', 'class']]))
            if row['CARNE'] == 1:
                list_temp = row[['user_id', 'gender','nationality', 'age', 'french','chinese','jpan','italian','greek','indian','spain','lebanan','moroccan','turkish','thai']].to_list()
                list_temp.append('3')
                df_out = df_out.append(pd.DataFrame([list_temp], columns=[['user_id', 'gender','nationality', 'age', 'french','chinese','jpan','italian','greek','indian','spain','lebanan','moroccan','turkish','thai', 'class']]))
            if row['GNOCCHI'] == 1:
                list_temp = row[['user_id', 'gender','nationality', 'age', 'french','chinese','jpan','italian','greek','indian','spain','lebanan','moroccan','turkish','thai']].to_list()
                list_temp.append('4')
                df_out = df_out.append(pd.DataFrame([list_temp], columns=[['user_id', 'gender','nationality', 'age', 'french','chinese','jpan','italian','greek','indian','spain','lebanan','moroccan','turkish','thai', 'class']]))
            if row['PIZZA'] == 1:
                list_temp = row[['user_id', 'gender','nationality', 'age', 'french','chinese','jpan','italian','greek','indian','spain','lebanan','moroccan','turkish','thai']].to_list()
                list_temp.append('5')
                df_out = df_out.append(pd.DataFrame([list_temp], columns=[['user_id', 'gender','nationality', 'age', 'french','chinese','jpan','italian','greek','indian','spain','lebanan','moroccan','turkish','thai', 'class']]))
            if row['RISO'] == 1:
                list_temp = row[['user_id', 'gender','nationality', 'age', 'french','chinese','jpan','italian','greek','indian','spain','lebanan','moroccan','turkish','thai']].to_list()
                list_temp.append('6')
                df_out = df_out.append(pd.DataFrame([list_temp], columns=[['user_id', 'gender','nationality', 'age', 'french','chinese','jpan','italian','greek','indian','spain','lebanan','moroccan','turkish','thai', 'class']]))
            if row['FORMAGGI'] == 1:
                list_temp = row[['user_id', 'gender','nationality', 'age', 'french','chinese','jpan','italian','greek','indian','spain','lebanan','moroccan','turkish','thai']].to_list()
                list_temp.append('7')
                df_out = df_out.append(pd.DataFrame([list_temp], columns=[['user_id', 'gender','nationality', 'age', 'french','chinese','jpan','italian','greek','indian','spain','lebanan','moroccan','turkish','thai', 'class']]))
            if row['LEGUMI'] == 1:
                list_temp = row[['user_id', 'gender','nationality', 'age', 'french','chinese','jpan','italian','greek','indian','spain','lebanan','moroccan','turkish','thai']].to_list()
                list_temp.append('8')
                df_out = df_out.append(pd.DataFrame([list_temp], columns=[['user_id', 'gender','nationality', 'age', 'french','chinese','jpan','italian','greek','indian','spain','lebanan','moroccan','turkish','thai', 'class']]))
            if row['VERDURE'] == 1:
                list_temp = row[['user_id', 'gender','nationality', 'age', 'french','chinese','jpan','italian','greek','indian','spain','lebanan','moroccan','turkish','thai']].to_list()
                list_temp.append('9')
                df_out = df_out.append(pd.DataFrame([list_temp], columns=[['user_id', 'gender','nationality', 'age', 'french','chinese','jpan','italian','greek','indian','spain','lebanan','moroccan','turkish','thai', 'class']]))
            if row['INTERIORA'] == 1:
                list_temp = row[['user_id', 'gender','nationality', 'age', 'french','chinese','jpan','italian','greek','indian','spain','lebanan','moroccan','turkish','thai']].to_list()
                list_temp.append('10')
                df_out = df_out.append(pd.DataFrame([list_temp], columns=[['user_id', 'gender','nationality', 'age', 'french','chinese','jpan','italian','greek','indian','spain','lebanan','moroccan','turkish','thai', 'class']]))
            if row['FUNGHI'] == 1:
                list_temp = row[['user_id', 'gender','nationality', 'age', 'french','chinese','jpan','italian','greek','indian','spain','lebanan','moroccan','turkish','thai']].to_list()
                list_temp.append('11')
                df_out = df_out.append(pd.DataFrame([list_temp], columns=[['user_id', 'gender','nationality', 'age', 'french','chinese','jpan','italian','greek','indian','spain','lebanan','moroccan','turkish','thai', 'class']]))
            if row['CROSTACEI_E_MOLLUSCHI'] == 1:
                list_temp = row[['user_id', 'gender','nationality', 'age', 'french','chinese','jpan','italian','greek','indian','spain','lebanan','moroccan','turkish','thai']].to_list()
                list_temp.append('12')
                df_out = df_out.append(pd.DataFrame([list_temp], columns=[['user_id', 'gender','nationality', 'age', 'french','chinese','jpan','italian','greek','indian','spain','lebanan','moroccan','turkish','thai', 'class']]))
            if row['PASTA'] == 1:
                list_temp = row[['user_id', 'gender','nationality', 'age', 'french','chinese','jpan','italian','greek','indian','spain','lebanan','moroccan','turkish','thai']].to_list()
                list_temp.append('13')
                df_out = df_out.append(pd.DataFrame([list_temp], columns=[['user_id', 'gender','nationality', 'age', 'french','chinese','jpan','italian','greek','indian','spain','lebanan','moroccan','turkish','thai', 'class']]))
            if row['SALUMI'] == 1:
                list_temp = row[['user_id', 'gender','nationality', 'age', 'french','chinese','jpan','italian','greek','indian','spain','lebanan','moroccan','turkish','thai']].to_list()
                list_temp.append('14')
                df_out = df_out.append(pd.DataFrame([list_temp], columns=[['user_id', 'gender','nationality', 'age', 'french','chinese','jpan','italian','greek','indian','spain','lebanan','moroccan','turkish','thai', 'class']]))
        # df_out.to_csv('./OutPuts/1_train_test.csv')
        return df_out[['user_id', 'gender','nationality', 'french','chinese','jpan','italian','greek','indian','spain','lebanan','moroccan','turkish','thai']], df_out[['class']]
    
    def transformer_for_feature_selection(self, X_train, y_train):
        column_list_temp = X_train.columns
        column_list = []
        out_columns = []
        for item in column_list_temp:
            column_list.append(item)
            out_columns.append(item)
        out_columns.append('class')
        df_out = pd.DataFrame(columns=[out_columns])
        df_in =  pd.concat([X_train,y_train], axis=1)
        df_in.rename(columns={('TORTELLINI',):'TORTELLINI', ('PESCE',):'PESCE', ('CARNE',):'CARNE', ('GNOCCHI',):'GNOCCHI', ('PIZZA',):'PIZZA', ('RISO',):'RISO', ('FORMAGGI',):'FORMAGGI', ('LEGUMI',):'LEGUMI', ('VERDURE',):'VERDURE', ('INTERIORA',):'INTERIORA', ('FUNGHI',):'FUNGHI', ('CROSTACEI_E_MOLLUSCHI',):'CROSTACEI_E_MOLLUSCHI', ('PASTA',):'PASTA', ('SALUMI',):'SALUMI',}, inplace=True)
        for index, row in df_in.iterrows():
            # TORTELLINI class: 1
            # PESCE class: 2
            # CARNE class: 3
            # GNOCCHI class: 4
            # PIZZA class: 5
            # RISO class: 6
            # FORMAGGI class: 7
            # LEGUMI class: 8
            # VERDURE class: 9
            # INTERIORA class: 10 
            # FUNGHI class: 11 
            # CROSTACEI_E_MOLLUSCHI class: 12
            # PASTA class: 13
            # SALUMI class: 14
            #     for index, row in df_in.iterrows():
            #         if (food_name === "FORMAGGI") {
            #     return "CHEESE";
            #   } else if (food_name === "VERDURE") {
            #     return "SALAD";
            #   } else if (food_name === "FUNGHI") {
            #     return "MASHROOM";
            #   } else if (food_name === "PESCE") {
            #     return "FISH";
            #   } else if (food_name === "RISO") {
            #     return "RICE";
            #   } else if (food_name === "CARNE") {
            #     return "RED MEAT";
            #   } else if (food_name === "CROSTACEI_E_MOLLUSCHI") {
            #     return "BURGER";
            #   } else if (food_name === "GNOCCHI") {
            #     return "SOUP";
            #   } else if (food_name === "CARNE") {
            #     return "RED MEAT";
            #   } else if (food_name === "TORTELLINI") {
            #     return "WHITE MEAT";
            #   } else if (food_name === "LEGUMI") {
            #     return "CHINESE NOODLE";
            #   } else {
            #     return food_name;
            #   }
            # TORTELLINI class: 1
            # PESCE class: 2
            # CARNE class: 3
            # GNOCCHI class: 4
            # PIZZA class: 5
            # RISO class: 6
            # FORMAGGI class: 7
            # LEGUMI class: 8
            # VERDURE class: 9
            # INTERIORA class: 10 
            # FUNGHI class: 11 
            # CROSTACEI_E_MOLLUSCHI class: 12
            # PASTA class: 13
            # SALUMI class: 14
            
            if row['TORTELLINI'] == 1:
                list_temp = list(row[column_list])
                list_temp.append('1')
                df_out = df_out.append(pd.DataFrame([list_temp], columns=[out_columns]))
            if row['PESCE'] == 1:
                list_temp = list(row[column_list])
                list_temp.append('2')
                df_out = df_out.append(pd.DataFrame([list_temp], columns=[out_columns]))
            if row['CARNE'] == 1:
                list_temp = list(row[column_list])
                list_temp.append('3')
                df_out = df_out.append(pd.DataFrame([list_temp], columns=[out_columns]))
            if row['GNOCCHI'] == 1:
                list_temp = list(row[column_list])
                list_temp.append('4')
                df_out = df_out.append(pd.DataFrame([list_temp], columns=[out_columns]))
            if row['PIZZA'] == 1:
                list_temp = list(row[column_list])
                list_temp.append('5')
                df_out = df_out.append(pd.DataFrame([list_temp], columns=[out_columns]))
            if row['RISO'] == 1:
                list_temp = list(row[column_list])
                list_temp.append('6')
                df_out = df_out.append(pd.DataFrame([list_temp], columns=[out_columns]))
            if row['FORMAGGI'] == 1:
                list_temp = list(row[column_list])
                list_temp.append('7')
                df_out = df_out.append(pd.DataFrame([list_temp], columns=[out_columns]))
            if row['LEGUMI'] == 1:
                list_temp = list(row[column_list])
                list_temp.append('8')
                df_out = df_out.append(pd.DataFrame([list_temp], columns=[out_columns]))
            if row['VERDURE'] == 1:
                list_temp = list(row[column_list])
                list_temp.append('9')
                df_out = df_out.append(pd.DataFrame([list_temp], columns=[out_columns]))
            if row['INTERIORA'] == 1:
                list_temp = list(row[column_list])
                list_temp.append('10')
                df_out = df_out.append(pd.DataFrame([list_temp], columns=[out_columns]))
            if row['FUNGHI'] == 1:
                list_temp = list(row[column_list])
                list_temp.append('11')
                df_out = df_out.append(pd.DataFrame([list_temp], columns=[out_columns]))
            if row['CROSTACEI_E_MOLLUSCHI'] == 1:
                list_temp = list(row[column_list])
                list_temp.append('12')
                df_out = df_out.append(pd.DataFrame([list_temp], columns=[out_columns]))
            if row['PASTA'] == 1:
                list_temp = list(row[column_list])
                list_temp.append('13')
                df_out = df_out.append(pd.DataFrame([list_temp], columns=[out_columns]))
            if row['SALUMI'] == 1:
                list_temp = list(row[column_list])
                list_temp.append('14')
                df_out = df_out.append(pd.DataFrame([list_temp], columns=[out_columns]))
        # df_out.to_csv('./OutPuts/1_train_test.csv')
        return df_out[column_list], df_out[['class']]
        
    def transformer_partial(self, X_train, y_train):
        df_out = pd.DataFrame(columns=[['user_id','gender','nationality','age', 'class']])
        df_in =  pd.concat([X_train,y_train], axis=1)
        for index, row in df_in.iterrows():
            # TORTELLINI class: 1
            # PESCE class: 2
            # CARNE class: 3
            # GNOCCHI class: 4
            # PIZZA class: 5
            # RISO class: 6
            # FORMAGGI class: 7
            # LEGUMI class: 8
            # VERDURE class: 9
            # INTERIORA class: 10 
            # FUNGHI class: 11 
            # CROSTACEI_E_MOLLUSCHI class: 12
            # PASTA class: 13
            # SALUMI class: 14
            
            if row['TORTELLINI'] == 1:
                list_temp = row[['user_id','gender','nationality','age']].to_list()
                list_temp.append('1')
                df_out = df_out.append(pd.DataFrame([list_temp], columns=[['user_id','gender','nationality','age', 'class']]))
            if row['PESCE'] == 1:
                list_temp = row[['user_id','gender','nationality','age']].to_list()
                list_temp.append('2')
                df_out = df_out.append(pd.DataFrame([list_temp], columns=[['user_id','gender','nationality','age', 'class']]))
            if row['CARNE'] == 1:
                list_temp = row[['user_id','gender','nationality','age']].to_list()
                list_temp.append('3')
                df_out = df_out.append(pd.DataFrame([list_temp], columns=[['user_id','gender','nationality','age', 'class']]))
            if row['GNOCCHI'] == 1:
                list_temp = row[['user_id','gender','nationality','age']].to_list()
                list_temp.append('4')
                df_out = df_out.append(pd.DataFrame([list_temp], columns=[['user_id','gender','nationality','age', 'class']]))
            if row['PIZZA'] == 1:
                list_temp = row[['user_id','gender','nationality','age']].to_list()
                list_temp.append('5')
                df_out = df_out.append(pd.DataFrame([list_temp], columns=[['user_id','gender','nationality','age', 'class']]))
            if row['RISO'] == 1:
                list_temp = row[['user_id','gender','nationality','age']].to_list()
                list_temp.append('6')
                df_out = df_out.append(pd.DataFrame([list_temp], columns=[['user_id','gender','nationality','age', 'class']]))
            if row['FORMAGGI'] == 1:
                list_temp = row[['user_id','gender','nationality','age']].to_list()
                list_temp.append('7')
                df_out = df_out.append(pd.DataFrame([list_temp], columns=[['user_id','gender','nationality','age', 'class']]))
            if row['LEGUMI'] == 1:
                list_temp = row[['user_id','gender','nationality','age']].to_list()
                list_temp.append('8')
                df_out = df_out.append(pd.DataFrame([list_temp], columns=[['user_id','gender','nationality','age', 'class']]))
            if row['VERDURE'] == 1:
                list_temp = row[['user_id','gender','nationality','age']].to_list()
                list_temp.append('9')
                df_out = df_out.append(pd.DataFrame([list_temp], columns=[['user_id','gender','nationality','age', 'class']]))
            if row['INTERIORA'] == 1:
                list_temp = row[['user_id','gender','nationality','age']].to_list()
                list_temp.append('10')
                df_out = df_out.append(pd.DataFrame([list_temp], columns=[['user_id','gender','nationality','age', 'class']]))
            if row['FUNGHI'] == 1:
                list_temp = row[['user_id','gender','nationality','age']].to_list()
                list_temp.append('11')
                df_out = df_out.append(pd.DataFrame([list_temp], columns=[['user_id','gender','nationality','age', 'class']]))
            if row['CROSTACEI_E_MOLLUSCHI'] == 1:
                list_temp = row[['user_id','gender','nationality','age']].to_list()
                list_temp.append('12')
                df_out = df_out.append(pd.DataFrame([list_temp], columns=[['user_id','gender','nationality','age', 'class']]))
            if row['PASTA'] == 1:
                list_temp = row[['user_id','gender','nationality','age']].to_list()
                list_temp.append('13')
                df_out = df_out.append(pd.DataFrame([list_temp], columns=[['user_id','gender','nationality','age', 'class']]))
            if row['SALUMI'] == 1:
                list_temp = row[['user_id','gender','nationality','age']].to_list()
                list_temp.append('14')
                df_out = df_out.append(pd.DataFrame([list_temp], columns=[['user_id','gender','nationality','age', 'class']]))
        # df_out.to_csv('./OutPuts/1_train_test.csv')
        return df_out[['user_id','gender','nationality','age']], df_out[['class']]
        
    def get_preference_dict(self, X_train, y_train):
        
        df_out = pd.DataFrame(columns=[['user_id','gender','nationality','age', 'french','chinese','jpan','italian','greek','indian','spain','lebanan','moroccan','turkish','thai', 'class']])
        df_in =  pd.concat([pd.DataFrame(X_train),pd.DataFrame(y_train)], axis=1)
        preference_dict = dict()
        # df_in.rename(columns={('TORTELLINI',):'TORTELLINI', ('PESCE',):'PESCE', ('CARNE',):'CARNE', ('GNOCCHI',):'GNOCCHI', ('PIZZA',):'PIZZA', ('RISO',):'RISO', ('FORMAGGI',):'FORMAGGI', ('LEGUMI',):'LEGUMI', ('VERDURE',):'VERDURE', ('INTERIORA',):'INTERIORA', ('FUNGHI',):'FUNGHI', ('CROSTACEI_E_MOLLUSCHI',):'CROSTACEI_E_MOLLUSCHI', ('PASTA',):'PASTA', ('SALUMI',):'SALUMI',}, inplace=True)
        for index, row in df_in.iterrows():
            # TORTELLINI class: 1
            # PESCE class: 2
            # CARNE class: 3
            # GNOCCHI class: 4
            # PIZZA class: 5
            # RISO class: 6
            # FORMAGGI class: 7
            # LEGUMI class: 8
            # VERDURE class: 9
            # INTERIORA class: 10 
            # FUNGHI class: 11 
            # CROSTACEI_E_MOLLUSCHI class: 12
            # PASTA class: 13
            # SALUMI class: 14
            preference_dict[row['user_id']] = set()
            if row['TORTELLINI'] == 1:
                preference_dict[row['user_id']].add('1')
                
            if row['PESCE'] == 1:
                preference_dict[row['user_id']].add('2')
                
            if row['CARNE'] == 1:
                preference_dict[row['user_id']].add('3')
                
            if row['GNOCCHI'] == 1:
                preference_dict[row['user_id']].add('4')
                
            if row['PIZZA'] == 1:
                preference_dict[row['user_id']].add('5')
                
            if row['RISO'] == 1:
                preference_dict[row['user_id']].add('6')
                
            if row['FORMAGGI'] == 1:
                preference_dict[row['user_id']].add('7')
                
            if row['LEGUMI'] == 1:
                preference_dict[row['user_id']].add('8')
                
            if row['VERDURE'] == 1:
                preference_dict[row['user_id']].add('9')
                
            if row['INTERIORA'] == 1:
                preference_dict[row['user_id']].add('10')
                
            if row['FUNGHI'] == 1:
                preference_dict[row['user_id']].add('11')
                
            if row['CROSTACEI_E_MOLLUSCHI'] == 1:
                preference_dict[row['user_id']].add('12')
                
            if row['PASTA'] == 1:
                preference_dict[row['user_id']].add('13')
                
            if row['SALUMI'] == 1:
                preference_dict[row['user_id']].add('14')
                
        # df_out.to_csv('./OutPuts/1_train_test.csv')
        return preference_dict
        
    def get_df_user_data(self):
        df = pd.DataFrame(columns=[['user_id','gender','nationality','age','TORTELLINI','PESCE','CARNE','GNOCCHI','PIZZA','RISO','FORMAGGI','LEGUMI','VERDURE','INTERIORA','FUNGHI','CROSTACEI_E_MOLLUSCHI','PASTA','SALUMI','french','chinese','jpan','italian','greek','indian','spain','lebanan','moroccan','turkish','thai']])
        query = "SELECT user_id,gender,nationality,age,TORTELLINI,PESCE,CARNE,GNOCCHI,PIZZA,RISO,FORMAGGI,LEGUMI,VERDURE,INTERIORA,FUNGHI,CROSTACEI_E_MOLLUSCHI,PASTA,SALUMI,french,chinese,jpan,italian,greek,indian,spain,lebanan,moroccan,turkish,thai FROM user_info"
        my_cursor = self.my_cursor.cursor(buffered=True)
        my_cursor.execute(query)
        user_gender_dict = dict()
        user_nationality_dict = dict()
        user_age_dict = dict()
        user_preference_dict = dict()
        user_cuisine_dict = dict()
        for user in my_cursor:
            user_gender_dict[int(user[0])] = user[1]
            user_nationality_dict[int(user[0])] = user[2]
            user_age_dict[int(user[0])] = int(user[3])
            user_preference_dict[user[0]] = []
            user_cuisine_dict[user[0]] = []
            if int(user[4]):
                user_preference_dict[user[0]].append(1)
            else:
                user_preference_dict[user[0]].append(0)
            if int(user[5]):
                user_preference_dict[user[0]].append(1)
            else:
                user_preference_dict[user[0]].append(0)
            if int(user[6]):
                user_preference_dict[user[0]].append(1)
            else:
                user_preference_dict[user[0]].append(0)
            if int(user[7]):
                user_preference_dict[user[0]].append(1)
            else:
                user_preference_dict[user[0]].append(0)
            if int(user[8]):
                user_preference_dict[user[0]].append(1)
            else:
                user_preference_dict[user[0]].append(0)
            if int(user[9]):
                user_preference_dict[user[0]].append(1)
            else:
                user_preference_dict[user[0]].append(0)
            if int(user[10]):
                user_preference_dict[user[0]].append(1)
            else:
                user_preference_dict[user[0]].append(0)
            if int(user[11]):
                user_preference_dict[user[0]].append(1)
            else:
                user_preference_dict[user[0]].append(0)
            if int(user[12]):
                user_preference_dict[user[0]].append(1)
            else:
                user_preference_dict[user[0]].append(0)
            if int(user[13]):
                user_preference_dict[user[0]].append(1)
            else:
                user_preference_dict[user[0]].append(0)
            if int(user[14]):
                user_preference_dict[user[0]].append(1)
            else:
                user_preference_dict[user[0]].append(0)
            if int(user[15]):
                user_preference_dict[user[0]].append(1)
            else:
                user_preference_dict[user[0]].append(0)
            if int(user[16]):
                user_preference_dict[user[0]].append(1)
            else:
                user_preference_dict[user[0]].append(0)
            if int(user[17]):
                user_preference_dict[user[0]].append(1)
            else:
                user_preference_dict[user[0]].append(0)
            if int(user[18]):
                user_cuisine_dict[user[0]].append(1)
            else:
                user_cuisine_dict[user[0]].append(0)
            if int(user[19]):
                user_cuisine_dict[user[0]].append(1)
            else:
                user_cuisine_dict[user[0]].append(0)
            if int(user[20]):
                user_cuisine_dict[user[0]].append(1)
            else:
                user_cuisine_dict[user[0]].append(0)
            if int(user[21]):
                user_cuisine_dict[user[0]].append(1)
            else:
                user_cuisine_dict[user[0]].append(0)
            if int(user[22]):
                user_cuisine_dict[user[0]].append(1)
            else:
                user_cuisine_dict[user[0]].append(0)
            if int(user[23]):
                user_cuisine_dict[user[0]].append(1)
            else:
                user_cuisine_dict[user[0]].append(0)
            if int(user[24]):
                user_cuisine_dict[user[0]].append(1)
            else:
                user_cuisine_dict[user[0]].append(0)
            if int(user[25]):
                user_cuisine_dict[user[0]].append(1)
            else:
                user_cuisine_dict[user[0]].append(0)
            if int(user[26]):
                user_cuisine_dict[user[0]].append(1)
            else:
                user_cuisine_dict[user[0]].append(0)
            if int(user[27]):
                user_cuisine_dict[user[0]].append(1)
            else:
                user_cuisine_dict[user[0]].append(0)
            if int(user[28]):
                user_cuisine_dict[user[0]].append(1)
            else:
                user_cuisine_dict[user[0]].append(0)
            
            list_for_df = []
            list_for_df.append(user[0])
            list_for_df.append(user_gender_dict[int(user[0])])
            list_for_df.append(user_nationality_dict[int(user[0])])
            list_for_df.append(user_age_dict[int(user[0])])
            list_for_df.extend(user_preference_dict[int(user[0])])
            list_for_df.extend(user_cuisine_dict[int(user[0])])
            df = df.append(pd.DataFrame([list_for_df],columns=[['user_id','gender','nationality','age','TORTELLINI','PESCE','CARNE','GNOCCHI','PIZZA','RISO','FORMAGGI','LEGUMI','VERDURE','INTERIORA','FUNGHI','CROSTACEI_E_MOLLUSCHI','PASTA','SALUMI','french','chinese','jpan','italian','greek','indian','spain','lebanan','moroccan','turkish','thai']]))    
        # df.to_csv("./OutPuts/Preferences/user_preferences.csv")
        # print(df)
        return df
            
    def get_df_user_data_single_class(self):
        df = pd.DataFrame(columns=[['user_id','gender','nationality','age','class' ,'french','chinese','jpan','italian','greek','indian','spain','lebanan','moroccan','turkish','thai']])
        query = "SELECT user_id,gender,nationality,age,TORTELLINI,PESCE,CARNE,GNOCCHI,PIZZA,RISO,FORMAGGI,LEGUMI,VERDURE,INTERIORA,FUNGHI,CROSTACEI_E_MOLLUSCHI,PASTA,SALUMI,french,chinese,jpan,italian,greek,indian,spain,lebanan,moroccan,turkish,thai FROM user_info"
        my_cursor = self.my_cursor.cursor(buffered=True)
        my_cursor.execute(query)
        user_gender_dict = dict()
        user_nationality_dict = dict()
        user_age_dict = dict()
        user_preference_dict = dict()
        user_cuisine_dict = dict()
        for user in my_cursor:
            user_gender_dict[int(user[0])] = user[1]
            user_nationality_dict[int(user[0])] = user[2]
            user_age_dict[int(user[0])] = int(user[3])
            user_preference_dict[user[0]] = []
            user_cuisine_dict[user[0]] = []
            user_preference_list = []
            if int(user[4]):
                user_preference_list.append(self.food_name_change('TORTELLINI'))
            if int(user[5]):
                user_preference_list.append(self.food_name_change('PESCE'))
            if int(user[6]):
                user_preference_list.append(self.food_name_change('CARNE'))
            if int(user[7]):
                user_preference_list.append(self.food_name_change('GNOCCHI'))
            if int(user[8]):
                user_preference_list.append(self.food_name_change('PIZZA'))
            if int(user[9]):
                user_preference_list.append(self.food_name_change('RISO'))
            if int(user[10]):
                user_preference_list.append(self.food_name_change('FORMAGGI'))
            if int(user[11]):
                user_preference_list.append(self.food_name_change('LEGUMI'))
            if int(user[12]):
                user_preference_list.append(self.food_name_change('VERDURE'))
            if int(user[13]):
                user_preference_list.append(self.food_name_change('INTERIORA'))
            if int(user[14]):
                user_preference_list.append(self.food_name_change('FUNGHI'))
            if int(user[15]):
                user_preference_list.append(self.food_name_change('CROSTACEI_E_MOLLUSCHI'))
            if int(user[16]):
                user_preference_list.append(self.food_name_change('PASTA'))
            if int(user[17]):
                user_preference_list.append(self.food_name_change('SALUMI'))
            user_preference_dict[user[0]].append(user_preference_list)
            if int(user[18]):
                user_cuisine_dict[user[0]].append(1)
            else:
                user_cuisine_dict[user[0]].append(0)
            if int(user[19]):
                user_cuisine_dict[user[0]].append(1)
            else:
                user_cuisine_dict[user[0]].append(0)
            if int(user[20]):
                user_cuisine_dict[user[0]].append(1)
            else:
                user_cuisine_dict[user[0]].append(0)
            if int(user[21]):
                user_cuisine_dict[user[0]].append(1)
            else:
                user_cuisine_dict[user[0]].append(0)
            if int(user[22]):
                user_cuisine_dict[user[0]].append(1)
            else:
                user_cuisine_dict[user[0]].append(0)
            if int(user[23]):
                user_cuisine_dict[user[0]].append(1)
            else:
                user_cuisine_dict[user[0]].append(0)
            if int(user[24]):
                user_cuisine_dict[user[0]].append(1)
            else:
                user_cuisine_dict[user[0]].append(0)
            if int(user[25]):
                user_cuisine_dict[user[0]].append(1)
            else:
                user_cuisine_dict[user[0]].append(0)
            if int(user[26]):
                user_cuisine_dict[user[0]].append(1)
            else:
                user_cuisine_dict[user[0]].append(0)
            if int(user[27]):
                user_cuisine_dict[user[0]].append(1)
            else:
                user_cuisine_dict[user[0]].append(0)
            if int(user[28]):
                user_cuisine_dict[user[0]].append(1)
            else:
                user_cuisine_dict[user[0]].append(0)
            
            
            for preference in user_preference_list:
                list_for_df = []
                list_for_df.append(user[0])
                list_for_df.append(user_gender_dict[int(user[0])])
                list_for_df.append(user_nationality_dict[int(user[0])])
                list_for_df.append(user_age_dict[int(user[0])])
                list_for_df.append(preference)
                list_for_df.extend(user_cuisine_dict[int(user[0])])
                df = df.append(pd.DataFrame([list_for_df],columns=[['user_id','gender','nationality','age', 'class', 'french','chinese','jpan','italian','greek','indian','spain','lebanan','moroccan','turkish','thai']]))  
        # df = df.drop_duplicates(subset=["user_id"])
        # df.to_csv("./OutPuts/Preferences/user_preferences_single.csv")
        # print(df)
        return df
    
    
    def hit_score(self, length, x, y, predictions, dict_test):
        prediction_list = [[item] for item in predictions]
        df = pd.concat([x.reset_index(drop=True),y.reset_index(drop=True),pd.DataFrame(prediction_list, columns=[('predicts',)])], axis=1)
        df.columns = [s[0] for s in df.columns]
        df = df.drop_duplicates(subset=['user_id'.strip()])
        hitted_predictions = 0
        all_predictions = 0
        
        for index,row in df.iterrows():
            if str(row['predicts'][0]) in dict_test[row['user_id']] or str(row['predicts'][1]) in dict_test[row['user_id']]:
                hitted_predictions += 1
            else:
                # print(row)
                # print()
                # input()
                pass
            # print(str(row['predicts'][0]), str(row['predicts'][1]), dict_test[row['user_id']])
            all_predictions += 1
        # print('OR', hitted_predictions/all_predictions)
        hitted_predictions = 0
        all_predictions = 0
        for index,row in df.iterrows():
            if str(row['predicts'][0]) in dict_test[row['user_id']] and str(row['predicts'][1]) in dict_test[row['user_id']]:
                hitted_predictions += 1
            else:
                pass
            all_predictions += 1
        # print('AND', hitted_predictions/all_predictions)
        
        dict_size = 0
        hitted_predictions = 0
        all_predictions = 0
        for index,row in df.iterrows():
            dict_size += len(dict_test[row['user_id']])
            if str(row['predicts'][0]) in dict_test[row['user_id']]:
                hitted_predictions += 1
            else:
                pass
            all_predictions += 1
    
    def food_name_change(self,food_name):
      if (food_name == "FORMAGGI"):
        return "CHEESE"
      elif (food_name == "VERDURE"):
        return "SALAD"
      elif (food_name == "FUNGHI") :
        return "MASHROOM"
      elif (food_name == "PESCE"):
        return "FISH"
      elif (food_name == "RISO"):
        return "RICE"
      elif (food_name == "CARNE"):
        return "RED MEAT"
      elif (food_name == "CROSTACEI_E_MOLLUSCHI"):
        return "BURGER"
      elif (food_name == "GNOCCHI"):
        return "SOUP"
      elif (food_name == "CARNE"):
        return "RED MEAT"
      elif (food_name == "TORTELLINI"):
        return "WHITE MEAT"
      elif (food_name == "LEGUMI"):
        return "CHINESE NOODLE"
      else:
        return food_name
    
    def P_1_score(self, x, y, predictions, dict_test):
        prediction_list = [[item] for item in predictions]
        df = pd.concat([x.reset_index(drop=True),y.reset_index(drop=True),pd.DataFrame(prediction_list, columns=[('predicts',)])], axis=1)
        df.columns = [s[0] for s in df.columns]
        df = df.drop_duplicates(subset=['user_id'])
        hitted_predictions = []
        for index,row in df.iterrows():
            if str(row['predicts'][0]) in dict_test[row['user_id']]:
                hitted_predictions.append(1)
            else:
                hitted_predictions.append(0)
            # print(str(row['predicts'][0]), str(row['predicts'][1]), dict_test[row['user_id']])
        
        # print('P@1', np.average(hitted_predictions))
        return np.average(hitted_predictions)
        
    def P_2_score(self, x, y, predictions, dict_test):
        prediction_list = [[item] for item in predictions]
        df = pd.concat([x.reset_index(drop=True),y.reset_index(drop=True),pd.DataFrame(prediction_list, columns=[('predicts',)])], axis=1)
        df.columns = [s[0] for s in df.columns]
        df = df.drop_duplicates(subset=['user_id'])
        hitted_predictions = []
        
        for index,row in df.iterrows():
            if str(row['predicts'][0]) in dict_test[row['user_id']] and str(row['predicts'][1]) in dict_test[row['user_id']]:
                hitted_predictions.append(1)
            elif str(row['predicts'][0]) in dict_test[row['user_id']] or str(row['predicts'][1]) in dict_test[row['user_id']]:
                hitted_predictions.append(0.5)
            else:
                # print( str(row['predicts'][0]), str(row['predicts'][1]))
                # print(dict_test[row['user_id']])
                # input()
                hitted_predictions.append(0)
        # print('P@2', np.average(hitted_predictions))
        return np.average(hitted_predictions)
    
    def R_1_score(self, x, y, predictions, dict_test):
        prediction_list = [[item] for item in predictions]
        df = pd.concat([x.reset_index(drop=True),y.reset_index(drop=True),pd.DataFrame(prediction_list, columns=[('predicts',)])], axis=1)
        df.columns = [s[0] for s in df.columns]
        df = df.drop_duplicates(subset=['user_id'])
        hitted_predictions = []
        
        for index,row in df.iterrows():
            if str(row['predicts'][0]) in dict_test[row['user_id']]:
                hitted_predictions.append(1/len(dict_test[row['user_id']]))
            else:
                hitted_predictions.append(0)
                
        
        # print('R@2', np.average(hitted_predictions))
        return np.average(hitted_predictions)
    
    def R_2_score(self, x, y, predictions, dict_test):
        prediction_list = [[item] for item in predictions]
        df = pd.concat([x.reset_index(drop=True),y.reset_index(drop=True),pd.DataFrame(prediction_list, columns=[('predicts',)])], axis=1)
        df.columns = [s[0] for s in df.columns]
        df = df.drop_duplicates(subset=['user_id'])
        hitted_predictions = []
        
        for index,row in df.iterrows():
            if str(row['predicts'][0]) in dict_test[row['user_id']] and str(row['predicts'][1]) in dict_test[row['user_id']]:
                hitted_predictions.append(2/len(dict_test[row['user_id']]))
            elif str(row['predicts'][0]) in dict_test[row['user_id']] or str(row['predicts'][1]) in dict_test[row['user_id']]:
                hitted_predictions.append(1/len(dict_test[row['user_id']]))
            else:
                hitted_predictions.append(0)
        # print('R@2', np.average(hitted_predictions))
        return np.average(hitted_predictions)
    
    def sign_test_scores(self):
        np.random.seed(0)
        random_state_list = np.random.randint(30, size=10)
        model_list = ['SVM', 'LR', 'MLP', 'QDA', 'Ada', 'RF', 'GaussianNB', 'KNN', 'DT']
        # model_list = ['Gaussian']
        for model in model_list:
            baseline_scores_P1 = []
            model_scores_P1 = []
            baseline_scores_P2 = []
            model_scores_P2 = []
            baseline_scores_R1 = []
            model_scores_R1 = []
            baseline_scores_R2 = []
            model_scores_R2 = []
            for ranodm_state in random_state_list:
                scores = self.train_test_sign(ranodm_state, model)
                print(scores)
                baseline_scores_P1.append(scores[0][0])
                model_scores_P1.append(scores[1][0])
                baseline_scores_P2.append(scores[0][1])
                model_scores_P2.append(scores[1][1])
                baseline_scores_R1.append(scores[0][2])
                model_scores_R1.append(scores[1][2])
                baseline_scores_R2.append(scores[0][3])
                model_scores_R2.append(scores[1][3])
            print(model)
            print(np.mean(baseline_scores_P1))
            print(np.mean(model_scores_P1))
            print(wilcoxon(baseline_scores_P1, model_scores_P1, alternative="greater"))
            print()
            print(np.mean(baseline_scores_P2))
            print(np.mean(model_scores_P2))
            print(wilcoxon(baseline_scores_P2, model_scores_P2, alternative="greater"))
            print()
            print(np.mean(baseline_scores_R1))
            print(np.mean(model_scores_R1))
            print(wilcoxon(baseline_scores_R1, model_scores_R1, alternative="greater"))
            print()
            print(np.mean(baseline_scores_R2))
            print(np.mean(model_scores_R2))
            print(wilcoxon(baseline_scores_R2, model_scores_R2, alternative="greater"))
            input()
    
    def suggestion_usage(self):
        full_preferences_list = self.get_full_list_of_preferences()
        recalling_interval = self.get_recalling_interval()
        recommended_used = 0
        all_used = 0
        for item in full_preferences_list:
            if item['member'] in recalling_interval.keys():
                if recalling_interval[item['member']][0] != '0':
                    if recalling_interval[item['member']][1] == '0':
                        if str(item['time']) >= recalling_interval[item['member']][0]:
                            if item['type'] == 'PASTA' or item['type'] == 'PIZZA':
                                recommended_used += 1
                                all_used += 1
                            else:
                                all_used += 1
                    else:
                        if recalling_interval[item['member']][1] >= item['time'] >= recalling_interval[item['member']][0]:
                            if item['type'] == 'PASTA' or item['type'] == 'PIZZA':
                                recommended_used += 1
                                all_used += 1
                            else:
                                all_used += 1
  
    def get_full_list_of_preferences(self):
        df = pd.read_csv("OutPuts/preference_insertion_deleted_table_single.csv").drop_duplicates()
        preferences_list = []
        
        for index, row in df.iterrows():
            preference_dict = dict()
            preference_dict['member'] = row['user_id']
            preference_dict['type'] = row['preference']
            preference_dict['time'] = row['time']
            preferences_list.append(preference_dict)
        
        return preferences_list
    
    def get_recalling_interval(self):
        df_remember = pd.read_csv("OutPuts/organizer_remeber_single.csv")
        df_conflict = pd.read_csv("OutPuts/organizer_conflict_single.csv")
        usage_interval_dict = dict()
        for _,row in df_remember.iterrows():
            if row['for_user'] not in usage_interval_dict.keys():
                usage_interval_dict[row['for_user']] = [row['time'], '0']
            else:
                if usage_interval_dict[row['for_user']][0] > row['time']:
                   usage_interval_dict[row['for_user']] = [row['time'], '0'] 
                   
        for _,row in df_conflict.iterrows():
            if row['for_user'] not in usage_interval_dict.keys():
                usage_interval_dict[row['for_user']] = ['0', row['time']]
            else:
                if usage_interval_dict[row['for_user']][0] < row['time']:
                    if usage_interval_dict[row['for_user']][1] == '0':
                        usage_interval_dict[row['for_user']][1] = row['time'] 
                    elif usage_interval_dict[row['for_user']][1] > row['time']:
                        usage_interval_dict[row['for_user']][1] = row['time'] 
                   
        return usage_interval_dict
    
    def class_feature_correlation(self):
        """"Calculate class-feature correlation.
        return:
            a dictionary for each label-feature dictionary
        """
        column_list_categorical = ['gender','nationality']
        column_list_numerical = ['age','TORTELLINI','PESCE','CARNE','GNOCCHI','PIZZA','RISO','FORMAGGI','LEGUMI','VERDURE','INTERIORA','FUNGHI','CROSTACEI_E_MOLLUSCHI','PASTA','SALUMI','french','chinese','jpan','italian','greek','indian','spain','lebanan','moroccan','turkish','thai']
        
        df = self.get_df_user_data().drop(["user_id"], axis=1)
        df = self.convert_to_categorical(df, column_list_categorical)
        df = self.convert_to_int(df, column_list_numerical)
        
        correlation_with_class = df.corr()
        print(correlation_with_class)
    
    def class_feature_correlation_binary_continous(self):
        """"Calculate class-feature correlation. Features are only continous data (age)
        return:
            A matrix of correlation between the features and binary classes
        """
        column_list_categorical = ['gender','nationality']
        column_list_numerical = ['age','TORTELLINI','PESCE','CARNE','GNOCCHI','PIZZA','RISO','FORMAGGI','LEGUMI','VERDURE','INTERIORA','FUNGHI','CROSTACEI_E_MOLLUSCHI','PASTA','SALUMI','french','chinese','jpan','italian','greek','indian','spain','lebanan','moroccan','turkish','thai']
        
        df = self.get_df_user_data().drop(["user_id"], axis=1)
        df = self.convert_to_categorical(df, column_list_categorical)
        df = self.convert_to_int(df, column_list_numerical)
        
        features_list = ['age']
        classes_list = ['TORTELLINI','PESCE','CARNE','GNOCCHI','PIZZA','RISO','FORMAGGI','LEGUMI','VERDURE','INTERIORA','FUNGHI','CROSTACEI_E_MOLLUSCHI','PASTA','SALUMI']
        for feature in features_list:
            for class_ in classes_list:
                feature_value_list = [i[0] for i in df[feature].to_numpy()]
                class_value_list = [i[0] for i in df[class_].to_numpy()]
                correlation_with_class = stats.pointbiserialr(feature_value_list, class_value_list)
                print(f"Point Biserial correlation between {feature} and {class_} is {correlation_with_class}")
    
    def class_feature_correlation_binary_binary(self):
        """"Calculate class-feature correlation. Features are only continous data (age)
        return:
            A matrix of correlation between the features and binary classes
        """
        column_list_categorical = ['gender','nationality']
        column_list_numerical = ['age','TORTELLINI','PESCE','CARNE','GNOCCHI','PIZZA','RISO','FORMAGGI','LEGUMI','VERDURE','INTERIORA','FUNGHI','CROSTACEI_E_MOLLUSCHI','PASTA','SALUMI','french','chinese','jpan','italian','greek','indian','spain','lebanan','moroccan','turkish','thai']
        
        df = self.get_df_user_data().drop(["user_id"], axis=1)
        df = self.convert_to_categorical(df, column_list_categorical)
        df = self.convert_to_int(df, column_list_numerical)
        
        features_list = ['gender','french','chinese','jpan','italian','greek','indian','spain','lebanan','moroccan','turkish','thai']
        classes_list = ['TORTELLINI','PESCE','CARNE','GNOCCHI','PIZZA','RISO','FORMAGGI','LEGUMI','VERDURE','INTERIORA','FUNGHI','CROSTACEI_E_MOLLUSCHI','PASTA','SALUMI']
        for feature in features_list:
            for class_ in classes_list:
                feature_value_list = [i[0] for i in df[feature].to_numpy()]
                class_value_list = [i[0] for i in df[class_].to_numpy()]
                correlation_with_class = distance.jaccard(feature_value_list, class_value_list)
                print(f"Jaccard similarity between {feature} and {class_} is {1 - correlation_with_class}")

    def class_feature_correlation_binary_categorical(self):
        """"Calculate class-feature correlation. Features are only continous data (age)
        return:
            A matrix of correlation between the features and binary classes
        """
        column_list_categorical = ['gender','nationality']
        column_list_numerical = ['age','TORTELLINI','PESCE','CARNE','GNOCCHI','PIZZA','RISO','FORMAGGI','LEGUMI','VERDURE','INTERIORA','FUNGHI','CROSTACEI_E_MOLLUSCHI','PASTA','SALUMI','french','chinese','jpan','italian','greek','indian','spain','lebanan','moroccan','turkish','thai']
        
        df = self.get_df_user_data().drop(["user_id"], axis=1)
        # df = self.convert_to_categorical(df, column_list_categorical)
        # df = self.convert_to_int(df, column_list_numerical)
        
        features_list = ['nationality']
        classes_list = ['TORTELLINI','PESCE','CARNE','GNOCCHI','PIZZA','RISO','FORMAGGI','LEGUMI','VERDURE','INTERIORA','FUNGHI','CROSTACEI_E_MOLLUSCHI','PASTA','SALUMI']
        for feature in features_list:
            for class_ in classes_list:
                feature_value_list = [i[0] for i in df[feature].to_numpy()]
                class_value_list = [i[0] for i in df[class_].to_numpy()]
                x_series = pd.Series(feature_value_list)
                y_series = pd.Series(class_value_list)
                confusion_matrix = pd.crosstab(x_series, y_series)
                correlation_with_class = self.cramers_v(confusion_matrix)
                print(f"Cramer correlation between {feature} and {class_} is {correlation_with_class}")

    def cramers_v(self, confusion_matrix):
        chi2 = chi2_contingency(confusion_matrix)[0]
        n = confusion_matrix.sum().sum()
        phi2 = chi2 / n
        r, k = confusion_matrix.shape
        phi2corr = max(0, phi2 - ((k-1)*(r-1))/(n-1))
        rcorr = r - ((r-1)**2)/(n-1)
        kcorr = k - ((k-1)**2)/(n-1)
        return np.sqrt(phi2corr / min((kcorr-1), (rcorr-1)))

    def convert_to_categorical(self, df, column_list):
        for column in column_list:
            categories = list(set([i[0] for i in df[column].values]))
            cat_type = CategoricalDtype(categories=categories, ordered=True)
            df.loc[:, column] = df[column].astype(cat_type)
        cat_columns = df.select_dtypes(['category']).columns
        df[cat_columns] = df[cat_columns].apply(lambda x: x.cat.codes)
        return df
    
    def convert_to_int(self, df, column_list):
        for column in column_list:
            df[column] = df[column].astype(int)
        return df
    
    def single_class_correlation(self):
        column_list_categorical = ['gender','nationality', 'class']
        column_list_numerical = ['age', 'french','chinese','jpan','italian','greek','indian','spain','lebanan','moroccan','turkish','thai']
        df = self.get_df_user_data_single_class().drop(["user_id"], axis=1)
        df = self.convert_to_categorical(df, column_list_categorical)
        df = self.convert_to_int(df, column_list_numerical)
        correlation_with_class = df.corr(method = 'kendall')
        # print(correlation_with_class)
        
    def class_feature_correlation_categorical_categorical(self):
        """"Calculate class-feature correlation. Features are only continous data (age)
        return:
            A matrix of correlation between the features and binary classes
        """
        column_list_categorical = ['gender','nationality', 'class']
        column_list_numerical = ['age', 'french','chinese','jpan','italian','greek','indian','spain','lebanan','moroccan','turkish','thai']
        df = self.get_df_user_data_single_class().drop(["user_id"], axis=1)
        df = self.convert_to_categorical(df, column_list_categorical)
        df = self.convert_to_int(df, column_list_numerical)
        
        features_list = ['age','gender','nationality', 'french','chinese','jpan','italian','greek','indian','spain','lebanan','moroccan','turkish','thai']
        classes_list = ['class']
        for feature in features_list:
            for class_ in classes_list:
                feature_value_list = [i[0] for i in df[feature].to_numpy()]
                class_value_list = [i[0] for i in df[class_].to_numpy()]
                x_series = pd.Series(feature_value_list)
                y_series = pd.Series(class_value_list)
                confusion_matrix = pd.crosstab(x_series, y_series)
                correlation_with_class = self.cramers_v(confusion_matrix)
                print(f"Cramer correlation between {feature} and {class_} is {correlation_with_class}")
    
    