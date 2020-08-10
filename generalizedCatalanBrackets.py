from combobject import CombObject
from dyckWord import DyckWord
from mPermutation import mPermutation

class GeneralizedCatalanBrackets(CombObject):

    def __init__(self, object = None, variant = None, rank = None, n = None, m = None):
        super().__init__(object, variant, rank)
        self.n = n
        self.m = m

    @staticmethod
    def GCB_Cardinality(n, m):
        return DyckWord.DW_Cardinality(n) * mPermutation.mP_Cardinality(m, n)

    def Cardinality(self):
        if (self.n and self.m) is not None:
            return self.GCB_Cardinality(self.n, self.m)

    def ToVariant(self):
        if (self.object and self.n and self.m) is not None:
            self.variant = self._ToVariant(self.object, self.n, self.m)
            return self.variant

    def _ToVariant(self, a, n, m):
        v1 = DyckWord(object = a[0], n = n).ToVariant()
        v2 = mPermutation(object = a[1], n = m, m = n).ToVariant()
        return [v1, v2]

    def ToObject(self):
        if (self.variant and self.n and self.m) is not None:
            self.object = self._ToObject(self.variant, self.n, self.m)
            return self.object

    def _ToObject(self, v, n, m):
        a1 = DyckWord(variant = v[0], n = n).ToObject()
        a2 = mPermutation(variant = v[1], n = m, m = n).ToObject()
        return [a1, a2]

    def Rank(self):
        if (self.variant and self.n and self.m) is not None:
            self.rank = self._Rank(self.variant, self.n, self.m)
            return self.rank

    def _Rank(self, v, n, m):
        l1 = DyckWord(variant = v[0], n = n).Rank()
        l2 = mPermutation(variant = v[1], n = m, m = n).Rank()
        return l1 + l2 * DyckWord.DW_Cardinality(n)

    def Unrank(self):
        if (self.rank and self.n and self.m) is not None:
            self.variant = self._Unrank(self.rank, self.n, self.m)
            return self.variant

    def _Unrank(self, r, n, m):
        l1 = r % DyckWord.DW_Cardinality(n)
        l2 = r // DyckWord.DW_Cardinality(n)
        v1 = DyckWord(rank = l1, n = n).Unrank()
        v2 = mPermutation(rank = l2, n = m, m = n).Unrank()
        return [v1, v2]


a = GeneralizedCatalanBrackets(n = 2, m = 2)
for r in range(a.Cardinality()):
    a.rank = r
    a.Unrank()
    a.ToObject()
    a.variant = None
    a.rank = None
    a.ToVariant()
    a.Rank()
    if r != a.rank:
        print("error")
    print(str(r + 1) + ') ' + str(a.__dict__))





