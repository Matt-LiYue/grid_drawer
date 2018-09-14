import json
import glob
import collections
from Transformer import *

from PreProcessing import *
class Canvas:
    def __init__(self):
        self.canvas = {"v": "6.2.2", "d":[],"p": {"background":"rgb(0, 0, 0)", "layers":["0",1], "autoAdjustIndex":True, "hierarchicalRendering":True}}
        # self.generateName()
    def printToFile(self, fname="/home/liyue/jichengnnegyuanhinhightopozhongruinew/demo/2deditor/Test_new.js"):
        if "Test_new" not in fname:
            toJson = True
        else:
            toJson = False
        with open(fname, "w") as f:
            f.write(self.toString(toJson))

    def drawLine(self, startX, startY, endX, endY, color, width=6):
        l = Line(startX, startY, endX, endY, color, width)
        self.canvas["d"].append(l.getRepresentation())

    def drawBendedLine(self, x1, y1, x2, y2, midy, color="rgb(0,255,0)"):
        if abs(y1 - midy) < 15:
            midy = midy + 30
        self.drawLine(x1, y1, x1, midy, color)
        self.drawLine(x1, midy, x2, midy, color)
        self.drawLine(x2, midy, x2, y2, color)

    def drawLineWith2PortTransformer(self, x1, y1, x2, y2, c1, c2):
        n = Transformer2("", x1, (y2+y1)/2, c1, c2)
        self.canvas["d"].append(n.getRepresentation())
        comp = abs(y2-y1)/2-n.height/2
        if y1 > y2:
            comp = -comp
        self.drawLine(x1, y1, x1, y1+comp, c1)
        self.drawLine(x2, y2, x2, y2-comp, c2)


    def __str__(self):
        return "var datamodel_config = " + json.dumps(self.canvas, indent=2)

    def toString(self, toJson):
        if toJson:
            return json.dumps(self.canvas, indent=2)
        else:
            return "var datamodel_config = " + json.dumps(self.canvas, indent=2)


    def printContent(self):
        return json.dumps(self.canvas["d"], indent=2)


class Line:
    def __init__(self, startX, startY, endX, endY, color, borderWidth):
        self.representation = {}
        self.startX, self.startY = startX, startY
        self.endX, self.endY = endX, endY
        self.representation["c"] = "ht.Shape"
        self.representation["i"] = 1
        self.representation["p"] = {"width": abs(self.endX - self.startX), "height": abs(self.endY - self.startY),
                                    "position": {"x": float(self.startX + self.endX) / 2,
                                                 "y": float(self.startY + self.endY) / 2}, "points": {}}
        self.representation["p"]["points"]["__a"] = [{"x": startX, "y": startY}, {"x": endX, "y": endY}]
        self.representation["s"] = {"shape.border.width": borderWidth, "shape.border.color": color}

    def __str__(self):
        return json.dumps(self.representation, indent=2)

    def addAttributeFromBus(self, cnID):
        attrs =  glob.infoMap[cnID]
        self.representation["a"] = {}
        self.representation["a"]["name"] = attrs['name']
        self.representation["a"]["voltage"] = attrs["volt"]
        self.representation["p"]["tag"] = cnID
        self.representation["a"]["lineColor"] = glob.getVoltRGB(attrs["volt"])

    def __repr__(self):
        return json.dumps(self.representation, indent=2)

    def getRepresentation(self):
        return self.representation




