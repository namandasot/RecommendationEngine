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
import numpy as np
import requests
import urllib2
import urllib
import json

cityDict = {'1':'Mumbai','3':'Bangalore','4':'Hyderabad','6':'Chennai','7':'Delhi','10':'Pune','11':'Nashik','13':'Aurangabad','14':'Meerut','15':'Mysore','16':'Agra','17':'Ahmedabad','20':'Lucknow','21':'Kanpur','23':'Kolkata','26':'Bhubaneswar','30':'Vadodara','31':'Jaipur','32':'Indore','38':'Durgapur','39':'Bhopal','40':'Guwahati','41':'Chandigarh','71':'Jamshedpur','77':'Mangalore','136':'Jodhpur','169':'Siliguri','170':'Kerala','172':'Karnal','175':'Chikkamagaluru'}
possessionDict = {0:1,1:75,2:150,3:320,4:640,5:980,6:1280}
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
    newsearch_params.config_type = request.GET.get('propertytype',None)
#     if not (newsearch_params.lat_longs and newsearch_params.city):
    if newsearch_params.lati:
        if not newsearch_params.localities:
            newsearch_params.localities = newsearch_params.city 
#         return "xyz"
    if similar==0 :
        newsearch_params.save()
    newsearch_params.currPage = request.GET.get('page','normal')

    return newsearch_params

def getSearchParamDict(newsearch_params):
    
    if newsearch_params.amenities:
        amenitiesCodes = newsearch_params.amenities.split(',')
        amenitiesList = Amenity.objects.values_list('amenity_name', flat=True).filter(amenity_code__in=amenitiesCodes)
    else:
        amenitiesList=[]
    search_params = []
    if newsearch_params.lati:
        localities_name = newsearch_params.localities.split(',')
#         lat_longs=newsearch_params.lat_longs.split(',')
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

def getRecom(search_params,prefList,past,input_weights):
    search_paramsCopy = copy.deepcopy(search_params)
    pastCopy = copy.deepcopy(past)
    prefListCopy = copy.deepcopy(prefList)
    if input_weights:
        input_weights = input_weights.split(',')
        input_weights = map(int, input_weights)
        recommendedProperties = DC.develop_dummy_listing(search_paramsCopy, pastCopy, prefListCopy, input_weights)
    else:
        recommendedProperties = DC.develop_dummy_listing(search_paramsCopy, pastCopy, prefListCopy)
    return recommendedProperties

def getRel(newsearch_params,search_params,recommendedProperties,past,currPage="Normal"):
    searchParams = search_params
    preferanceList = newsearch_params.preference.split(',')
    pastPropInfoList = []
    recoPropInfoList = []
    for recoProperties in recommendedProperties:
        recoPropInfoList.extend(recoProperties)
    recoPropAttrList = getProjectAttr(recoPropInfoList)
    for a in past:
        pastPropInfoList.append(a["Project_Config_No"])
    pastConfigData = getProjectAttr(pastPropInfoList)
    relevantProperties = Scoring.getScores(searchParams,pastConfigData,recoPropAttrList,preferanceList,currPage)
    #relevantProperties = sorted(relevantProperties, key=lambda k: k['relevance_score']['total_score'],reverse=True)
    relevantProperties = filterSameProjectNo(relevantProperties)
    return relevantProperties

def filterSameProjectNo(relevantProperties):
    relevantPropertiesFiltered = []
    projectNo = []
#     for rp in relevantProperties:
#         if rp['Project_No'] not in projectNo:
#             projectNo.append(rp['Project_No'])
#             relevantPropertiesFiltered.append(rp)
            
    for rap in relevantProperties:
        for rp in rap:
            if rp not in projectNo:
                projectNo.append(rp) 
                relevantPropertiesFiltered.append(rap)
        
            
    return relevantPropertiesFiltered

def getPastConfig(userId,date):
    return MCFW.getFootprint(userId,date)

def getNewSearchResults(request):
    limit = int(request.GET.get('limit',20))
    newsearch_params = getNewSearchResults1(request)
    search_params = getSearchParamDict(newsearch_params)
    input_weights = request.GET.get('input_weights',None)
    recommendedProperties = getRecom(search_params, newsearch_params.preference.split(','),[],input_weights)
    relevantProperties = getRel(newsearch_params,search_params,recommendedProperties,[])
    return relevantProperties[:limit]

