import numpy

class KNN_Search:
    def __init__(self):
        pass
    def get_nearest_neighbours(self, All_points, input_point):
        d = ((All_points - input_point)**2).sum(axis=1)  # compute distances
        ndx = d.argsort()
        return ndx
        #import pprint
        #pprint.pprint(zip(All_points[ndx[:10]], d[ndx[:10]]))
