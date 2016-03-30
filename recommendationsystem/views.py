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
from serializers import AllProjectInfoSerializer,AllProjectInfoMailerSerializer
from mongoConnect import MongoConnectionForWebsite
import time
# test comment
class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


DC = DataCleaner()  # to be moved to class based views
MCFW = MongoConnectionForWebsite()  # to be moved to class based views


def testRecoIds(request):
    ia = time.time()
    userId = request.GET.get('user',None)
    print userId
    
   # propertyListInt = getProjectIds(request, userId)    #change it to mongodb function
    propertyListInt = MCFW.getFootprint(userId)
    print '///////////////////////////////'
    print 'Mongo Loading time', time.time() - ia
    
    b = time.time() 
    recommendedProperties = DC.get_recommendations(propertyListInt)[:10]
    print 'Recommendation time', time.time() - b
    return recoIds(request,recommendedProperties)


def getProjectIds(request, userId):
    
    properties=request.GET.get('properties',None)
    print properties
    propertyListInt = []
    propertiesList = properties.split(",")
    for project in propertiesList:
        propertyListInt.append(long(project))
    
    return propertyListInt
    
def recoIds(request,properties):
    """
    List all code snippets, or create a new snippet.
    """
    
    recommendedPropertiesAllData = list(AllProjectInfo.objects.filter(project_config_no__in=properties))
    recommendedPropertiesAllData.sort(key=lambda t: properties.index(t.pk))
    
    recommendedProperties = []
    for recoProperty in recommendedPropertiesAllData:
        recommendedProperties.append(AllProjectInfoSerializer(recoProperty).data)
    return JSONResponse(recommendedProperties)

def mailer(request):
    userId = request.GET.get('user',None)
    print userId
    
    propertyListInt = MCFW.getFootprint(userId)
    recommendedProperties = DC.get_recommendations(propertyListInt)[:4]
    return recoMailData(request,recommendedProperties)
    
def recoMailData(request,properties):    
    recommendedPropertiesAllData = list(AllProjectInfo.objects.filter(project_config_no__in=properties))
    recommendedPropertiesAllData.sort(key=lambda t: properties.index(t.pk))
    
    recommendedProperties = []
    for recoProperty in recommendedPropertiesAllData:
        recommendedProperties.append(AllProjectInfoMailerSerializer(recoProperty).data)
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
