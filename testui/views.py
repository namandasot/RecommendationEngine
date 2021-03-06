from django.shortcuts import render
from recommendationsystem.models import AllProjectInfo
from recommendationsystem import views
from recommendationsystem.sqlreader import DataCleaner
import requests
from recommendationsystem.views import *
from recommendationsystem.mongoConnect import *

MCFW = MongoConnectionForWebsite()

def showRecoProjectsUser(request):
    userId = request.GET.get('user',None)
    propertyListInt = MCFW.getFootprint(userId)
#     print propertyListInt
    return getRecommendation(request,propertyListInt)


def showRecoProjectsNewSearch(request):
    newsearch_params = getNewSearchResults1(request)
    pastProp = request.GET.get('past',None)
    pastPropList = []
    pastConfigData = []
    propertyListInt = []
    if pastProp:
        pastPropList = pastProp.split(',')
        for project in pastPropList:
            propertyListInt.append(long(project))
    search_params = getSearchParamDict(newsearch_params)
    input_weights = request.GET.get('input_weights',None)
    recommendedProperties = getRecom(search_params, newsearch_params.preference.split(','),propertyListInt,input_weights)
    relevantProperties = getRel(newsearch_params,search_params,recommendedProperties,propertyListInt)
#     print newsearch_params
#     print search_params
    
    return showMap(request,search_params,propertyListInt,recommendedProperties,relevantProperties)
    
def showMap(request,search,past,recoList,relevantList):
    finalResult = {}
    for reco in recoList:
        recommendedPropertiesAllData = list(AllProjectInfo.objects.filter(project_config_no__in=reco))
        recommendedPropertiesAllData.sort(key=lambda t: reco.index(t.pk))
        for i,recommendedPropertieAllData in enumerate(recommendedPropertiesAllData):
#             print recommendedPropertieAllData.project_config_no
            for relevant in relevantList:
                feedback = ""
                score = 0

                if relevant['Project_Config_No']==recommendedPropertieAllData.project_config_no:
#                     print relevant
                    score=relevant['relevance_score']['total_score']
                    feedback = relevant['relevance_score']
                    break
            if finalResult.has_key(recommendedPropertieAllData.project_config_no):
                if finalResult[recommendedPropertieAllData.project_config_no]['rank'] > i+1:
                    finalResult[recommendedPropertieAllData.project_config_no]['rank'] = i+1
            else:
                finalResult[recommendedPropertieAllData.project_config_no] = {'rank':i+1,'project':recommendedPropertieAllData,'score':score,'feedback':feedback}

    finalResultNew = sorted(finalResult.values(), key=lambda k: k['score'],reverse=True)
    allProperties = AllProjectInfo.objects.filter(project_city_name=search[0]['Project_City_Name'])
    pastList = list(AllProjectInfo.objects.filter(project_config_no__in=past))
    pastList.sort(key=lambda t: past.index(t.pk))
    context = {'recoProjects' : finalResultNew, 'allProperties' : allProperties, 'search':search, 'past':pastList}
    return render(request, 'reco.html', context) 
    
    
def getRecommendation(request,propertyListInt):
    recoProjectsIds = DC.get_recommendations(propertyListInt)[:10]
#     print recoProjectsIds
    projects = []
    for project in propertyListInt:
        projects.append(AllProjectInfo.objects.get(project_config_no=project))

#     print projects
    recoProjects = []
    for recoProjectsId in recoProjectsIds :
        recoProjects.append(AllProjectInfo.objects.get(project_config_no=recoProjectsId))
    allProperties = AllProjectInfo.objects.filter(project_city_name=projects[0].project_city_name)

    context = {'projects' : projects, 'recoProjects' : recoProjects, 'allProperties' : allProperties}
    return render(request, 'reco.html', context) 

def showRecoProjects(request):
    propertyListInt = getProjectIds(request, '')
#     print propertyListInt
    return getRecommendation(request,propertyListInt)