extraLen = 60
class Point:
    def __init__(self, ID, x, y, canv):
        self.ID = ID
        self.x = x
        self.y = y
        self.canv = canv
        if int(self.ID) > 0:
            self.color = glob.colorRGB[str(glob.pointVolt[self.ID])+"Color"]
        else:
            self.color = "rgb(0,255,0)"
        self.cluster = 0
        self.upBranch = []
        self.downBranch = []
        self.length = extraLen


    def reOrderDownBranch(self):
        toLft = []
        toRgt = []
        for b in self.downBranch:
            if b.x < self.x:
                toLft.append(b)
            else:
                toRgt.append(b)
        toLft.sort(key=lambda x:x.findBranchVertLoc(self))
        toRgt.sort(key=lambda x:x.findBranchVertLoc(self), reverse=True)
        self.downBranch=toLft+toRgt


    def initBranches(self):
        for k in glob.allEdges[self.ID]:
            other = glob.allPoint[k]
            if abs(self.y - other.y) < 30:
                self.downBranch.append(other)
            elif self.y > other.y:
                self.upBranch.append(other)
            else:
                self.downBranch.append(other)

        self.upBranch.sort(key=lambda b: b.x)
        self.downBranch.sort(key=lambda b: b.x)
        self.length = (max(len(self.downBranch), len(self.upBranch))-1) * 100 + extraLen

    def drawBranches(self):
        self.drawBranch(self.downBranch, "rgb(0,0,255)")

    #def findBranchLoc(self, otherID):

    def findBranchLoc(self, tgt):
        start = self.x - self.length / 2 + extraLen/2

        if tgt in self.upBranch:
            if len(self.upBranch) == 1:
                start = self.x
                gap = 0
            else:
                gap = (self.length - extraLen) / (len(self.upBranch) - 1)
            idx = self.upBranch.index(tgt)
        elif tgt in self.downBranch:
            if len(self.downBranch) == 1:
                start = self.x
                gap = 0
            else:
                gap = (self.length - extraLen) / (len(self.downBranch) - 1)
            idx = self.downBranch.index(tgt)
        else:
            raise ValueError("errors!")
        return start + gap * idx, self.y

    def findBranchVertLoc(self, tgt):
        if tgt not in self.upBranch:
            res = (self.y + tgt.y)/2
        elif tgt.x < self.x:
            res = self.y - (1+self.upBranch.index(tgt))*60
        else:
            res = self.y - (1+self.upBranch[::-1].index(tgt))*60

        if self.cluster != tgt.cluster:#tgt is in another cluster, avoid the line intersecting with self.cluster
            if (tgt.x - glob.allCluster[self.cluster].x) * (self.x - glob.allCluster[self.cluster].x) < 0: #tgt and self on two sides of self.cluster
                if glob.allCluster[self.cluster].intersectWithLine(self, tgt, res):
                    res += min([_.y for _ in glob.allCluster[self.cluster].points]) - self.y
        return res

    def drawBranch(self, branches, color):
        start = self.x - self.length / 2 + extraLen/2
        if len(branches) <= 1:
            start = self.x
            gap = 0
        else:
            gap = (self.length - extraLen) / (len(branches) - 1)
        for b in branches:
            if (b, self) not in glob.drawnEdges and (self, b) not in glob.drawnEdges:
                tgtX, tgtY = b.findBranchLoc(self)
                midY = b.findBranchVertLoc(self)

                if int(self.ID) > 0 and int(b.ID) > 0:  # No 3-port transformer
                    if b.color != self.color:   # 2-port transformer
                        if start == tgtX:
                            self.canv.drawLineWith2PortTransformer(start,self.y,tgtX,tgtY,self.color,b.color)
                        else:
                            self.canv.drawBendedLine(start, self.y + 7.5, tgtX, tgtY - 7.5, midY, self.color)
                    else:   # AC line
                        self.canv.drawBendedLine(start, self.y + 7.5, tgtX, tgtY - 7.5, midY, self.color)
                else:
                    self.canv.drawBendedLine(start, self.y+7.5, tgtX, tgtY-7.5, midY, b.color)
                glob.drawnEdges.add((b, self))
            start += gap

    def draw(self):
        #if int(self.ID) > 0:
        self.canv.drawLine(self.x - self.length/2, self.y, self.x + self.length/2, self.y, self.color, 15)
        # else:
        #     n = Transformer3("", self.x, self.y, "rgb(255,0,0)", "rgb(255,255,0)", "rgb(255,255,255)")
        #     self.canv.canvas["d"].append(n.getRepresentation())
        #self.drawBranches()

class Drawer:
    def __init__(self):
        self.canv = Canvas()
        self.loadData()
        proc = Preprocessing()
        for n in glob.allPoint.values():
            n.initBranches()
        for n in glob.allPoint.values():
            n.reOrderDownBranch()

        proc.AdjustInsideCluster()
        for n in glob.allPoint.values():
            n.draw()
            n.drawBranches()

        #
        # for k in glob.allEdges:
        #     fromX, fromY = glob.allPoint[k].x, glob.allPoint[k].y
        #     for to in glob.allEdges[k]:
        #         toX, toY = glob.allPoint[to].x, glob.allPoint[to].y
        #         self.canv.drawBendedLine(fromX, fromY, toX, toY, (fromY+toY)/2)

        self.canv.printToFile()


    def loadData(self):
        with open('/home/liyue/peidiantu/volt.csv') as f:
            for l in f.readlines()[1:]:
                tmp = l.split(",")
                glob.pointVolt[tmp[0]] = int(tmp[2])


        with open('/home/liyue/peidiantu/input_data_point.json') as f:
            data = json.load(f)

        nodes = data['results'][1:-1]
        edges = data['results'][-1]['@@setedge']

        for n in nodes:
            id, x, y = n["v_id"], float(n["v"]["@longitude"]), float(n["v"]["@latitude"])
            glob.allPoint[id] = Point(id, x, y, self.canv)

        for e in edges:
            glob.allEdges[e["from_id"]].append(e["to_id"])
            glob.allEdges[e["to_id"]].append(e["from_id"])


p = Drawer()