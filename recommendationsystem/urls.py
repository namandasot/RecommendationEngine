'''
Created on 15-Oct-2015

@author: prateek
'''
from django.conf.urls import include, url
from django.contrib import admin
from views import recoIds

urlpatterns = [
    url(r'^test/(?P<property>[0-9]+)', 'recommendationsystem.views.recoIds')
]