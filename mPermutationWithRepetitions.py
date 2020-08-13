from CombObject import CombObject

class mPermutationWithRepetitions(CombObject):

    def __init__(self, object = None, variant = None, rank = None, n = None, m = None):
        super().__init__(object, variant, rank)
        self.n = n
        self.m = m

    def Cardinality(self):
        if (self.n and self.m) is not None:
            return self._Cardinality(self.n, self.m)

    @staticmethod
    def _Cardinality(n, m):
        if n == 0:
            if m == 0:
                return 1
            else:
                return 0
        else:
            return n**m

    def ToVariant(self):
        if (self.object and self.n and self.m) is not None:
            self.variant = self._ToVariant(self.object, self.n, self.m)
            return self.variant

    def _ToVariant(self, a, n, m):
        v = a.copy()
        v.reverse()
        return v

    def ToObject(self):
        if (self.variant and self.n and self.m) is not None:
            self.object = self._ToObject(self.variant, self.n, self.m)
            return self.object

    def _ToObject(self, v, n, m):
        a = v.copy()
        a.reverse()
        return a

    def Rank(self):
        if (self.variant and self.n and self.m) is not None:
            self.rank = self._Rank(self.variant, self.n, self.m)
            return self.rank

    def _Rank(self, v, n, m):
        if n == 0 or m == 0:
            r = 0
        else:
            r = v[0] - 1 + n * self._Rank(v[1:], n, m - 1)
        return r

    def Unrank(self):
        if (self.rank and self.n and self.m) is not None:
            self.variant = self._Unrank(self.rank, self.n, self.m)
            return self.variant

    def _Unrank(self, r, n, m):
        if n == 0 or m == 0:
            v = []
        else:
            v = [r % n + 1] + self._Unrank(r // n, n, m - 1)
        return v