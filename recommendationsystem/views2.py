from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from recommendationsystem.NewRecommender import DataCleaner
from models import NewSearchParams,Amenity,AllProjectInfo
from serializers import AllProjectInfoSerializer,AllProjectInfoMailerSerializer
from mongoConnectRecoNew import MongoConnectionForWebsite
import time
from rest_framework.views import APIView
from rest_framework.response import Response
import datetime
from datetime import datetime as dtime
from recommendationsystem.scoringSystem import scroingSystemForWebsite
import copy
import numpy as np
import urllib2
import json
from hdfcredrecoengine.configFile import *
import itertools


Scoring = scroingSystemForWebsite()
DC = DataCleaner()  # to be moved to class based views
MCFW = MongoConnectionForWebsite()  # to be moved to class based views

def getPossessionDays(possessionDate):
    try:
        d1 = dtime.strptime(possessionDate, "%Y-%m-%d")
    except:
        return 0
    d2 = dtime.strptime(str(datetime.date.today()), "%Y-%m-%d")
    return max(0,(d1 - d2).days)


def getNewSearchResults1(request,similar=0):
    newsearch_params = NewSearchParams()
    newsearch_params.userId = request.GET.get('user_cookie_id',None)
    newsearch_params.budget = floatC(request.GET.get('budget',None))
    cityId = request.GET.get('cityid','3')
    newsearch_params.city = cityDict[str(cityId)].lower()
    possession = intC(request.GET.get('possession',0))
    try:
        newsearch_params.possession = possessionDict[possession]
    except:
        newsearch_params.possession = None
    newsearch_params.bhk = floatC(request.GET.get('bhk',None))
    newsearch_params.amenities = request.GET.get('amenityid',None)
    newsearch_params.lati = request.GET.get('lat',None)
    newsearch_params.longi = request.GET.get('long',None)
    newsearch_params.preference = request.GET.get('position',"budget,location,bhk,possession,amenities")
    newsearch_params.preference = newsearch_params.preference.replace("size","bhk")
    newsearch_params.localities = request.GET.get('areas',None)
    newsearch_params.area = intC(request.GET.get('area',None))
    newsearch_params.config_type = str(request.GET.get('propertytype','apartment')).lower()
    if newsearch_params.lati:
        if not newsearch_params.localities:
            newsearch_params.localities = newsearch_params.city 
    if similar==0 :
        newsearch_params.save()
    newsearch_params.currPage = request.GET.get('page','normal')
    return newsearch_params

def getSearchParamDict(newsearch_params):
    amenitiesList=[]
    if newsearch_params.amenities:
        amenitiesCodes = newsearch_params.amenities.split(',')
        amenitiesList = Amenity.objects.values_list('amenity_name', flat=True).filter(amenity_code__in=amenitiesCodes)
        
    search_params = []
    if newsearch_params.lati:
        localities_name = newsearch_params.localities.split(',')
        latidudes = newsearch_params.lati.split(',')
        longitudes = newsearch_params.longi.split(',')
        for idx,latitude in enumerate(latidudes):
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
            search_param['Map_Latitude']=latidudes[idx]
            search_param['Map_Longitude']=longitudes[idx]
            try:
                search_param['locality_name']=localities_name[idx]
            except:
                search_param['locality_name']=localities_name[0]
            search_param['Config_Type'] = newsearch_params.config_type
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
        search_param['Config_Type'] = newsearch_params.config_type
        search_param['locality_name']=None

        search_params.append(search_param)
    return search_params

def getRecom(search_params,prefList,past):
    search_paramsCopy = copy.deepcopy(search_params)
    pastCopy = copy.deepcopy(past)
    prefListCopy = copy.deepcopy(prefList)
    recommendedProperties = DC.develop_dummy_listing(search_paramsCopy, pastCopy, prefListCopy)
    return recommendedProperties

def getRel(newsearch_params,search_params,recommendedProperties,past,currPage="Normal"):
    preferanceList = newsearch_params.preference.split(',')
    pastPropInfoList = [] 
    recoPropInfoList =  [x for x in itertools.chain.from_iterable(itertools.izip_longest(*recommendedProperties)) if x]
    recoPropAttrList = getProjectAttr(recoPropInfoList)
    for a in past:
        pastPropInfoList.append(a["Project_Config_No"])
    pastConfigData = getProjectAttr(pastPropInfoList)
    relevantProperties = Scoring.getScores(search_params,pastConfigData,recoPropAttrList,preferanceList,currPage)
    #relevantProperties = sorted(relevantProperties, key=lambda k: k['relevance_score']['total_score'],reverse=True)
    relevantProperties = filterSameProjectNo(relevantProperties)
    return relevantProperties

def filterSameProjectNo(relevantProperties):
    relevantPropertiesFiltered = []
    projectNo = []
    for rap in relevantProperties:
        proj = rap.keys()[0]
        if proj not in projectNo:
            projectNo.append(proj) 
            relevantPropertiesFiltered.append(rap)
    return relevantPropertiesFiltered

def getPastConfig(userId,date):
    return MCFW.getFootprint(userId,date)

def getLimit(request):
    limit = request.GET.get('limit','0,10')
    limit = int(limit.split(',')[1])
    return limit

