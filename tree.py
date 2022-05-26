import copy
from CombObject import CombObject
from combination import Combination
from permutation import Permutation
from stirlingSecondKind import StirlingSecondKind
from treeObject import TreeObject

class Tree(CombObject):

    #TreeObject object
    def __init__(self, object = None, variant = None, rank = None, n = None, m = None):
        super().__init__(object, variant, rank)
        self.n = n
        self.m = m

    def Cardinality(self):
        if (self.n and self.m) is not None:
            return self._Cardinality(self.n, self.m)

    @staticmethod
    def _Cardinality(n, m):
        return Combination._Cardinality(n, m) * Permutation._Cardinality(n - m) * StirlingSecondKind._Cardinality(n - 2, n - m)

    def toCodePrufer(self):
        tree = copy.deepcopy(self.object)
        code = []

        while(tree.getNodesCount() > 2):
            minValue = tree.getMinLeaf()
            if tree.isHead(minValue):
                head = tree.getHead()
                code.append(tree.get()['children'][head][0])
            else:
                code.append(tree.get()['parents'][minValue])

            tree.deleteLeaf(minValue)

        return code

    def fromCodePrufer(self, code):
        indexMinNode = 0
        nodes, nodesInTree = [], []
        parents, children = {}, {}
        for node in range(self.n):
            nodes.append(node + 1)
            parents[node + 1] = None
            children[node + 1] = []

        while len(nodes) > 2:
            node = nodes[indexMinNode]
            if node in code:
                indexMinNode += 1
                continue
            indexMinNode = 0
            nodes.remove(node)
            valueFromCode = code.pop(0)
            parents[node] = valueFromCode
            children[valueFromCode].append(node)
            if node not in nodesInTree:
                nodesInTree.append(node)
            if valueFromCode not in nodesInTree:
                nodesInTree.append(valueFromCode)

        if nodes[0] not in nodesInTree:
            nodeParent = nodes[0]
            nodeChildren = nodes[1]
        else:
            nodeParent = nodes[1]
            nodeChildren = nodes[0]
        parents[nodeParent] = nodeChildren
        children[nodeChildren].append(nodeParent)

        return TreeObject(parents, children)

    def getPermutation(self, code):
        permutation = []
        codeSorted = code.copy()
        codeSorted.sort()

        for value in code:
            permutation.append(codeSorted.index(value) + 1)

        return permutation

    def getCombination(self):
        leafs = self.object.getLeafs()
        combination = [1 if numberNode + 1 in leafs else 0 for numberNode in range(self.n)]
        return combination

    def getStirlingNumber(self, code):
        stirlingNumber = []
        savedValues = []
        for index in range(len(code)):
            if code[index] in savedValues:
                indexStirlingNumber = savedValues.index(code[index])
                stirlingNumber[indexStirlingNumber].append(index + 1)
                continue
            else:
                stirlingNumber.append([index + 1])
            savedValues.append(code[index])
        return stirlingNumber

    def ToVariant(self):
        if (self.object and self.n and self.m) is not None:
            self.variant = self._ToVariant()
            return self.variant

    def _ToVariant(self):
        codePrufer = self.toCodePrufer()
        uniqueFromCodePrufer = []
        for item in codePrufer:
            if item not in uniqueFromCodePrufer:
                uniqueFromCodePrufer.append(item)

        permutation = self.getPermutation(uniqueFromCodePrufer)
        combination = self.getCombination()
        stirlingNumber = self.getStirlingNumber(codePrufer)

        permutationVariant = Permutation(object = permutation, n = self.n - self.m).ToVariant()
        comninationVariant = Combination(object = combination, n = self.n, m = self.m).ToVariant()
        stirlingNumberVariant = StirlingSecondKind(object = stirlingNumber, n = self.n - 2, m = self.n - self.m).ToVariant()

        return [permutationVariant, comninationVariant, stirlingNumberVariant]

    def ToObject(self):
        if (self.variant and self.n and self.m) is not None:
            self.object = self._ToObject()
            return self.object.get()

    def _ToObject(self):
        permutationVariant, combinationVariant, stirlingNumberVariant = self.variant
        permutation = Permutation(variant = permutationVariant, n = self.n - self.m).ToObject()
        combination = Combination(variant = combinationVariant, n = self.n, m = self.m).ToObject()
        stirlingNumber = StirlingSecondKind(variant = stirlingNumberVariant, n = self.n - 2, m = self.n - self.m).ToObject()

        numberObject = [0 for index in range(self.n - 2)]
        for subset in stirlingNumber:
            for item in subset:
                numberObject[item - 1] = stirlingNumber.index(subset) + 1

        sortedNodesWithoutLeafs = [numberNode + 1 for numberNode in range(self.n) if combination[numberNode] == 0]
        uniqueFromCodePrufer = [sortedNodesWithoutLeafs[item - 1] for item in permutation]
        codePrufer = [uniqueFromCodePrufer[item - 1] for item in numberObject]
        
        return self.fromCodePrufer(codePrufer)


    def Rank(self):
        if (self.variant and self.n and self.m) is not None:
            self.rank = self._Rank()
            return self.rank

    def _Rank(self):
        permutationRank = Permutation(variant = self.variant[0], n = self.n - self.m).Rank()
        combinationRank = Combination(variant = self.variant[1], n = self.n, m = self.m).Rank()
        stirlingNumberRank = StirlingSecondKind(variant = self.variant[2], n = self.n - 2, m = self.n - self.m).Rank()

        return combinationRank + Combination._Cardinality(self.n, self.m) * (permutationRank + Permutation._Cardinality(self.n - self.m) * stirlingNumberRank)

    def Unrank(self):
        if (self.rank and self.n and self.m) is not None:
            self.variant = self._Unrank()
            return self.variant

    def _Unrank(self):
        tmp = self.rank // Combination._Cardinality(self.n, self.m)

        permutationRank = tmp % Permutation._Cardinality(self.n - self.m)
        combinationRank = self.rank % Combination._Cardinality(self.n, self.m)
        stirlingNumberRank = tmp // Permutation._Cardinality(self.n - self.m)

        permutationVariant = Permutation(rank = permutationRank, n = self.n - self.m).Unrank()
        combinationVariant = Combination(rank = combinationRank, n = self.n, m = self.m).Unrank()
        stirlingNumberVariant = StirlingSecondKind(rank = stirlingNumberRank, n = self.n - 2, m = self.n - self.m).Unrank()

        return [permutationVariant, combinationVariant, stirlingNumberVariant]