def getNewSearchResultsModified(request):
    limit = request.GET.get('limit','0,10')
    limit = int(limit.split(',')[1])
    propertytype = str(request.GET.get('propertytype','apartment')).lower()
    newsearch_params = getNewSearchResults1(request)
    if newsearch_params == "xyz":
        return {"message": "mandatory inputs not present",  "status": 3}
    search_params = getSearchParamDict(newsearch_params)
    input_weights = request.GET.get('input_weights',None)
    pastConfigs = getPastConfig(newsearch_params.userId,"2016-01-01")
    pastConfigData = getProjectAttr(pastConfigs)
    pastList = []
    try:
        for a in search_params:
            for pastCnfgDta in pastConfigData:
                if getDistanceinKM(a['Map_Latitude'], a['Map_Longitude'], pastCnfgDta['Map_Latitude'], pastCnfgDta['Map_Longitude']) < 8:
                    if pastCnfgDta["Project_Config_No"] not in pastList:
                        pastList.append(pastCnfgDta["Project_Config_No"])
    except:
        pass
    pastConfigs = pastList
    pastConfigData = getProjectAttr(pastConfigs)
    recommendedProperties = getRecom(search_params, newsearch_params.preference.split(','),pastConfigs,input_weights)
    relevantProperties = getRel(newsearch_params,search_params,recommendedProperties,pastConfigData,newsearch_params.currPage)
    relProjConfigId = getConfigId(relevantProperties)
    a = str(datetime.datetime.now())
    MCFW.insertToMongo(relProjConfigId[:limit] , newsearch_params.userId,a)
    relevantProperties =  relevantProperties[:limit]
    returnList = populateReturnList(relevantProperties)
    return returnList
    
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


def getNewSearchResultsFootPrint(request):
    limit = request.GET.get('limit',[0,10])
    limit = int(limit[1])
    userId = request.GET.get('user_cookie_id',None)
    newsearch_params = NewSearchParams.objects.get(userId=userId)
    search_params = getSearchParamDict(newsearch_params)
    pastConfigs = getPastConfig(userId,newsearch_params.modified)
    input_weights = request.GET.get('input_weights',None)
    recommendedProperties = getRecom(search_params, newsearch_params.preference.split(','),pastConfigs,input_weights)
    pastConfigData = getProjectAttr(pastConfigs)
    relevantProperties = getRel(newsearch_params,search_params,recommendedProperties,pastConfigData)
    return relevantProperties

def getNewSearchResultsFootPrintModified(request):
    limit = request.GET.get('limit','0,10')
    limit = int(limit.split(',')[1])
    
    userId = request.GET.get('user_cookie_id',None)
    newsearch_params = NewSearchParams.objects.get(userId=userId)
    search_params = getSearchParamDict(newsearch_params)
    pastConfigs = getPastConfig(userId,"2016-01-01")
    input_weights = request.GET.get('input_weights',None)
    pastConfigData = getProjectAttr(pastConfigs)
    pastList = []
    for a in search_params:
        for pastCnfgDta in pastConfigData:
            if getDistanceinKM(a['Map_Latitude'], a['Map_Longitude'], pastCnfgDta['Map_Latitude'], pastCnfgDta['Map_Longitude']) < 8:
                if pastCnfgDta["Project_Config_No"] not in pastList:
                    pastList.append(pastCnfgDta["Project_Config_No"])
    pastConfigs = pastList
    pastConfigData = getProjectAttr(pastConfigs)
    recommendedProperties = getRecom(search_params, newsearch_params.preference.split(','),pastConfigs,input_weights)
    relevantProperties = getRel(newsearch_params,search_params,recommendedProperties,pastConfigData)
    pastShownData = MCFW.getFromMongo(userId)
    relProjConfigId = getConfigId(relevantProperties)
    returnList = []
    returnListConfig = []
    for prop,propAtr in zip(relProjConfigId,relevantProperties):
        if prop not in pastShownData:
            returnList.append(propAtr)
            returnListConfig.append(prop)
            
        if len(returnListConfig) >= limit:
            break
    totalProp = returnListConfig + pastShownData
    a = str(datetime.datetime.now())
    MCFW.insertToMongo(totalProp , userId,a)
    returnList = populateReturnList(returnList)
    return returnList


