import math
import collections

class Cluster:
    def __init__(self, r,g,b):
        self.points = set()
        self.color = "rgb(%d,%d,%d)" % (r, g, b)



    def renewAttribute(self):
        Xs = [_.x for _ in self.points]
        Ys = [_.y for _ in self.points]
        self.x = sum(Xs)/len(Xs)
        self.y = sum(Ys)/len(Ys)
        self.width = max(Xs) - min(Xs)
        self.height = max(Ys) - min(Ys)


    def getSize(self):
        return self.width * self.height

    def addPoint(self, point):
        self.points.add(point)

    def getColor(self):
        return self.color

    def adjustPointsWithSingleBranch(self):
        for p in self.points:
            if (len(p.upBranch) + len(p.downBranch)) == 1:
                if p.upBranch:
                    otherSide = p.upBranch[0]
                else:
                    otherSide = p.downBranch[0]
                if otherSide in self.points and (abs(otherSide.y - p.y)) > 30:
                    p.x = otherSide.findBranchLoc(p)[0]
                    gap = otherSide.y - p.y
                    p.y -= gap/abs(gap) * 60


    def detectCollision(self, points):
        for i in range(1, len(points)):
            if abs(points[i].x - points[i-1].x) < points[i].length/2 + points[i-1].length/2 + 20: #points should be at least 20pt apart
                return True
        return False

    def loosenPoints(self, points):
        for i in range(1, len(points)):
            if abs(points[i].x - points[i-1].x) < points[i].length/2 + points[i-1].length/2 + 20:# Moves in 20pt steps
                points[i].x += 10
                points[i-1].x -= 10

    def adjustCollision(self):
        posDic = collections.defaultdict(list)
        for p in self.points:
            posDic[p.y/10].append(p)
        for k in posDic:
            if len(posDic[k])>1:
                posDic[k].sort(key=lambda p:p.x)
                while self.detectCollision(posDic[k]):
                    self.loosenPoints(posDic[k])


    def lineToOtherCluster(self, tgt):
        if tgt not in self.points:
            return True
        return False


    def findOutReacher(self):
        outerReacher = []
        for p in self.points:
            for connectedP in p.upBranch + p.downBranch:
                if self.lineToOtherCluster(connectedP):  # Move the point that connects to other cluster to the edge of this cluster (for less line intersection)
                    outerReacher.append(p)
                    break
        return outerReacher

    def reacherIntersectwithCluster(self, reacher):
        for p in reacher.upBranch + reacher.downBranch:
            if p not in self.points:
                if self.lineIntersectwithPoint(reacher, p):
                    return True
        else:
            return False


    def moveReacher(self, reacher):
        if reacher.x >= self.x:
            sign = 1
        else:
            sign = -1
        reacher.x += sign*30 #moves at 30 gaps

    def MoveOutreacherLineToSideHelper(self, ToRight, Branches):
        out = []
        within = []
        for b in Branches:
            if self.lineToOtherCluster(b):
                out.append(b)
            else:
                within.append(b)
        if ToRight:
            res = within+out
        else:
            res = out+within
        return res

    def MoveOutreacherLineToSide(self, reacher):
        if reacher.x > self.x: # point on the right side of the cluster
            ToRight = True
        else:
            ToRight = False
        reacher.upBranch = self.MoveOutreacherLineToSideHelper(ToRight, reacher.upBranch)
        reacher.downBranch = self.MoveOutreacherLineToSideHelper(ToRight, reacher.downBranch)

    def ReacherAtEdge(self, reacher):
        self.renewAttribute()
        Xs = [_.x for _ in self.points]
        if reacher.x >= max(Xs) or reacher.x <= min(Xs):
            return True
        return False



    def moveOutreacher(self):
        self.renewAttribute()
        outReacher = self.findOutReacher()
        for reacher in outReacher:
            while self.reacherIntersectwithCluster(reacher):
                self.moveReacher(reacher)
            if self.ReacherAtEdge(reacher):
                self.MoveOutreacherLineToSide(reacher)

    def lineIntersectwithPoint(self, point, tgt):
        x, y1 = point.findBranchLoc(tgt)
        y2 = tgt.y

        otherpoints = [p for p in self.points if p != point]
        for p in otherpoints:
            if (p.y - y1) * (p.y - y2) > 0: #p.y is inside y1 and y2
                if p.x - p.length/2 < x < p.x + p.length/2: #have intersection
                    return True
        return False

    def intersectWithLine(self, origin, tgt, y):
        lines = []

        for p in self.points:
            if (p.x - origin.x) * (p.x - tgt.x) < 0: #p in between origin and target
                for t in p.upBranch + p.downBranch:
                    if t in self.points:
                        lines.append([p.y, t.y])
        for l in lines:
            if (y - l[0]) * (y - l[1]) <= 0:
                return True
        return False



    def adjustPoints(self):
        self.adjustCollision()
        self.adjustPointsWithSingleBranch()
        self.moveOutreacher()