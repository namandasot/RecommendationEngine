from django.shortcuts import render
from recommendationsystem.models import AllProjectInfo
from recommendationsystem import views
from volume1.sqlreader import DataCleaner

# Create your views here.
def showRecoProjects(request,project_config_id):
    projectId = int(project_config_id)
    project = AllProjectInfo.objects.get(project_config_no=projectId)
    DC = DataCleaner()
    recoProjectsIds = DC.get_recommendations(projectId)
    recoProjects = []
    for recoProjectsId in recoProjectsIds :
        recoProjects.append(AllProjectInfo.objects.get(project_config_no=recoProjectsId))
    print recoProjects
    context = {'project' : project, 'recoProjects' : recoProjects}
    return render(request, 'reco.html', context)