import copy
from KNN_Search import KNN_Search
from sklearn.neighbors import NearestNeighbors
import numpy as np
import MySQLdb
import time
import datetime
import os
import pprint

class DataCleaner:
    def __init__(self):
        self.aminity_class = self.aminites_class_reader()
        self.workable_data, self.project_city, self.project_config = self.get_workable_data()
        self.KNN = KNN_Search()

    def aminites_class_reader(self):
        amneties_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'aminities_class.txt')
        fil = open(amneties_file).read().strip().split('\n')
        aminity_class = {}
        for line in fil:
            line = line.split('|')
            aminity_class[line[0].lower().strip()] = line[1].lower().strip()
        return aminity_class

    def aminities_cleaner(self, text):
        if text:
            text = text.split(',')
            text = [x.strip().lower() for x in text if len(x)>1]
            return text
        else:
            return []

    def process_possession(self, text_date):
        try:
            possion_days = (datetime.date.today() - text_date).days
            if possion_days <= 0:
                possion_days = 0
            return float(possion_days)
        except:
            return 0.0

    def connect_data(self):
        data_dict = {}
        project_id_dict = {}
        project_city_dict = {}
        project_config_dict = {}
        aminitie = []
        category = []
        db = MySQLdb.connect(host="127.0.0.1", port=3306, user="root", db="REDADMIN2")
        cur = db.cursor()
        cur.execute("select Project_No, Project_config_No, Project_City_Name, Map_Latitude, Map_Longitude, Built_Up_Area, No_Of_Balconies, No_Of_Bedroom, No_Of_Bathroom, Minimum_Price, Category, Possession, PricePerUnit, amenities from REDADMIN2.all_project_info")
        for row1 in cur.fetchall():
            project_config_dict[row1[1]] = row1[0]
            row = row1[1:]
            if not data_dict.has_key(row[1]):
                data_dict[row[1]] = {'project_id':[], 'attributes':[]}
            aminities = row[-1]
            category.append(row[-3])
            aminitie = self.aminities_cleaner(aminities)
            class_list = [self.aminity_class.get(x, '') for x in aminitie]
            class_list = list(set(class_list))
            class_list = [x for x in class_list if x != '']
            aminities_class_list =['garden', 'gym', 'outdoor sports', 'swimming pool', 'vastu', 'recreational activities', 'parking', 'health care', 'gas pipelines']
            row = list(row[:-2])
            row[-1] = self.process_possession(row[-1])
            for aminity in aminities_class_list:
                if aminity in class_list:
                    row.append(1)
                else:
                    row.append(0)
            project_city_dict[row[0]] = row[1]
            data_dict[row[1]]['project_id'].append(row[0])
            r = []
            for val in row[2:]:
                if val in ['', 'NONE']:
                    r.append(0.0)
                elif val == 'AFFORDABLE':
                     r.append(1.0)
                elif val == 'MID_RANGE':
                    r.append(2.0)
                elif val == 'MID_RANGE':
                    r.append(3.0)
                else:
                    try:
                        r.append(float(val))
                    except:
                        r.append(0.0)
            data_dict[row[1]]['attributes'].append(r)
        return data_dict, project_city_dict, project_config_dict

    def get_workable_data(self):
        organised_data, project_city_dict, project_config_dict = self.connect_data()
        for city in organised_data:
            x = np.array(organised_data[city]['attributes']).astype(np.float)
            x_normed = (x - x.min(axis=0))/(x.max(axis=0)-x.min(axis=0))
            organised_data[city]['attributes'] = x_normed
        return organised_data, project_city_dict, project_config_dict

    def get_weighted_x(self, X):
        #mumbai = [300, 300, 2, 0, 10, 1, 100, 1, 1, 1, 1, 1, 5.5, 1, 0, 2, 0, 0.7]
        weights = [9, 9, 2.5, 0, 1.5, 1, 8, 1.1, 0.9, 0.6, 0.6, 0.6, 1, 0.6, 0, 0.5, 0, 0.5]
        stdev = np.ndarray.std(X, 0)
        X /= stdev
        X *= weights
        return X

    def get_reweighted(self, X, X_clicked):
        click_stdev = np.ndarray.std(np.array(X_clicked),0)
        print X
        print '<><><><>'
        print click_stdev
        X = X / (click_stdev+1)
        print '<><><><>'
        print X
        return X

    def simple_knn_recommender(self, city, project_config_No):
        X1 = self.workable_data[city]['attributes']
        X = copy.deepcopy(X1)
        X = self.get_weighted_x(X)
        X_clicked2 = []
        for num in project_config_No:
            configs_index = self.workable_data[city]['project_id'].index(num)
            x_clic = X[configs_index]
            X_clicked2.append(x_clic)
        X = self.get_reweighted(X, X_clicked2)
        
        X_clicked3 = []
        for num in project_config_No:
            configs_index = self.workable_data[city]['project_id'].index(num)
            x_clic = X[configs_index]
            X_clicked3.append(x_clic)
        
        results = self.KNN.get_optimum_neighbours(X, X_clicked3)

        final_output = [self.workable_data[city]['project_id'][ele] for ele in results[:100]]
        return final_output

    def get_recommendations(self, project_config_No):
        #city = self.project_city.get(project_config_No)
        cities = self.project_city.get(project_config_No[0])
        Recommendation_list = self.simple_knn_recommender(cities, project_config_No)
        final_reults = self.reco_filter(Recommendation_list)
        final_reults = [x for x in final_reults if x not in project_config_No]
        return final_reults

    def reco_filter(self, reco_list):
        filtered_reco_list = []
        reco_project_list = []
        for ele in reco_list:
            project_of_config = self.project_config.get(ele)
            if project_of_config not in reco_project_list:
                filtered_reco_list.append(ele)
                reco_project_list.append(project_of_config)
        return filtered_reco_list


if __name__ == '__main__':
    mum = []
    DC = DataCleaner()
    lis = [13, 19274L]
    b = DC.get_recommendations(lis)
    lis = [13, 13]
    c = DC.get_recommendations(lis)
