import sys
import time
import csv
from decimal import Decimal
import numpy as np
from scipy.spatial import KDTree
from collections import Counter
from geopandas import *
import matplotlib.pyplot as plt

import shapefile, sys
from matplotlib.path import Path
from matplotlib.patches import PathPatch
from matplotlib.ticker import MaxNLocator
import pyproj

#Decimal(str(16.2)).quantize(Decimal('.01'), rounding=ROUND_UP)
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
    
def naiveApproach(intersections, tripLocations):
    #counts is a dictionary that has as keys the intersection index in the intersections list
    #and as values the number of trips in the tripLocation list which has the key as the closest
    #intersection.
    counts = {}
    min_dist = 1000000000
    startTime = time.time()
    for i in tripLocations:
        for j in intersections:
            check = dist(i[0],i[1],j[0],j[1])
            if min_dist > check:
                min_dist = check
                x,y = j[0], j[1]
        count = counts.setdefault((x,y), 0)
        counts[(x,y)] = count + 1
        
    #TODO: insert your code here. You should implement the naive approach, i.e., loop 
    #      through all the trips and find the closest intersection by looping through
    #      all of them


    #
    endTime = time.time()
    print 'The naive computation took', (endTime - startTime), 'seconds'
    return counts

def kdtreeApproach(intersections, tripLocations):
    #counts is a dictionary that has as keys the intersection index in the intersections list
    #and as values the number of trips in the tripLocation list which has the key as the closest
    #intersection.
    counts = {}
    startTime = time.time()
    tree = KDTree(intersections)
    points = tree.query(tripLocations,k = 1)
    indeces = points[1]
    counts = Counter(indeces)
    #key = indeces.keys()
    #value = key[indeces.values().index(max(indeces.values()))]
    #print value
    #print intersections[value]
    #print counts.keys()
    #busy = indeces.keys().index(value.index(max(value)))
    #print busy
    #TODO: insert your code here. You should build the kdtree and use it to query the closest
    #      intersection for each trip


    #
    endTime = time.time()
    print 'The kdtree computation took', (endTime - startTime), 'seconds'
    return counts

def plotResults(intersections, counts):
    #TODO: intersect the code to plot here
    proj = pyproj.Proj(init = "esri:26918")
    high = max(counts.values())
    a = set(counts.keys())
    l = set([i for i in xrange(len(intersections))])
    b = list(l - a)
    for i in b:
        counts.setdefault(i, 1)

    for i in counts.keys():
        plt.plot(intersections[i][1], intersections[i][0], 'bo', ms = counts[i]/float(high)*15) #alpha = counts[i]/float(high))
    #for i in b:
    #    plt.plot(intersections[i][0], intersections[i][1], 'bo', ms = counts[i]/float(high)*15)

    '''new_intersections = []
    for i in intersections:
        K = i[0]
        J = i[1]
        
        new_intersections.append(proj(J,K))

    fig = plt.figure(figsize=(4.5, 7.2))

    fig.suptitle('New York City Street Maps', fontsize=20)


    ax = fig.add_subplot(111, aspect='equal')


    sf = shapefile.Reader(sys.argv[3])


    for sr in sf.shapeRecords():


        color = '0.8'


        if sr.record[4]=='New York': color='orange'

        parts = list(sr.shape.parts) + [-1]


        for i in xrange(len(sr.shape.parts)):
            path = Path(sr.shape.points[parts[i]:parts[i+1]])
            patch = PathPatch(path, edgecolor=color, facecolor='none', lw=0.5, aa=True)
            ax.add_patch(patch)


    #ax.set_xlim(sf.bbox[0], sf.bbox[2])
    #ax.set_ylim(sf.bbox[1], sf.bbox[3])


    ax.xaxis.set_major_locator(MaxNLocator(3))
    #ax.plot(new_intersections[counts][0], new_intersections[counts][1], 'bo', ms = 5, color = "cyan")
    #for i in new_intersections:
    ax.plot(new_intersections[counts][0],new_intersections[counts][1],'bo', ms = 2, color = "cyan")
    #ax.scatter(new_intersections[0], new_intersections[1])'''


    plt.show()

if __name__ == '__main__':
    #these functions are provided and they already load the data for you
    roadIntersections = loadRoadNetworkIntersections(sys.argv[1])
    tripPickups       = loadTaxiTrips(sys.argv[2])

    
    #naiveCounts = naiveApproach(roadIntersections,tripPickups)

    

    kdtreeCounts = kdtreeApproach(roadIntersections,tripPickups)

    #
    plotResults(roadIntersections,kdtreeCounts)
