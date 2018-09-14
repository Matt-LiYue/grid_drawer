import scipy.cluster.hierarchy as hcluster
import glob
import random
from Cluster import *
class Preprocessing:
    def __init__(self):
        self.ReArrangeNode()
        self.Clustering()


    def ReArrangeNode(self):
        longs = [_.x for _ in glob.allPoint.values()]
        las = [_.y for _ in glob.allPoint.values()]
        baseLongs = min(longs)
        baseLas = min(las)

        for p in glob.allPoint.values():
            p.x, p.y = (p.x - baseLongs) * 15000, (p.y - baseLas) * 15000


    def Clustering(self):
        nodes = glob.allPoint.values()
        points = [[_.x,_.y] for _ in nodes]
        threshold = 450
        clusters = hcluster.fclusterdata(points, threshold, criterion="distance")
        for i in range(len(nodes)):
            clusterID = clusters[i]
            nodes[i].cluster = clusterID
            if clusterID not in glob.allCluster:
                glob.allCluster[clusterID] = Cluster(random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
            c = glob.allCluster[clusterID]
            c.points.add(nodes[i])
            #nodes[i].color = c.color
        for cluster in glob.allCluster.values():
            cluster.renewAttribute()

    def AdjustInsideCluster(self):
        for k in glob.allCluster.values():
            k.adjustPoints()
