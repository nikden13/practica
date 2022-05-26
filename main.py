from combination import Combination
from treeObject import TreeObject
from tree import Tree
from stirlingSecondKind import StirlingSecondKind
from permutation import Permutation
import time

def getOutputProcessRank(cardinality, procentForOutput):
    return cardinality // 100 * procentForOutput

def test(object):
    error, needOutputProcess, outputProcessRank, procentForOutput = False, None, None, 10
    cardinality = object.Cardinality()
    print('Cardinality:', cardinality)

    for rank in range(cardinality):
        if outputProcessRank is None:
            outputProcessRank = getOutputProcessRank(cardinality, procentForOutput)
        if rank > outputProcessRank:
            needOutputProcess = True

        object.rank = rank
        object.Unrank()
        object.ToObject()
        object.ToVariant()
        newRank = object.Rank()
        if (newRank != rank):
            error = True
            print('Error =(\nRank =', rank)
            break

        if needOutputProcess:
            process = round(outputProcessRank / cardinality * 100)
            outputProcessRank += getOutputProcessRank(cardinality, procentForOutput)
            needOutputProcess = False
            print('Process:',  process , '%')

    if not error:
        print('Success =)')
            

def main():
    tree = Tree(n = 10, m = 8)
    permutation = Permutation(n = 8)
    combination = Combination(n = 15, m = 13)
    stirling = StirlingSecondKind(n = 10, m = 3)

    start = time.time()
    test(tree)
    print('Time:', time.time() - start, 'seconds.')

if __name__ == '__main__':
    main()