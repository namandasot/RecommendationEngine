from KNN_Search import KNN_Search
from sklearn.neighbors import NearestNeighbors
import numpy as np
import MySQLdb
import time
import datetime
import os

class DataCleaner:
    def __init__(self):
        self.aminity_class = self.aminites_class_reader()
        self.workable_data, self.project_city = self.get_workable_data()
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
        aminitie = []
        category = []
        db = MySQLdb.connect(host="127.0.0.1", port=3306, user="root", db="REDADMIN2")
        cur = db.cursor()
        cur.execute("select Project_config_No, Project_City_Name, Map_Latitude, Map_Longitude, Built_Up_Area, No_Of_Balconies, No_Of_Bedroom, No_Of_Bathroom, Minimum_Price, Category, Possession, PricePerUnit, amenities from REDADMIN2.all_project_info")
        for row in cur.fetchall():
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
        return data_dict, project_city_dict

    def get_workable_data(self):
        organised_data, project_city_dict = self.connect_data()
        for city in organised_data:
            x = np.array(organised_data[city]['attributes']).astype(np.float)
            x_normed = (x - x.min(axis=0))/(x.max(axis=0)-x.min(axis=0))
            organised_data[city]['attributes'] = x_normed
        return organised_data, project_city_dict
    
    def get_weighted_x(self, X):
        weights = [50, 50, 2, 1, 10, 1, 75, 1, 1, 1, 1, 1, 2.5, 1, 1, 2, 1, 0.7]
        X *= weights
        return X

    def simple_knn_recommender(self, city, project_config_No):
        X = self.workable_data[city]['attributes']
        X = self.get_weighted_x(X)
        
        #X_clicked = X[self.workable_data[city]['project_id'].index(project_config_No)]

        X_clicked2 = [X[self.workable_data[city]['project_id'].index(num)] for num in project_config_No]
        results = self.KNN.get_optimum_neighbours(X, X_clicked2)
        final_output = [self.workable_data[city]['project_id'][ele] for ele in results[:100]]
        return final_output

    def get_recommendations(self, project_config_No):
        #city = self.project_city.get(project_config_No)
        cities = self.project_city.get(project_config_No[0])
        Recommendation_list = self.simple_knn_recommender(cities, project_config_No)
        return Recommendation_list


if __name__ == '__main__':
    mum = []
    DC = DataCleaner()
    lis = [37961L,7L, 19279L,24334L]
    b = DC.get_recommendations(lis)
    print b
