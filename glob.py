import random
import collections
allPoint = {}
allCluster = {}
allEdges = collections.defaultdict(list)
drawnEdges = set()
pointVolt = {}

colorRGB = { "white":"rgb(255,255,255)", "black":"rgb(0,0,0)", "500Color":"rgb(255,0,0)", "220Color":"rgb(255,0,255)",
            "10Color":"rgb(170,170,0)", "35Color":"rgb(255,255,0)", "110Color":"rgb(240,65,85)","11Color":"rgb(0,89,127)",
            "6Color":"rgb(0,0,0)", "13Color":"rgb(0,0,0)", "18Color":"rgb(60,255,255)", "20Color":"rgb(164,255,170)","4Color":"rgb(240,255,139)"}