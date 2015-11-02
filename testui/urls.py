'''
Created on 15-Oct-2015

@author: prateek
'''
from django.conf.urls import include, url
from django.contrib import admin
from views import showRecoProjects

urlpatterns = [
    url(r'^test/(?P<project_config_id>[0-9]+)', 'testui.views.showRecoProjects')
]