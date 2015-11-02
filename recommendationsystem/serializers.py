'''
Created on 27-Oct-2015

@author: prateek
'''
from django.contrib.auth.models import User, Group
from rest_framework import serializers
from models import AllProjectInfo

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')
        
class AllProjectInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AllProjectInfo
        fields = ('project_config_no',)
