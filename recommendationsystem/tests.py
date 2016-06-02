from django.test import TestCase
from models import NewSearchParams
from views import getSearchParamDict
# Create your tests here.


class SearchParamDictTestCase(TestCase):
    def test_animals_can_speak(self):
        newsearch_params = NewSearchParams()
        newsearch_params.userId = '12345678'
        newsearch_params.budjet = 20000000
        newsearch_params.city = 'Delhi'
        newsearch_params.possession = 90
        newsearch_params.bhk = 3
        newsearch_params.amenities = '3,5,2'
        newsearch_params.lat_longs = '16|26,17|27,18|28'
        newsearch_params.preference = 'budjet,location,bhk,possession.amenities'
        newsearch_params.localities = 'andheri,malad,worli'
        newsearch_params.area = 1500
        searchParamDictList = getSearchParamDict(newsearch_params)
        
        self.assertEqual(len(searchParamDictList), 3)
        
        self.assertEqual(searchParamDictList[0]['Category'], None)
        self.assertEqual(searchParamDictList[0]['Built_Up_Area'], 1500)
        self.assertEqual(searchParamDictList[0]['Project_No'], None)
        self.assertEqual(searchParamDictList[0]['No_Of_Bathroom'], None)
        self.assertEqual(searchParamDictList[0]['Minimum_Price'], 20000000)
        self.assertEqual(searchParamDictList[0]['PricePerUnit'], None)
        self.assertEqual(searchParamDictList[0]['No_Of_Bedroom'], 3)
        self.assertEqual(searchParamDictList[0]['Possession'], 90)
        self.assertEqual(searchParamDictList[0]['Project_City_Name'], 'Delhi')
        self.assertEqual(searchParamDictList[0]['amenities'][0], 'Gym')
        self.assertEqual(searchParamDictList[0]['amenities'][1], 'Park')
        self.assertEqual(searchParamDictList[0]['amenities'][2], 'Swimming Pool')
        self.assertEqual(searchParamDictList[0]['Project_config_No'], None)
        self.assertEqual(searchParamDictList[0]['No_Of_Balconies'], None)
        self.assertEqual(searchParamDictList[0]['Map_Longitude'], '26')
        self.assertEqual(searchParamDictList[0]['Map_Latitude'], '16')
        self.assertEqual(searchParamDictList[0]['locality_name'], 'andheri')
        
        self.assertEqual(searchParamDictList[1]['Category'], None)
        self.assertEqual(searchParamDictList[1]['Built_Up_Area'], 1500)
        self.assertEqual(searchParamDictList[1]['Project_No'], None)
        self.assertEqual(searchParamDictList[1]['No_Of_Bathroom'], None)
        self.assertEqual(searchParamDictList[1]['Minimum_Price'], 20000000)
        self.assertEqual(searchParamDictList[1]['PricePerUnit'], None)
        self.assertEqual(searchParamDictList[1]['No_Of_Bedroom'], 3)
        self.assertEqual(searchParamDictList[1]['Possession'], 90)
        self.assertEqual(searchParamDictList[1]['Project_City_Name'], 'Delhi')
        self.assertEqual(searchParamDictList[1]['amenities'][0], 'Gym')
        self.assertEqual(searchParamDictList[1]['amenities'][1], 'Park')
        self.assertEqual(searchParamDictList[1]['amenities'][2], 'Swimming Pool')
        self.assertEqual(searchParamDictList[1]['Project_config_No'], None)
        self.assertEqual(searchParamDictList[1]['No_Of_Balconies'], None)
        self.assertEqual(searchParamDictList[1]['Map_Longitude'], '27')
        self.assertEqual(searchParamDictList[1]['Map_Latitude'], '17')
        self.assertEqual(searchParamDictList[1]['locality_name'], 'malad')
        
        
        self.assertEqual(searchParamDictList[2]['Category'], None)
        self.assertEqual(searchParamDictList[2]['Built_Up_Area'], 1500)
        self.assertEqual(searchParamDictList[2]['Project_No'], None)
        self.assertEqual(searchParamDictList[2]['No_Of_Bathroom'], None)
        self.assertEqual(searchParamDictList[2]['Minimum_Price'], 20000000)
        self.assertEqual(searchParamDictList[2]['PricePerUnit'], None)
        self.assertEqual(searchParamDictList[2]['No_Of_Bedroom'], 3)
        self.assertEqual(searchParamDictList[2]['Possession'], 90)
        self.assertEqual(searchParamDictList[2]['Project_City_Name'], 'Delhi')
        self.assertEqual(searchParamDictList[2]['amenities'][0], 'Gym')
        self.assertEqual(searchParamDictList[2]['amenities'][1], 'Park')
        self.assertEqual(searchParamDictList[2]['amenities'][2], 'Swimming Pool')
        self.assertEqual(searchParamDictList[2]['Project_config_No'], None)
        self.assertEqual(searchParamDictList[2]['No_Of_Balconies'], None)
        self.assertEqual(searchParamDictList[2]['Map_Longitude'], '28')
        self.assertEqual(searchParamDictList[2]['Map_Latitude'], '18')
        self.assertEqual(searchParamDictList[2]['locality_name'], 'worli')
