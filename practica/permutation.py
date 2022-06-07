from CombObject import CombObject

class Permutation(CombObject):

    def __init__(self, object = None, variant = None, rank = None, n = None):
        super().__init__(object, variant, rank)
        self.n = n

    def Cardinality(self):
        if self.n is not None:
            return self._Cardinality(self.n)

    @staticmethod
    def _Cardinality(n):
        return CombObject.Factorial(n)

    def ToVariant(self):
        if (self.object and self.n) is not None:
            self.variant = self._ToVariant(self.object, self.n)
            return self.variant

    def _ToVariant(self, a, n):
        v = []
        aa = a.copy()
        for i in range(n, 0, -1):
            v.append(aa.index(i) + 1)
            aa.remove(i)
        return v

    def ToObject(self):
        if (self.variant and self.n) is not None:
            self.object = self._ToObject(self.variant, self.n)
            return self.object

    def _ToObject(self, v, n):
        a = []
        for i in range(n):
            a.insert(v[n - i - 1] - 1, i + 1)
        return a

    def Rank(self):
        if (self.variant and self.n) is not None:
            self.rank = self._Rank(self.variant, self.n)
            return self.rank

    def _Rank(self, v, n):
        if n == 0:
            r = 0
        else:
            r = v[0] - 1 + n * self._Rank(v[1:], n - 1)
        return r

    def Unrank(self):
        if (self.rank and self.n) is not None:
            self.variant = self._Unrank(self.rank, self.n)
            return self.variant

    def _Unrank(self, r, n):
        if n == 0:
            v = []
        else:
            v = [r % n + 1] + self._Unrank(r // n, n - 1)
        return v