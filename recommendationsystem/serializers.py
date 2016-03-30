'''
Created on 27-Oct-2015

@author: prateek
'''

from rest_framework import serializers
from models import AllProjectInfo
 
class AllProjectInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AllProjectInfo
        fields = ('project_config_no','project_no','project_name','developer_name','built_up_area','project_location_name','no_of_bedroom','minimum_price','p_config_string')


class AllProjectInfoMailerSerializer(serializers.ModelSerializer):
    class Meta:
        model = AllProjectInfo
        
        #TODO
        fields = ('project_config_no','project_no','project_name','developer_name','built_up_area','project_location_name','no_of_bedroom','minimum_price','p_config_string')
