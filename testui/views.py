from django.shortcuts import render
from recommendationsystem.models import AllProjectInfo
from recommendationsystem import views
from recommendationsystem.sqlreader import DataCleaner
import requests
from recommendationsystem.views import *


MCFW = MongoConnectionForWebsite() 

def showRecoProjects(request):
    userId = request.GET.get('user',None)
    propertyListInt = MCFW.getFootprint(userId)
    print propertyListInt
    #propertyListInt = getProjectIds(request, '')
    recoProjectsIds = DC.get_recommendations(propertyListInt)[:10]
    
    print recoProjectsIds
    
    projects = []
    for project in propertyListInt:
        projects.append(AllProjectInfo.objects.get(project_config_no=project))
    print 'projects'
    print projects
    
    recoProjects = []
    for recoProjectsId in recoProjectsIds :
        recoProjects.append(AllProjectInfo.objects.get(project_config_no=recoProjectsId))
    allProperties = AllProjectInfo.objects.filter(project_city_name=projects[0].project_city_name)

    context = {'projects' : projects, 'recoProjects' : recoProjects, 'allProperties' : allProperties}
    return render(request, 'reco.html', context)


    