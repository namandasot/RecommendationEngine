from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
import MySQLdb
from sklearn.neighbors import NearestNeighbors
import numpy as np
import os
from volume1.sqlreader import DataCleaner
# test comment
class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


def recoIds(request,property):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        DC = DataCleaner()
        testVar = DC.get_recommendations(int(property))
#         print testVar
        return JSONResponse(testVar)
