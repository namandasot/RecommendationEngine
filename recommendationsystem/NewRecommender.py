import copy
from KNN_Search import KNN_Search
from sklearn.neighbors import NearestNeighbors
import numpy as np
import MySQLdb
import time
import datetime
import os
import pprint

#from hdfcredrecoengine.settings import HOSTIP, HOSTUSER, HOSTPASWD
HOSTIP = '52.35.25.23'
HOSTUSER = 'ITadmin'
HOSTPASWD = 'ITadmin'

class DataCleaner:
    def __init__(self):
        self.aminity_class = self.aminites_class_reader()
        self.workable_data, self.project_city, self.project_config, self.normalization_factors, self.stdev_city = self.get_workable_data()
        self.weights = [9, 9, 2.5, 0, 1.5, 1, 8, 0, 0.9/3, 0.6/3, 0.6/3, 0.6/3, 1/3, 0.6/3, 0, 0.5/3, 0, 0.5/3]
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

    def process_row(self, row1, data_dict, project_city_dict, project_config_dict, category, process_poss=True):
        project_config_dict[row1[1]] = row1[0]
        row1 = list(row1)
        row1[2] = row1[2].lower()
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
        if process_poss == True:
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
        return data_dict, project_city_dict, project_config_dict, category

    def connect_data(self):
        data_dict = {}
        project_id_dict = {}
        project_city_dict = {}
        project_config_dict = {}
        aminitie = []
        category = []
        db = MySQLdb.connect(HOSTIP, HOSTUSER, HOSTPASWD,"REDADMIN2" )
