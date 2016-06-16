from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from recommendationsystem.NewRecommender import DataCleaner
from models import *
from serializers import AllProjectInfoSerializer,AllProjectInfoMailerSerializer
from mongoConnectRecoNew import MongoConnectionForWebsite
import time
from rest_framework.views import APIView
from rest_framework.response import Response
import datetime
from datetime import datetime as dtime
from recommendationsystem.scoringSystem import scroingSystemForWebsite
import copy

Scoring = scroingSystemForWebsite()
DC = DataCleaner()  # to be moved to class based views
MCFW = MongoConnectionForWebsite()  # to be moved to class based views

def getPossessionDays(possessionDate):
    try:
        d1 = dtime.strptime(possessionDate, "%Y-%m-%d")
    except:
        return 0
    d2 = dtime.strptime(str(datetime.date.today()), "%Y-%m-%d")
    days = (d1 - d2).days
    if days<0:
        return 0
    else:
        return days


def getNewSearchResults1(request):
    newsearch_params = NewSearchParams()
    newsearch_params.userId = request.GET.get('user_cookie_id',None)
    newsearch_params.budget = intC(request.GET.get('budget',None))
    newsearch_params.city = request.GET.get('city',None)
    newsearch_params.possession = intC(request.GET.get('possession',None))
    newsearch_params.bhk = intC(request.GET.get('bhk',None))
    newsearch_params.amenities = request.GET.get('amenities',None)
    newsearch_params.lat_longs = request.GET.get('lat_longs',None)
    newsearch_params.preference = request.GET.get('preference',None)
    newsearch_params.localities = request.GET.get('locality',None)
    newsearch_params.area = intC(request.GET.get('area',None))
    newsearch_params.save()
    return newsearch_params

def getSearchParamDict(newsearch_params):
    
    if newsearch_params.amenities:
        amenitiesCodes = newsearch_params.amenities.split(',')
        amenitiesList = Amenity.objects.values_list('amenity_name', flat=True).filter(amenity_code__in=amenitiesCodes)
    else:
        amenitiesList=None
    search_params = []
    if newsearch_params.lat_longs:
        localities_name = newsearch_params.localities.split(',')
        lat_longs=newsearch_params.lat_longs.split(',')
        for idx,lat_long in enumerate(lat_longs):
            search_param = {}
            search_param['Project_No']=None
            search_param['Project_config_No']=None
            search_param['Project_City_Name']=newsearch_params.city
            search_param['Built_Up_Area'] = newsearch_params.area
            search_param['No_Of_Balconies']=None
            search_param['No_Of_Bedroom']=newsearch_params.bhk
            search_param['No_Of_Bathroom']=None
            search_param['Minimum_Price']=newsearch_params.budget
            search_param['Category']=None
            search_param['Possession']=newsearch_params.possession
            search_param['PricePerUnit']=None
            search_param['amenities']=amenitiesList
            search_param['Map_Latitude']=lat_long.split('|')[0]
            search_param['Map_Longitude']=lat_long.split('|')[1]
            search_param['locality_name']=localities_name[idx]
            search_params.append(search_param)
    else:
        search_param = {}
        search_param['Project_No']=None
        search_param['Project_config_No']=None
        search_param['Project_City_Name']=newsearch_params.city
        search_param['Built_Up_Area'] = newsearch_params.area
        search_param['No_Of_Balconies']=None
        search_param['No_Of_Bedroom']=newsearch_params.bhk
        search_param['No_Of_Bathroom']=None
        search_param['Minimum_Price']=newsearch_params.budget
        search_param['Category']=None
        search_param['Possession']=newsearch_params.possession
        search_param['PricePerUnit']=None
        search_param['amenities']=amenitiesList
        search_param['Map_Latitude']=None
        search_param['Map_Longitude']=None
        search_params.append(search_param)
    return search_params

