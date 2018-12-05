from __future__ import print_function
from numpy import array
from math import sqrt
from pyspark import SparkConf, SparkContext
import sys, pdb
from datetime import datetime
from pyspark.mllib.clustering import KMeans, KMeansModel

conf = (SparkConf().setAppName("kmeans"))
sc = SparkContext(conf = conf)
data = sc.textFile(sys.argv[1])
header = data.first()
data = data.filter(lambda line: line != header)
parsedData = data.map(lambda line: array([float(x) for i,x in enumerate(line.split(',')) if i!=0 ]))
clusters = KMeans.train(parsedData, 20, maxIterations=10, initializationMode="random")
# Evaluate clustering by computing Within Set Sum of Squared Errors
def error(point):
    center = clusters.centers[clusters.predict(point)]
    return sqrt(sum([x**2 for x in (point - center)]))

WSSSE = parsedData.map(lambda point: error(point)).reduce(lambda x, y: x + y)
print("Within Set Sum of Squared Error = " + str(WSSSE))

sc.stop()