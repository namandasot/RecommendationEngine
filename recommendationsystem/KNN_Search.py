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

    def get_optimum_neighbours(self, All_points, input_point):
        d = []
        for a_point in input_point:
            distance_list = ((All_points - a_point)**2).sum(axis=1)  # compute distances
            d.append(distance_list)

        weights = [1, 0.5, 0.3, 0.25, 0.2, 0.15, 0.1, 0, 0, 0, 0]
        distance_sum = d[0]
        for i, vector in enumerate(d[1:]):
            if i <= 7:
                distance_sum = distance_sum + weights[i+1] * vector
        distance_sum_sorted_index = distance_sum.argsort()
        print len(distance_sum_sorted_index)
        return distance_sum_sorted_index