def getRecom(search_params,prefList,past):
    search_paramsCopy = copy.deepcopy(search_params)
    recommendedProperties = DC.develop_dummy_listing(search_paramsCopy, past,prefList)
    return recommendedProperties

def getRel(newsearch_params,search_params,recommendedProperties,past):
    searchParams = search_params
    preferanceList = newsearch_params.preference.split(',')
    recoPropInfoList = []
    for recoProperties in recommendedProperties:
        recoPropInfoList.extend(recoProperties)
    recoPropAttrList = getProjectAttr(recoPropInfoList)
    pastConfigData = getProjectAttr(past)
    relevantProperties = Scoring.getScores(searchParams,pastConfigData,recoPropAttrList,preferanceList)
    return relevantProperties

def getPastConfig(userId,date):
    return MCFW.getNewFootprint(userId,date)

def getNewSearchResults(request):
    limit = request.GET.get('limit',20)
    newsearch_params = getNewSearchResults1(request)
    search_params = getSearchParamDict(newsearch_params)
    recommendedProperties = getRecom(search_params, newsearch_params.preference.split(','),[])
    relevantProperties = getRel(newsearch_params,search_params,recommendedProperties,[])
    return relevantProperties

def getNewSearchResultsFootPrint(request):
    limit = request.GET.get('limit',20)
    userId = request.GET.get('user_cookie_id',None)
    newsearch_params = NewSearchParams.objects.get(userId=userId)
    search_params = getSearchParamDict(newsearch_params)
    pastConfigs = getPastConfig(userId,newsearch_params.modified)
    recommendedProperties = getRecom(search_params, newsearch_params.preference.split(','),pastConfigs)
    pastConfigData = getProjectAttr(pastConfigs)
    relevantProperties = getRel(newsearch_params,search_params,recommendedProperties,pastConfigData)
    return relevantProperties

class NewSearch(APIView):
    def get(self, request):
        return Response(getNewSearchResultsFootPrint(request))


def getProjectAttr(recoPropInfoList):
    recommendedPropertiesAllData = list(AllProjectInfo.objects.filter(project_config_no__in=recoPropInfoList).exclude(config_type='LAND'))
    recommendedPropertiesAllData.sort(key=lambda t: recoPropInfoList.index(t.pk))
    
    recommendedProperties = []
    for recoProperty in recommendedPropertiesAllData:
        propDict = AllProjectInfoSerializer(recoProperty).data
        propDict['No_Of_Bedroom'] = float(str(propDict['No_Of_Bedroom']))
#         print propDict['No_Of_Bedroom']
        propDict['Possession'] = getPossessionDays(propDict['Possession'])
        propDict['locality_name'] = propDict['Project_Area_Name'] +', '+ propDict['Project_Suburb_Name'] +', ' +propDict['Project_City_Name']
        if propDict['amenities']:
            propDict['amenities']=propDict['amenities'][1:-1].split(',')
        else:
            propDict['amenities']=None
        recommendedProperties.append(propDict)
    return recommendedProperties

class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


def intC(temp):
    no = int(temp) if temp else None
    return no


class NewReco(APIView):
    def get(self, request):    
        return Response(getNewSearchResults(request))

def testRecoIds(request):
    ia = time.time()
    userId = request.GET.get('user',None)
    print userId
    
#     propertyListInt = getProjectIds(request, userId)    #change it to mongodb function
    propertyListInt = MCFW.getFootprint(userId)
    print '///////////////////////////////'
    print 'Mongo Loading time', time.time() - ia
    
    b = time.time() 
    recommendedProperties = DC.get_recommendations(propertyListInt)[:10]
    print 'Recommendation time', time.time() - b
    return recoIds(request,recommendedProperties)

'''No use now'''
def getProjectIds(request, userId):
    
    properties=request.GET.get('properties',None)
    print properties
    propertyListInt = []
    propertiesList = properties.split(",")
    for project in propertiesList:
        propertyListInt.append(long(project))
    
    return propertyListInt
    
def recoIds(request,properties):
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
    
