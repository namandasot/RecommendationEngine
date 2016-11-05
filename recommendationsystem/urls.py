'''
Created on 15-Oct-2015

@author: prateek
'''
from django.conf.urls import url
from recommendationsystem import views

urlpatterns = [
    url(r'^$', 'recommendationsystem.views.testRecoIds'),
    url(r'showmore/$', views.NewSearch.as_view()),
    
    url(r'newsearch/$', views.NewReco.as_view()),
    
    #url(r'^test/(?P<property>[0-9]+)', 'recommendationsystem.views.recoIds'),
#     url(r'^test/mapApi', 'recommendationsystem.views.mapApi'),
    url(r'^mailer/$','recommendationsystem.views.mailer')
]