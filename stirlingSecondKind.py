from operator import truediv
from tkinter import N
from turtle import pen
from CombObject import CombObject
import copy

class StirlingSecondKind(CombObject):
    def __init__(self, object = None, variant = None, rank = None, n = None, m = None):
        super().__init__(object, variant, rank)
        self.n = n
        self.m = m
        
    def Cardinality(self):
        if (self.n and self.m) is not None:
            return self._Cardinality(self.n, self.m)

    @staticmethod
    def _Cardinality(n, m):
        if m == 1 or m == n:
            return 1
        if m == 0:
            return 0
        return StirlingSecondKind._Cardinality(n - 1, m - 1) + m * StirlingSecondKind._Cardinality(n - 1, m)

    def ToVariant(self):
        if (self.object and self.n and self.m) is not None:
            self.variant = self._ToVariant([])
            return self.variant

    def _ToVariant(self, variant, sortedObject = []):
        if (len(sortedObject) == 0):
            sortedObject = self.sortObject(copy.deepcopy(self.object))
        if (self.needNextCheckObject(sortedObject)):
            itemWithMaxValue, maxValue = self.getItemWithMaxValue(sortedObject)
            if (len(itemWithMaxValue) == 1):
                sortedObject.remove(itemWithMaxValue)
                self.updateVariant(variant)
                self._ToVariant(variant[1], sortedObject)
            else:
                itemWithMaxValue.remove(maxValue)
                value = sortedObject.index(itemWithMaxValue) + 1
                self.updateVariant(variant, value)
                self._ToVariant(variant[2], sortedObject)
        return variant

    def updateVariant(self, variant, value = None):
        if value:
            variant.append(0)
            variant.append(value)
        else:
            variant.append(1) 
        variant.append([])


    def getItemWithMaxValue(self, object):
        maxValue = 0
        for item in object:
            maxValueInItem = max(item)
            if maxValueInItem > maxValue:
                resultItem = item
                maxValue = maxValueInItem
        return [resultItem, maxValue]

    def needNextCheckObject(self, object):
        if len(object) == 1:
            return False
        for item in object:
            if len(item) > 1:
                return True
        return False

    def sortObject(self, object):
        sortedVariant = []
        minValuesDictionary = {};
        for item in object:
            item.sort()
            if len(item) > 0:
                minValuesDictionary[object.index(item)] = item[0]
        minValuesDictionarySorted = dict(sorted(minValuesDictionary.items(), key=lambda x:x[1]))
        for index in minValuesDictionarySorted:
            sortedVariant.append(object[index])
        return sortedVariant

    def ToObject(self):
        if (self.variant and self.n and self.m) is not None:
            self.object = self._ToObject(self.variant, closeLists = [])
            return self.object

    def _ToObject(self, variant = [], object = [], arrayN = None, arrayM = None, closeLists = []):
        if variant == []:
            result = []
            if self.m == self.n:
                for value in range(self.m):
                    result.append([value + 1])
                return result
            if self.m == 1:
                result = [[number + 1 for number in range(self.n)]]
                return result
            return result
        if object == []:
            object = [[] for number in range(self.m)]
        if arrayN is None:
            arrayN = [number + 1 for number in range(self.n)]
        if arrayM is None:
            arrayM = [number + 1 for number in range(self.m)]
        if (variant[0] == 0):
            index = variant[1] - 1
            indexWithList = 2
        else:
            index = self.getIndexByLastOpenList(object, closeLists)
            closeLists.insert(0, index)
            indexWithList = 1
            arrayM.pop()
        object[index].insert(0, arrayN.pop())

        if len(variant[indexWithList]) > 0:
            self._ToObject(variant[indexWithList], object, arrayN, arrayM, closeLists)
            return object

        self.addRemainingNodes(object, arrayN, arrayM)
        return object

    def addRemainingNodes(self, object, arrayN, arrayM):
        if len(arrayN) == len(arrayM):
            for key, value in enumerate(arrayN):
                object[key].insert(0, value)
            #index = arrayM[-1] - 1
            #object[index].append(arrayN[-1])

            #for item in object:
                #if item == []:
                    #item.append(arrayN[0])
                    #arrayN.pop(0)
        else:    
            for number in arrayN:
                object[0].insert(0, number)

    def getIndexByLastOpenList(self, list, closeLists):
        for index in range(len(list)-1, -1, -1):
            if index not in closeLists:
                return index
        return 0

    def Rank(self):
        if (self.variant and self.n and self.m) is not None:
            self.rank = self._Rank(self.variant, self.n, self.m)
            return self.rank

    def _Rank(self, variant, n, m):
        if m == 1 or m == n:
            return 0
        if variant[0] == 0:
            return variant[1] - 1 + m * self._Rank(variant[2], n - 1, m)
        return self._Rank(variant[1], n - 1, m - 1) + m * self._Cardinality(n - 1, m)

    def Unrank(self):
        if (self.rank and self.n and self.m) is not None:
            self.variant = self._Unrank(self.rank, self.n, self.m)
            return self.variant

    def _Unrank(self, rank, n, m):
        if m == 1 or m == n:
            return []
        if rank < m * self._Cardinality(n - 1, m):
            nodeNumber = rank % m + 1
            return [0, nodeNumber, self._Unrank(rank // m, n - 1, m)]
        return [1, self._Unrank(rank - m * self._Cardinality(n - 1, m), n - 1, m - 1)]
