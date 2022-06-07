from CombObject import CombObject
from DyckPath import DyckPath
from mPermutationWithRepetitions import mPermutationWithRepetitions

class GeneralizedCatalanBrackets(CombObject):

    def __init__(self, object = None, variant = None, rank = None, n = None, m = None):
        super().__init__(object, variant, rank)
        self.n = n
        self.m = m

    def Cardinality(self):
        if (self.n and self.m) is not None:
            return self._Cardinality(self.n, self.m)

    @staticmethod
    def _Cardinality(n, m):
        return DyckPath._Cardinality(n) * mPermutationWithRepetitions._Cardinality(m, n)

    def ToVariant(self):
        if (self.object and self.n and self.m) is not None:
            self.variant = self._ToVariant(self.object, self.n, self.m)
            return self.variant

    def _ToVariant(self, a, n, m):
        v1 = DyckPath(object = a[0], n = n).ToVariant()
        v2 = mPermutationWithRepetitions(object = a[1], n = m, m = n).ToVariant()
        return [v1, v2]

    def ToObject(self):
        if (self.variant and self.n and self.m) is not None:
            self.object = self._ToObject(self.variant, self.n, self.m)
            return self.object

    def _ToObject(self, v, n, m):
        a1 = DyckPath(variant = v[0], n = n).ToObject()
        a2 = mPermutationWithRepetitions(variant = v[1], n = m, m = n).ToObject()
        return [a1, a2]

    def Rank(self):
        if (self.variant and self.n and self.m) is not None:
            self.rank = self._Rank(self.variant, self.n, self.m)
            return self.rank

    def _Rank(self, v, n, m):
        l1 = DyckPath(variant = v[0], n = n).Rank()
        l2 = mPermutationWithRepetitions(variant = v[1], n = m, m = n).Rank()
        return l1 + l2 * DyckPath._Cardinality(n)

    def Unrank(self):
        if (self.rank and self.n and self.m) is not None:
            self.variant = self._Unrank(self.rank, self.n, self.m)
            return self.variant

    def _Unrank(self, r, n, m):
        l1 = r % DyckPath._Cardinality(n)
        l2 = r // DyckPath._Cardinality(n)
        v1 = DyckPath(rank = l1, n = n).Unrank()
        v2 = mPermutationWithRepetitions(rank = l2, n = m, m = n).Unrank()
        return [v1, v2]