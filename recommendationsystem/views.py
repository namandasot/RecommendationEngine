from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
import MySQLdb
from sklearn.neighbors import NearestNeighbors
import numpy as np
import os
from sqlreader import DataCleaner
from models import AllProjectInfo
import requests
import json
from serializers import AllProjectInfoSerializer
# test comment
class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

DC = DataCleaner()

def testRecoIds(request,properties):
    
    propertyListInt = []
    propertiesList = properties.split(",")
    for project in propertiesList:
        propertyListInt.append(long(project))
    return recoIds(request,propertyListInt)

def recoIds(request,properties):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        
        testVar = DC.get_recommendations(properties)
#         print testVar
        recommendedPropertiesAllData = AllProjectInfo.objects.filter(project_config_no__in=testVar)
        
        recommendedProperties = []
        for recoProperty in recommendedPropertiesAllData:
            recommendedProperties.append(AllProjectInfoSerializer(recoProperty).data)
        print recommendedProperties
        return JSONResponse(recommendedProperties)



#for getting road distance
def mapApi(request):

    allProperties = AllProjectInfo.objects.filter(project_city_name='Mumbai')
    response = []
    for orgProperty in allProperties:
        origin = ''+str(orgProperty.map_latitude)+','+str(orgProperty.map_longitude)
        print origin
        
        destination = ""
        for i in range(3):
            for k in range(20):
                desPproperty = allProperties[(i+1)*k]
                destination = destination+'|'+str(desPproperty.map_latitude)+','+str(desPproperty.map_longitude)
            
            print destination[1:]
            
            mapsApi = 'https://maps.googleapis.com/maps/api/distancematrix/json?key=AIzaSyBImp6Wc_X4yRW2duvUoDw2GcNZ5IkhpEk&origins='
            mapsApi = mapsApi+origin+'&destinations='+destination[1:]
            print mapsApi
            resp = requests.get(mapsApi)
            response.append(resp.text)
            print json.loads(resp.text)
        break

    return JSONResponse(response)