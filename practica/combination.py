from CombObject import CombObject

class Combination(CombObject):

    def __init__(self, object = None, variant = None, rank = None, n = None, m = None):
        super().__init__(object, variant, rank)
        self.n = n
        self.m = m

    def Cardinality(self):
        if (self.n and self.m) is not None:
            return self._Cardinality(self.n, self.m)

    @staticmethod
    def _Cardinality(n, m):
        return CombObject.Binomial(n, m)

    def ToVariant(self):
        if (self.object and self.n and self.m) is not None:
            self.variant = self._ToVariant(self.object, self.n)
            return self.variant

    def _ToVariant(self, a, n):
        v = a.copy()
        v.reverse()
        if 0 in v and 1 in v:
            l = n - 1
            while v[l] == v[l - 1]:
               l -= 1
            v = v[:l]
        return v

    def ToObject(self):
        if (self.variant and self.n and self.m) is not None:
            self.object = self._ToObject(self.variant, self.n, self.m)
            return self.object

    def _ToObject(self, v, n, m):
        if m == n:
            a = [1 for i in range(n)]
        elif m == 0:
            a = [0 for i in range(n)]
        else:
            a = v.copy()
            if a[-1] == 0:
                a.extend([1 for i in range(self.n - len(a))])
            else:
                a.extend([0 for i in range(self.n - len(a))])
            a.reverse()
        return a

    def Rank(self):
        if (self.variant and self.n and self.m) is not None:
            self.rank = self._Rank(self.variant, self.n, self.m)
            return self.rank

    def _Rank(self, v, n, m):
        if m == 0 or m == n:
            r = 0
        else:
            if v[0] == 0:
                r = self._Rank(v[1:], n - 1, m)
            else:
                r = self._Rank(v[1:], n - 1, m - 1) + self._Cardinality(n - 1, m)
        return r

    def Unrank(self):
        if (self.rank and self.n and self.m) is not None:
            self.variant = self._Unrank(self.rank, self.n, self.m)
            return self.variant

    def _Unrank(self, r, n, m):
        if m == 0 or m == n:
            v = []
        else:
            if r < self._Cardinality(n - 1, m):
                v = [0] + self._Unrank(r, n - 1, m)
            else:
                v = [1] + self._Unrank(r - self._Cardinality(n - 1, m), n - 1, m - 1)
        return v