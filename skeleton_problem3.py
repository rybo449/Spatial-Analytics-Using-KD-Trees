import sys
import time
import csv
import numpy as np
from scipy.spatial import KDTree
from collections import Counter
from geopandas import *
import matplotlib.pyplot as plt
from math import sqrt


def loadTaxiTripsPickupAndDropoffs(filename):
    #bbox around Manhattan
    latBounds = [40.6,40.9]
    lngBounds = [-74.05,-73.90]
    #
    f = open(filename)
    reader = csv.reader(f)
    header = reader.next()
    #
    lngIndex0 = header.index(' pickup_longitude')
    latIndex0 = header.index(' pickup_latitude')
    latIndex1 = header.index(' dropoff_latitude')
    lngIndex1 = header.index(' dropoff_longitude')
    result = []
    for l in reader:
        try:
            point0 = [float(l[latIndex0]),float(l[lngIndex0])]
            point1 = [float(l[latIndex1]),float(l[lngIndex1])]
            if latBounds[0] <= point0[0] <= latBounds[1] and lngBounds[0] <= point0[1] <= lngBounds[1] and latBounds[0] <= point1[0] <= latBounds[1] and lngBounds[0] <= point1[1] <= lngBounds[1]:
                result.append([point0[0],point0[1],point1[0],point1[1]])
        except:
            print l
    return result
    
def naiveApproach(tripLocations, startRectangle, endRectangle):
    #indices is a list that should contain the indices of the trips in the tripLocations list
    #which start in the startRectangle region and end in the endRectangle region
    indices = []
    startTime = time.time()
    num = 0
    for i in tripLocations:
        if startRectangle[0][0]<=i[0] and startRectangle[0][1]>=i[0] and startRectangle[1][0]<=i[1] and startRectangle[1][1]>=i[1] and endRectangle[0][0]<=i[2] and endRectangle[0][1]>=i[2] and endRectangle[1][0]<=i[3] and endRectangle[1][1]>=i[3]:
            indices.append(num)
        num+=1
    print indices
    #TODO: insert your code here. You should implement the naive approach, i.e., loop 
    #      through all the trips and find the closest intersection by looping through
    #      all of them


    #
    endTime = time.time()
    print 'The naive computation took', (endTime - startTime), 'seconds'
    return indices

def kdtreeApproach(tripLocations, startRectangle, endRectangle):
    #indices is a list that should contain the indices of the trips in the tripLocations list
    #which start in the startRectangle region and end in the endRectangle region
    indices = []


    trip1 = []
    trip2 = []
    for i,j,k,l in tripLocations:
        trip1.append([i,j])
        trip2.append([k,l])
    #print trip1
    startTime = time.time()



    srad = sqrt((startRectangle[0][0] - startRectangle[0][1])**2 + (startRectangle[1][0] - startRectangle[1][1])**2)/float(2)
    erad = sqrt((endRectangle[0][0] - endRectangle[0][1])**2 + (endRectangle[1][0] - endRectangle[1][1])**2)/float(2)
    startx = (startRectangle[0][0] + startRectangle[0][1])/2
    starty = (startRectangle[1][0] + startRectangle[1][1])/2
    endx = (endRectangle[0][0] + endRectangle[0][1])/2
    endy = (endRectangle[1][0] + endRectangle[1][1])/2


    tree1 = KDTree(trip1)
    tree2 = KDTree(trip2)
    start = set(tree1.query_ball_point([startx,starty], srad))
    end = set(tree2.query_ball_point([endx, endy], erad))
    in_both = list(start.intersection(end))
    print len(in_both)
    for i in in_both:
        if startRectangle[0][0]<=tripLocations[i][0] and startRectangle[0][1]>=tripLocations[i][0] and startRectangle[1][0]<=tripLocations[i][1] and startRectangle[1][1]>=tripLocations[i][1] and endRectangle[0][0]<=tripLocations[i][2] and endRectangle[0][1]>=tripLocations[i][2] and endRectangle[1][0]<=tripLocations[i][3] and endRectangle[1][1]>=tripLocations[i][3]:
            indices.append(i)
    print indices        
    #indices.append(start)
    #indices.append(end)
    #print indices

    #TODO: insert your code here. You should build the kdtree and use it to query the closest
    #      intersection for each trip

    #
    endTime = time.time()
    print 'The kdtree computation took', (endTime - startTime), 'seconds'
    return indices

def extraCredit(tripLocations, startPolygon, endPolygon):
    #indices is a list that should contain the indices of the trips in the tripLocations list
    #which start in the startPolygon region and end in the endPolygon region
    indices = []

    #TODO: insert your code here. You should build the kdtree and use it to query the closest
    #      intersection for each trip

    return indices    

if __name__ == '__main__':
    #these functions are provided and they already load the data for you
    trips             = loadTaxiTripsPickupAndDropoffs(sys.argv[1])
    #
    startRectangle    = [[40.713590,40.721319],[-74.011116,-73.994722]] #[[minLat,maxLat],[minLng,maxLng]]
    endRectangle      = [[40.744532,40.748398],[-74.003005,-73.990881]] #[[minLat,maxLat],[minLng,maxLng]]

    #You need to implement this one. You need to make sure that the counts are correct
    naiveIndices = naiveApproach(trips,startRectangle, endRectangle)

    #You need to implement this one. You need to make sure that the counts are correct
    kdtreeIndices = kdtreeApproach(trips,startRectangle, endRectangle)