def filterPropRadius(search_params,pastConfigData):
    pastConfigData1 = []
    for a in search_params:
            for pastCnfgDta in pastConfigData:
                if getDistanceinKM(a['Map_Latitude'], a['Map_Longitude'], pastCnfgDta['Map_Latitude'], pastCnfgDta['Map_Longitude']) < pastRadius:
                    if pastCnfgDta not in pastConfigData1:
                        pastConfigData1.append(pastCnfgDta)
    return pastConfigData1

def getDistanceinKM(lat1,lon1,lat2,lon2):
        R = 6371  # radius of the earth in km
        lat1 = np.radians(float(lat1))
        lat2 = np.radians(float(lat2))
        lon1 = np.radians(float(lon1))
        lon2 = np.radians(float(lon2))
        x = (lon2 - lon1) * np.cos( 0.5*(lat2+lat1) )
        y = lat2 - lat1
        d = R * np.sqrt( x*x + y*y )
        return d

def getNewSearchResultsModified(request,loadMore=0):
    limit = getLimit(request)
    newsearch_params = getNewSearchResults1(request)
    search_params = getSearchParamDict(newsearch_params)
    pastConfigs = getPastConfig(newsearch_params.userId,"2016-01-01")
    pastConfigData = getProjectAttr(pastConfigs)
    try:
        pastConfigData = filterPropRadius(search_params,pastConfigData)
    except:
        pass
    recommendedProperties = getRecom(search_params, newsearch_params.preference.split(','),pastConfigs)
    relevantProperties = getRel(newsearch_params,search_params,recommendedProperties,pastConfigData,newsearch_params.currPage)
    relProjConfigId = getConfigId(relevantProperties)
    
    if loadMore : 
        returnList = filterLoadMore(newsearch_params,relProjConfigId,relevantProperties,limit)
    else:
        currTime = str(datetime.datetime.now())
        MCFW.insertToMongo(relProjConfigId[:limit] , newsearch_params.userId,currTime)
        returnList =  relevantProperties[:limit]
    returnList = populateReturnList(returnList)
    return returnList

def getSimilarProperties(request):
    limit = getLimit(request)
    newsearch_params = getNewSearchResults1(request,1)
    search_params = getSearchParamDict(newsearch_params)
    pastConfigs = getPastConfig(newsearch_params.userId,"2016-01-01")
    pastConfigData = getProjectAttr(pastConfigs)
    try:
        pastConfigData = filterPropRadius(search_params,pastConfigData)
    except:
        pass
    recommendedProperties = getRecom(search_params, newsearch_params.preference.split(','),pastConfigs)
    relevantProperties = getRel(newsearch_params,search_params,recommendedProperties,pastConfigData)
    for a in relevantProperties:
        for propName in a:
            if a[propName]['Project_Config_No'] in pastConfigs :
                relevantProperties.remove(a)
    relevantProperties =  relevantProperties[:limit]
    return relevantProperties


    
def filterLoadMore(newsearch_params,relProjConfigId,relevantProperties,limit):
    pastShownData = MCFW.getFromMongo(newsearch_params.userId)
    returnList = []
    returnListConfig = []
    for prop,propAtr in zip(relProjConfigId,relevantProperties):
        if prop not in pastShownData:
            returnList.append(propAtr)
            returnListConfig.append(prop)
            
        if len(returnListConfig) >= limit:
            break
    totalProp = returnListConfig + pastShownData
    currTime = str(datetime.datetime.now())
    MCFW.insertToMongo(totalProp , newsearch_params.userId,currTime)

    return returnList

def populateReturnList(returnList):
    method = "POST"
    handler = urllib2.HTTPHandler()
    opener = urllib2.build_opener(handler)
    url = "https://hdfcred.com/apimaster/mobile_v3/recoengine_web"
    data = {"data": returnList}
    request = urllib2.Request(url, data=json.dumps(data["data"]))
    request.add_header("Content-Type",'application/json')
    request.get_method = lambda: method
    try:
        connection = opener.open(request)
        print "Done"
    except urllib2.HTTPError,e:
        connection = e
    if connection.code == 200:
        data = connection.read()
        return json.loads(data)
    else:
        print "except"

def getConfigId(propDictArray):
    configArr = []
    for ele in propDictArray:
        for a in ele:
            configArr.append(ele[a]["Project_Config_No"])
    return configArr


def getProjectAttr(recoPropInfoList):
    recommendedPropertiesAllData = list(AllProjectInfo.objects.filter(project_config_no__in=recoPropInfoList))
    recommendedPropertiesAllData.sort(key=lambda t: recoPropInfoList.index(t.pk))    
    recommendedProperties = []
    for recoProperty in recommendedPropertiesAllData:
        propDict = AllProjectInfoSerializer(recoProperty).data
        try:
            propDict['No_Of_Bedroom'] = float(str(propDict['No_Of_Bedroom']))
        except:
            propDict['No_Of_Bedroom'] = 0
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

def floatC(temp):
    no = float(temp) if temp else None
    return no

class NewReco(APIView):
    def get(self, request):    
        limit1 = request.GET.get('limit','0,10')
        limit1 = int(limit1.split(',')[0])
        return Response(getNewSearchResultsModified(request,limit1))
        
class SimilarProperties(APIView):
    def get(self, request):    
        return Response(getSimilarProperties(request))

def testRecoIds(request):
    userId = request.GET.get('user',None)
    propertyListInt = MCFW.getFootprint(userId)
    recommendedProperties = DC.get_recommendations(propertyListInt)[:10]
    return recoIds(request,recommendedProperties)

def getProjectIds(request, userId):    
    properties=request.GET.get('properties',None)
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
    
    