#         db = MySQLdb.connect(host=HOSTIP, port=3306, user=HOSTUSER, db="REDADMIN2",pwd = HOSTPASWD)
        cur = db.cursor()
        cur.execute("select Project_No, Project_config_No, Project_City_Name, Map_Latitude, Map_Longitude, Built_Up_Area, No_Of_Balconies, No_Of_Bedroom, No_Of_Bathroom, Minimum_Price, Category, Possession, PricePerUnit, amenities from REDADMIN2.all_project_info")
        for row1 in cur.fetchall():
            data_dict, project_city_dict, project_config_dict, category = self.process_row(row1, data_dict, project_city_dict, project_config_dict, category)
        return data_dict, project_city_dict, project_config_dict


    def get_workable_data(self):
        organised_data, project_city_dict, project_config_dict = self.connect_data()
        normalization_factors = {}
        stdev_city = {}
        for city in organised_data:
            x = np.array(organised_data[city]['attributes']).astype(np.float)
            x_normed = (x - x.min(axis=0))/(x.max(axis=0)-x.min(axis=0))
            stdev_city[city] = np.ndarray.std(x_normed, 0)

            normalization_factors[city] = {'x_min': x.min(axis=0), 'x_max':x.max(axis=0)}
            organised_data[city]['attributes'] = x_normed
        return organised_data, project_city_dict, project_config_dict, normalization_factors, stdev_city

    def get_weighted_x(self, X):
        #mumbai = [300, 300, 2, 0, 10, 1, 100, 1, 1, 1, 1, 1, 5.5, 1, 0, 2, 0, 0.7]
        stdev = np.ndarray.std(X, 0)
        X /= stdev
        X *= self.weights
        return X

    def get_reweighted(self, X, X_clicked):
        click_stdev = np.ndarray.std(np.array(X_clicked),0)
        X = X / (click_stdev+1)
        X_clicked = X_clicked/(click_stdev+1)
        return X, X_clicked, click_stdev

    def simple_knn_recommender(self, city, project_config_No):
        X1 = self.workable_data[city]['attributes']
        X = copy.deepcopy(X1)
        X = self.get_weighted_x(X)
        X_clicked2 = []
        project_config_No = [x for x in project_config_No if x in self.workable_data[city]['project_id']]
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

        final_output = [self.workable_data[city]['project_id'][ele] for ele in results[:200]]
        return final_output

    def get_recommendations(self, project_config_No):
        #city = self.project_city.get(project_config_No)
        cities = self.project_city.get(project_config_No[0])
        Recommendation_list = self.simple_knn_recommender(cities, project_config_No)
        final_reults = self.reco_filter(Recommendation_list, project_config_No)
        final_reults = [x for x in final_reults if x not in project_config_No]
        return final_reults

    def reco_filter(self, reco_list, project_config_No):
        filtered_reco_list = []
        reco_project_list = []
        existing = []
        for ele in project_config_No:
            project_of_config = self.project_config.get(ele)
            existing.append(project_of_config)

        for ele in reco_list:
            project_of_config = self.project_config.get(ele)
            if project_of_config not in reco_project_list + existing:
                filtered_reco_list.append(ele)
                reco_project_list.append(project_of_config)
        return filtered_reco_list


    def simple_knn_Search_recommender(self, city, search_X, project_config_No):
        X1 = self.workable_data[city]['attributes']
        X = copy.deepcopy(X1)
        X = self.get_weighted_x(X)
        X_clicked2 = []
        click_stdev = np.zeros(18)
        final_recommendations = []

        if len(project_config_No) > 0:
            project_config_No = [x for x in project_config_No if x in self.workable_data[city]['project_id']]
            for num in project_config_No:
                configs_index = self.workable_data[city]['project_id'].index(num)
                x_clic = X[configs_index]
                X_clicked2.append(x_clic)
            X, X_clicked2, click_stdev = self.get_reweighted(X, X_clicked2)
        
        for sear in search_X:

            re_weighted_sear = [sear]/(1+click_stdev)
            if len(project_config_No) > 0:
                re_weighted_sear = np.append(X_clicked2, re_weighted_sear, axis=0)
            results = self.KNN.get_optimum_neighbours(X,  re_weighted_sear)
            final_output = [self.workable_data[city]['project_id'][ele] for ele in results[:10000]]
            try:
                print 'INDEX', final_output.index(23516)
            except:
                pass
            final_reults = self.reco_filter(final_output, project_config_No)
            final_reults = [x for x in final_reults if x not in project_config_No]

            final_recommendations.append(final_reults)
        return final_recommendations

    def develop_dummy_listing(self, search_parameters, project_config_No, preferences):
        data_dict = {}
        project_city_dict = {}
        project_config_dict = {}
        category = []
        city1 = ''
        preferences.reverse()
        
        location_pref = 1.0 + (preferences.index('location') - 2.0)/10
        budget_pref = 1.0 + (preferences.index('budget') - 2.0)/10
        bhk_pref = 1.0 + (preferences.index('bhk') - 2.0)/10
        poss_pref = 1.0 + (preferences.index('possession') - 2.0)/10
        amenities_pref = 1.0 + (preferences.index('amenities') - 2.0)/10
