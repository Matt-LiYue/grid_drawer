class Transformer2:
    def __init__(self, ID, x, y, c1, c2, isFloat=False):
        self.id = ID
        self.x = float(x)
        self.y = float(y)
        self.c1 = c1
        self.c2 = c2
        self.isFloat = isFloat
        self.width, self.height = 72, 90
        self.representation = {}
        self.initRepresentation()

    def initRepresentation(self):
        self.representation["c"] = "ht.Node"
        self.representation["i"] = 1  # not sure the usage
        self.representation["p"] = {"name": "two-port-transformer", "layer": 1,
                                    "position": {"x": self.x, "y": self.y}}
        self.representation["a"] = {}
        self.representation["a"]["lineColor"] = self.c1
        self.representation["a"]["lineColor2"] = self.c2
        self.representation["p"]["image"] = "symbols/electricity/transformer2.json"
        self.representation["s"] = {"label": ""}

    def getRepresentation(self):
        return self.representation

class Transformer3:
    def __init__(self, ID, x, y, c1, c2, c3):
        self.id = ID
        self.x = float(x)
        self.y = float(y)
        self.c1 = c1
        self.c2 = c2
        self.c3 = c3
        self.width, self.height = 72, 90
        self.representation = {}
        self.initRepresentation()

    def initRepresentation(self):
        self.representation["c"] = "ht.Node"
        self.representation["i"] = 1  # not sure the usage
        self.representation["p"] = {"name": "two-port-transformer", "layer": 1,
                                    "position": {"x": self.x, "y": self.y}}
        self.representation["a"] = {}
        self.representation["a"]["lineColor"] = self.c1
        self.representation["a"]["lineColor2"] = self.c2
        self.representation["a"]["lineColor2"] = self.c3
        self.representation["p"]["image"] = "symbols/electricity/transformer3.json"
        self.representation["s"] = {"label": ""}

    def getRepresentation(self):
        return self.representation