class TreeObject:
    def __init__(self, parents, children):
        self.parents = parents
        self.children = children

    def isHead(self, nodeValue):
        self.parents[nodeValue] == None

    def isHeadAsLeaf(self, nodeValue):
        self.isHead(nodeValue) and len(self.get()['children'][nodeValue]) < 2

    def isLeaf(self, nodeValue):
        return bool(self.children[nodeValue]) == False

    def getNodesCount(self):
        return len(self.get()['parents'])

    def get(self):
        return {
            'parents': self.parents,
            'children': self.children,
        }

    def getHead(self):
        for key, value in self.parents.items():
            if value == None:
                return key
        return 0

    def getLeafs(self):
        leafs = []
        for keyChild in self.children.keys():
            if self.isLeaf(keyChild):
                leafs.append(keyChild)

        #добавить корень, если у него только один дочерний узел
        head = self.getHead()
        if self.isHeadAsLeaf(head):
            leafs.append(head)

        return leafs

    def getMinLeaf(self):
        leafs = self.getLeafs()

        if bool(leafs) == False:
            return 0

        return min(leafs)

    def deleteLeaf(self, nodeValue):
        wasChange = False
        if self.isLeaf(nodeValue):
            self.parents.pop(nodeValue)
            self.children.pop(nodeValue)
            wasChange = True
        elif self.isHeadAsLeaf(nodeValue):
            self.parents[self.children[nodeValue][0]] = None
            self.parents.pop(nodeValue)
            self.children.pop(nodeValue)
            wasChange = True

        if wasChange:
             for parent, child in self.children.items():
                if nodeValue in child:
                    nodeIndex = child.index(nodeValue)
                    self.get()['children'][parent].pop(nodeIndex)
                    break