#         poss_pref *= 2.0
        print location_pref,budget_pref,bhk_pref,poss_pref,amenities_pref
        #self.weights = [9, 9, 2.5, 0, 3, 1, 8, 0, 0.9/2, 0.6/3, 0.6/3, 0.6/3, 1/3, 0.1/3, 0, 0.09/3, 0, 0.09/3]
        self.weights = [6.5, 6.5, 2.5, 0, 3, 1, 7, 0, 0.8, 0.6/3, 0.6/3, 0.6/3, 1/3, 0.6/3, 0, 0.5/3, 0, 0.5/3]
        print self.weights
        self.weights[0] *= location_pref**3
        self.weights[1] *= location_pref
        self.weights[6] *= budget_pref
        self.weights[8] *= poss_pref
        self.weights[4] = bhk_pref * bhk_pref * self.weights[4]
        self.weights[9] *= amenities_pref
        self.weights[10] *= amenities_pref
        self.weights[11] *= amenities_pref
        self.weights[12] *= amenities_pref
        self.weights[13] *= amenities_pref
        self.weights[14] *= amenities_pref
        self.weights[15] *= amenities_pref
        self.weights[16] *= amenities_pref
        print self.weights
        for i, ele in enumerate(search_parameters):
            attributes = []
            ele['Project_config_No'] = 'search'+str(i)
            ele['amenities'] = ','.join(ele['amenities'])
            attribute_names = ['Project_No', 'Project_config_No', 'Project_City_Name', 'Map_Latitude', 'Map_Longitude', 'Built_Up_Area', 'No_Of_Balconies', 'No_Of_Bedroom', 'No_Of_Bathroom', 'Minimum_Price', 'Category', 'Possession', 'PricePerUnit', 'amenities']
            for attr in attribute_names:
                attributes.append(ele[attr])
            organised_dataa, project_city_dict, project_config_dict, category = self.process_row(attributes, data_dict, project_city_dict, project_config_dict, category, process_poss=False)
        for i, city in enumerate(organised_dataa):
            if i == 0:
                city1 = city
            x = np.array(organised_dataa[city]['attributes']).astype(np.float)
            x_normed = (x - self.normalization_factors[city]['x_min'])/(self.normalization_factors[city]['x_max']-self.normalization_factors[city]['x_min'])
            x_normed /= self.stdev_city[city]
            x_normed *= self.weights
            organised_dataa[city]['attributes'] = x_normed

        search_x = []
        for x_vector in organised_dataa[city1]['attributes']:
            search_x.append(x_vector)

        return self.simple_knn_Search_recommender(city1, search_x, project_config_No)


            # organised_dataa[city]['attributes'] = self.get_weighted_x(organised_dataa[city]['attributes'])
        # pprint.pprint(organised_dataa)
        # self.simple_knn_Search_recommender(city, organised_dataa[city1]['attributes'])


if __name__ == '__main__':
    mum = []
    DC = DataCleaner()
    #lis = [43199, 41989, 20297]

    pref_list = ['budget','bhk','possession','amenities','location']

    #search_parameters = [{"Category":None,"Built_Up_Area":900,"Project_No":None,"No_Of_Bathroom":None,"Minimum_Price":9000000,"PricePerUnit":None,"No_Of_Bedroom":2,"Possession":90,"Project_City_Name":"mumbai","amenities":["Swimming Pool","Gym"],"Map_Longitude":"72.827567000000000","Project_config_No":None,"Map_Latitude":"19.194291000000000","No_Of_Balconies":None},{"Category":None,"Built_Up_Area":900,"Project_No":None,"No_Of_Bathroom":None,"Minimum_Price":9000000,"PricePerUnit":None,"No_Of_Bedroom":2,"Possession":90,"Project_City_Name":"mumbai","amenities":["Swimming Pool","Gym"],"Map_Longitude":"72.832754686438760","Project_config_No":None,"Map_Latitude":"19.206685585502232","No_Of_Balconies":None},{"Category":None,"Built_Up_Area":900,"Project_No":None,"No_Of_Bathroom":None,"Minimum_Price":9000000,"PricePerUnit":None,"No_Of_Bedroom":2,"Possession":90,"Project_City_Name":"mumbai","amenities":["Swimming Pool","Gym"],"Map_Longitude":"72.852032000000000","Project_config_No":None,"Map_Latitude":"19.221384000000000","No_Of_Balconies":None}]
    a = time.time()
    s= [{"Category":None,"Built_Up_Area":None,"Project_No":None,"No_Of_Bathroom":None,"Minimum_Price":6000000,"PricePerUnit":None,"No_Of_Bedroom":3,"Possession":30,"Project_City_Name":"pune","amenities":["Swimming Pool","Gym"],"Map_Longitude":"73.9367","Project_config_No":None,"Map_Latitude":"18.5204","No_Of_Balconies":None}]
    print DC.develop_dummy_listing(s, [], pref_list)


    # b = DC.get_recommendations(lis)
    # print b
