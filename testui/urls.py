'''
Created on 15-Oct-2015

@author: prateek
'''
from django.conf.urls import include, url
from django.contrib import admin
from views import *

urlpatterns = [
    url(r'^userfootprint/$', 'testui.views.showRecoProjectsUser'),
    url(r'^project/$', 'testui.views.showRecoProjects'),
    url(r'^newsearch/$', 'testui.views.showRecoProjectsNewSearch')
]