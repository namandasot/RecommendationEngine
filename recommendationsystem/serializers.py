'''
Created on 27-Oct-2015

@author: prateek
'''

from rest_framework import serializers
from models import AllProjectInfo
 
class AllProjectInfoSerializer(serializers.ModelSerializer):
    Project_No = serializers.IntegerField(source='project_no')
    Project_Config_No = serializers.IntegerField(source='project_config_no')
    Map_Latitude= serializers.DecimalField(max_digits=20, decimal_places=15,source='map_latitude')
    Map_Longitude= serializers.DecimalField(max_digits=20, decimal_places=15,source='map_longitude')
    price= serializers.IntegerField(source='minimum_price')
    Possession= serializers.CharField(source='possession')
    posessionDate = serializers.CharField(source='possession_text')
#     amenities= serializers.CharField(source='amenities')
    Built_Up_Area = serializers.IntegerField(source='built_up_area')
#    No_Of_Bedroom = serializers.DecimalField(max_digits=5, decimal_places=2,source='no_of_bedroom')
    No_Of_Bedroom = serializers.CharField(source='no_of_bedroom')
    Project_City_Name= serializers.CharField(source='project_city_name')
    Project_Suburb_Name= serializers.CharField(source='project_suburb_name')
    Project_Area_Name= serializers.CharField(source='project_area_name')

#             search_param['Possession']=newsearch_params.possession
#             search_param['amenities']=amenitiesList
#             search_param['locality_name']=localities_name[idx]

    class Meta:
        model = AllProjectInfo
        fields = ('Project_No','Project_Config_No','Map_Latitude','Map_Longitude','price','Possession','posessionDate','amenities','Built_Up_Area','No_Of_Bedroom','Project_City_Name','Project_Suburb_Name','Project_Area_Name')


class AllProjectInfoMailerSerializer(serializers.ModelSerializer):
    class Meta:
        model = AllProjectInfo

        #TODO
        fields = ('project_config_no','project_no','project_name','developer_name','built_up_area','project_location_name','no_of_bedroom','minimum_price','p_config_string','address','project_suburb_name','possession_text','amenities')
        