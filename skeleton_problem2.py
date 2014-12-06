import sys
import time
import csv
import numpy as np
from scipy.spatial import KDTree
from collections import Counter
from geopandas import *
import matplotlib.pyplot as plt


def dist(p1, p2, p3, p4):
    return ((p1-p3)**2 + (p2-p4)**2)**(0.5)


def loadRoadNetworkIntersections(filename):
    #bbox around Manhattan
    latBounds = [40.6,40.9]
    lngBounds = [-74.05,-73.90]
    #
    listWithIntersectionCoordinates = []
    f = open(filename)
    reader = csv.reader(f, delimiter=' ')
    for l in reader:
        try:
            point = [float(l[0]),float(l[1])]
            if latBounds[0] <= point[0] <= latBounds[1] and lngBounds[0] <= point[1] <= lngBounds[1]:
                listWithIntersectionCoordinates.append(point)
        except:
            print l

    return listWithIntersectionCoordinates

def loadTaxiTrips(filename):
    #load pickup positions
    loadPickup = True
    #bbox around Manhattan
    latBounds = [40.6,40.9]
    lngBounds = [-74.05,-73.90]
    #
    f = open(filename)
    reader = csv.reader(f)
    header = reader.next()
    #
    if loadPickup:        
        lngIndex = header.index(' pickup_longitude')
        latIndex = header.index(' pickup_latitude')
    else:
        latIndex = header.index(' dropoff_latitude')
        lngIndex = header.index(' dropoff_longitude')
    result = []
    for l in reader:
        try:
            point = [float(l[latIndex]),float(l[lngIndex])]
            if latBounds[0] <= point[0] <= latBounds[1] and lngBounds[0] <= point[1] <= lngBounds[1]:
                result.append(point)

        except:
            print l
    return result
    
def naiveApproach(intersections, tripLocations, distanceThreshold):
    #counts is a dictionary that has as keys the intersection index in the intersections list
    #and as values the number of trips in the tripLocation list which are within a distance of
    #distanceThreshold from the intersection
    counts = {}
    startTime = time.time()

    #TODO: insert your code here. You should implement the naive approach, i.e., loop 
    #      through all the trips and find the closest intersection by looping through
    #      all of them
    for i in tripLocations:
        for j in intersections:
            check = dist(i[0],i[1],j[0],j[1])
            if distanceThreshold > check:
                x,y = j[0], j[1]
        	count = counts.setdefault((x,y), 0)
        	counts[(x,y)] = count + 1

    
    endTime = time.time()
    print 'The naive computation took', (endTime - startTime), 'seconds'
    return counts

def kdtreeApproach(intersections, tripLocations, distanceThreshold):
    #counts is a dictionary that has as keys the intersection index in the intersections list
    #and as values the number of trips in the tripLocation list which are within a distance of
    #distanceThreshold from the intersection
    counts = {}
    startTime = time.time()
    tree = KDTree(intersections)
    points = tree.query_ball_point(tripLocations,distanceThreshold)
    #print points
    for i in xrange(len(points)):
    	counts[i] = len(points[i])
    #TODO: insert your code here. You should build the kdtree and use it to query the closest
    #      intersection for each trip


    #
    endTime = time.time()
    print 'The kdtree computation took', (endTime - startTime), 'seconds'
    return counts

def plotResults(intersections, counts):
    #TODO: intersect the code to plot here
    high = max(counts.values())
    for i in counts.keys():
        plt.plot(intersections[i][1], intersections[i][0], 'bo', ms = counts[i]/float(high)*7, alpha = counts[i]/float(high))
    plt.show()

    print 'TODO'

def extraCredit(intersections, counts):
    #TODO: intersect the code to plot here
    print 'TODO'

if __name__ == '__main__':
    #these functions are provided and they already load the data for you
    roadIntersections = loadRoadNetworkIntersections(sys.argv[1])
    tripPickups       = loadTaxiTrips(sys.argv[2])
    distanceThreshold = float(sys.argv[3])

    #You need to implement this one. You need to make sure that the counts are correct
    #naiveCounts = naiveApproach(roadIntersections,tripPickups, distanceThreshold)

    #You need to implement this one. You need to make sure that the counts are correct
    kdtreeCounts = kdtreeApproach(roadIntersections,tripPickups, distanceThreshold)

    #
    plotResults(roadIntersections,kdtreeCounts)
