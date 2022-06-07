from CombObject import CombObject
from Combination import Combination
from Permutation import Permutation

class mPermutation(CombObject):

    def __init__(self, object = None, variant = None, rank = None, n = None, m = None):
        super().__init__(object, variant, rank)
        self.n = n
        self.m = m

    def Cardinality(self):
        if (self.n and self.m) is not None:
            return self._Cardinality(self.n, self.m)
        
    @staticmethod
    def _Cardinality(n, m):
        if m > n:
            return 0
        else:
            return int(CombObject.Factorial(n) / CombObject.Factorial(n - m))

    def ToVariant(self):
        if (self.object and self.n and self.m) is not None:
            self.variant = self._ToVariant(self.object, self.n, self.m)
            return self.variant

    def _ToVariant(self, a, n, m):
        a1, a2, a3 = a.copy(), [], []
        a1.sort()
        for i in range(m):
            s = 0
            for j in range(m):
                if a[i] >= a[j]:
                    s += 1
            a2.append(s)
        a3 = [1 if i + 1 in a1 else 0 for i in range(n)]
        v1 = Combination(object = a3, n = n, m = m).ToVariant()
        v2 = Permutation(object = a2, n = m).ToVariant()
        return [v1, v2]

    def ToObject(self):
        if (self.variant and self.n and self.m) is not None:
            self.object = self._ToObject(self.variant, self.n, self.m)
            return self.object

    def _ToObject(self, v, n, m):
        a1 = Combination(variant = v[0], n = n, m = m).ToObject()
        a2 = Permutation(variant=v[1], n=m).ToObject()
        a3 = []
        for i in range(len(a1)):
            if a1[i] == 1:
                a3.append(i + 1)
        a = [a3[a2[i] - 1] for i in range(m)]
        return a

    def Rank(self):
        if (self.variant and self.n and self.m) is not None:
            self.rank = self._Rank(self.variant, self.n, self.m)
            return self.rank

    def _Rank(self, v, n, m):
        l1 = Combination(variant = v[0], n = n, m = m).Rank()
        l2 = Permutation(variant = v[1], n = m).Rank()
        return l1 + l2 * Combination._Cardinality(n, m)

    def Unrank(self):
        if (self.rank and self.n and self.m) is not None:
            self.variant = self._Unrank(self.rank, self.n, self.m)
            return self.variant

    def _Unrank(self, r, n, m):
        l1 = r % Combination._Cardinality(n, m)
        l2 = r // Combination._Cardinality(n, m)
        v1 = Combination(rank = l1, n = n, m = m).Unrank()
        v2 = Permutation(rank = l2, n = m).Unrank()
        return [v1, v2]