def populateReturnList(returnList):
    method = "POST"
    handler = urllib2.HTTPHandler()
    opener = urllib2.build_opener(handler)
    url = "https://hdfcred.com/apimaster/mobile_v3/recoengine_web"
#     data = {"data":[{"5230":{"relevance_score":{"possession":{"text":"\"This home is Ready for Possession\""}},"Project_Config_No":"285"}, "11":{"relevance_score":{"possession":{"text":"\"This home is Ready for Possession\""}},"Project_Config_No":"285"}}]}
    data = {"data": returnList}
    request = urllib2.Request(url, data=json.dumps(data["data"]))
    request.add_header("Content-Type",'application/json')
    request.get_method = lambda: method
    try:
        connection = opener.open(request)
        print "Done"
    except urllib2.HTTPError,e:
        connection = e
    
    # check. Substitute with appropriate HTTP code.
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
#             configArr.append(ele["Project_Config_No"])
    return configArr

def testRecoIds(request):
    userId = request.GET.get('user',None)
    propertyListInt = MCFW.getFootprint(userId)
    recommendedProperties = DC.get_recommendations(propertyListInt)[:10]
    return recoIds(request,recommendedProperties)

    


class NewSearch(APIView):
    def get(self, request):
        #return Response(getNewSearchResultsFootPrint(request))
        return Response(getNewSearchResultsFootPrintModified(request))


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
        #return Response(getNewSearchResults(request))
        limit1 = request.GET.get('limit','0,10')
        limit1 = int(limit1.split(',')[0])
        if limit1 ==0:
            return Response(getNewSearchResultsModified(request))
        else:
            return Response(getNewSearchResultsFootPrintModified(request))
        
        
class SimilarProperties(APIView):
    def get(self, request):    
        #return Response(getNewSearchResults(request))
        return Response(getSimilarProperties(request))

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
    
    
    
    
def getSimilarProperties(request):
    start= time.time()
    currTime = time.time()
    print currTime-start
    limit = request.GET.get('limit','0,10')
    limit = int(limit.split(',')[1])
    propertytype = str(request.GET.get('propertytype','apartment')).lower()
    newsearch_params = getNewSearchResults1(request,1)
    if newsearch_params == "xyz":
        return {"message": "mandatory inputs not present",  "status": 3}
    search_params = getSearchParamDict(newsearch_params)
    input_weights = request.GET.get('input_weights',None)
    currTime = time.time()
    print "Init1Time " ,currTime-start

    pastConfigs = getPastConfig(newsearch_params.userId,"2016-01-01")
    pastConfigsCopy = pastConfigs
    pastConfigData = getProjectAttr(pastConfigs)
    currTime = time.time()
    print "InitTime " ,currTime-start

    pastList = []
    for a in search_params:
        for pastCnfgDta in pastConfigData:
            if getDistanceinKM(a['Map_Latitude'], a['Map_Longitude'], pastCnfgDta['Map_Latitude'], pastCnfgDta['Map_Longitude']) < 8:
                if pastCnfgDta["Project_Config_No"] not in pastList:
                    pastList.append(pastCnfgDta["Project_Config_No"])
    pastConfigs = pastList
    pastConfigData = getProjectAttr(pastConfigs)
    currTime = time.time()
    print "InitTime " ,currTime-start

    recommendedProperties = getRecom(search_params, newsearch_params.preference.split(','),pastConfigs,input_weights)
    currTime = time.time()
    print "RecoTime " ,currTime-start

    relevantProperties = getRel(newsearch_params,search_params,recommendedProperties,pastConfigData)
    relProjConfigId = getConfigId(relevantProperties)
    #a = str(datetime.datetime.now())
    currTime = time.time()
    print "RelTime " ,currTime-start

    for a in relevantProperties:
        for propName in a:
            if a[propName]['Project_Config_No'] in pastConfigs :
                relevantProperties.remove(a)
    currTime = time.time()
    print "RelTime " ,currTime-start
    #MCFW.insertToMongo(relProjConfigId[:limit] , newsearch_params.userId,a)
    relevantProperties =  relevantProperties[:limit]
#     returnList = populateReturnList(relevantProperties)
    currTime = time.time()
    print "EndTime " ,currTime-start
    return relevantProperties

