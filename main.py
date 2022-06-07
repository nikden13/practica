from re import L
from combination import Combination
from treeObject import TreeObject
from tree import Tree
from stirlingSecondKind import StirlingSecondKind
from permutation import Permutation
import time
import pandas as pd

tree = TreeObject(
    {
        1: 3,
        2: 6,
        3: None,
        4: 1,
        5: 6,
        6: 3,
    },
    {
        1: [4],
        2: [],
        3: [1, 6],
        4: [],
        5: [],
        6: [2, 5],
    }
)

def getOutputProcessRank(cardinality, procentForOutput):
    return cardinality // 100 * procentForOutput

def inLists(object, lists):
    for list in lists:
        if (compareLists(object, list)):
            return True
    return False

def inDicts(dict, objects):
    if (objects == []):
        return False
    for object in objects:
        if (len(dict['parents']) != len(object['parents'])):
            continue
        for index in range(len((object['parents']))):
            try:
                if ((object['parents'][index + 1] != dict['parents'][index + 1])):
                    return False
            except Exception:
                return False
    return True


def compareLists(object, list):
    if (object is not list) or (list is not list):
        return object == list
    if len(object) != len(list):
        return False
    for index in range(len(list)):
        if (type(object[index] is list)) and (type(list[index] is list)):
            return compareLists(object[index], list[index])
        if (object[index] != list[index]):
            return False
    return True

def test(object):
    error, needOutputProcess, outputProcessRank, procentForOutput = False, None, None, 1
    variants, objects, times  = [], [], [];
    cardinality = object.Cardinality()
    print('Cardinality:', cardinality)

    for rank in range(cardinality):
        #if outputProcessRank is None:
        #    outputProcessRank = getOutputProcessRank(cardinality, procentForOutput)
        #if rank > outputProcessRank:
        #    needOutputProcess = True
    
        object.rank = rank
        #object.Unrank()
        #object.ToObject()
        #object.ToVariant()
        for i in range(10):
            tm = 0;
            start = time.perf_counter()
            object.Unrank()
            tm += (time.perf_counter() - start)
        times.append(tm / 1)

        #print(tm, 'seconds.')
    data = pd.DataFrame({'toobject': times})
    data.to_excel('./results1.xlsx')
        #if (inLists(variantFromRank, variants)):
        #    print('Error Unrank rank =', rank)
        #    error = True
        #    break
        #variants.append(variantFromRank)

        #start = time.time()
        #obj = object.ToObject()
        #print('Time:', time.time() - start, 'seconds.')

        #if (inDicts(obj, objects)):
        #    print('Error ToObject rank =', rank)
        #    error = True
        #    break
        #objects.append(obj)

        #variantFrmObject = object.ToVariant()
        #if (not inLists(variantFrmObject, [variants[-1]])):
        #    print('Error ToVariant rank =', rank)
        #    error = True
        #    break

        #newRank = object.Rank()
        #print('Time:', time.time() - start, 'seconds.')

        #if (newRank != rank):
        #    error = True
        #    print('Error =(\nRank =', rank)
        #    break

        #if needOutputProcess:
        #    process = round(outputProcessRank / cardinality * 100)
        #    outputProcessRank += getOutputProcessRank(cardinality, procentForOutput)
        #    needOutputProcess = False
        #    print('Process:',  process , '%')

    if not error:
        print('Success')
            
def testFromRank(object, rank):
    object.rank = rank
    object.rank
    object.Unrank()
    object.ToObject()
    #start = time.time()
    #object.ToVariant()
    #object.Rank()
    #print('Time:', time.time() - start, 'seconds.')

def testToRank(object):
    object.ToVariant()
    object.Rank()

def testFromObject(object):
    object.object = TreeObject(
        {
            1: 3,
            2: 6,
            3: None,
            4: 1,
            5: 6,
            6: 3,
        },
        {
            1: [4],
            2: [],
            3: [1, 6],
            4: [],
            5: [],
            6: [2, 5],
        }
    )

    print('Object:', object.object.get())
    print('Variant from object:', object.ToVariant())
    print('Rank from variant:', object.Rank())

def grafik(object):
    times = []
    rank = object.Cardinality() - 1
    object.rank = rank
    #obect.Unrank()
    #object.ToObject()
    #object.ToVariant()
    for i in range(1):
        tm = 0;
        start = time.perf_counter()
        object.Unrank()
        tm += (time.perf_counter() - start)
    times.append(tm / 1)

    #print(tm, 'seconds.')
    data = pd.DataFrame({'toobject': times})
    data.to_excel('./results1.xlsx')

def main():
    times = []
    for generateNumber in range(2, 21):
        tree = Tree(n = 21, m = generateNumber)
        for i in range(1):
            tm = 0;
            start = time.perf_counter()
            testFromRank(tree, tree.Cardinality() - 1)
            
            #testToRank(tree)
            tm += (time.perf_counter() - start)
        times.append(tm / 1)
        print(generateNumber)

        #print(tm, 'seconds.')
    #tree = Tree(n = 9, m = 8)
    #tree = Tree(n = 7, m = 2)
    #test(tree)
    data = pd.DataFrame({'1': times})
    data.to_excel('./results1.xlsx')
        

    #testFromObject(tree)
    #permutation = Permutation(n = 5)
    #combination = Combination(n = 15, m = 13)
    #stirling = StirlingSecondKind(n = 5, m = 3)
    #tree = Tree(n = 6, m = 5)
    #start = time.time()
    #test(tree)
    #testFromRank(tree)
    #testFromObject(tree)
    #print('Time:', time.time() - start, 'seconds.')

if __name__ == '__main__':
    main()

