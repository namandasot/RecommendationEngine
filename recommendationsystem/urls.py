'''
Created on 15-Oct-2015

@author: Naman
'''
from django.conf.urls import url
from recommendationsystem import views2

urlpatterns = [
    url(r'^$', 'recommendationsystem.views.testRecoIds'),
    
    url(r'newsearch/$', views2.NewReco.as_view()),
    url(r'similarProperties/$', views2.SimilarProperties.as_view()),

    #url(r'^test/(?P<property>[0-9]+)', 'recommendationsystem.views.recoIds'),
#     url(r'^test/mapApi', 'recommendationsystem.views.mapApi'),
    url(r'^mailer/$','recommendationsystem.views.mailer')
]