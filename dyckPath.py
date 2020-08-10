from combobject import CombObject

class DyckPathWithReturnSteps(CombObject):

    def __init__(self, object = None, variant = None, rank = None, n = None, m = None):
        super().__init__(object, variant, rank)
        self.n = n
        self.m = m

    @staticmethod
    def DP_Cardinality(n, m):
        if m == 0:
            return 0
        elif m == n:
            return 1
        else:
            return int((m / n) * CombObject.Binomial(2 * n - m - 1, n - 1))

    def Cardinality(self):
        if (self.n and self.m) is not None:
            return self.DP_Cardinality(self.n, self.m)

    def ToVariant(self):
        if (self.object and self.n and self.m) is not None:
            self.variant = self._ToVariant(self.object, self.n, self.m)
            return self.variant

    def _ToVariant(self, a, n, m):
        v, l, k = [], 0, 0
        for i in range(2 * n):
            if l == 0:
                l += 1
            else:
                if a[i] == -1:
                    l -= 1
                    v.append(0)
                else:
                    k += 1
                    l += 1
                    v.append(1)
                if k == n - m:
                    return v

    def ToObject(self):
        if (self.variant and self.n) is not None:
            self.object = self._ToObject(self.variant, self.n)
            return self.object

    def _ToObject(self, v, n):
        l, k = 0, -1
        a = [0 for i in range(2 * n)]
        for i in range(2 * n):
            if l == 0:
                l += 1
                a[i] = 1
            else:
                k += 1
                if k > len(v) - 1:
                    l -= 1
                    a[i] = -1
                elif v[k] == 0:
                    l -= 1
                    a[i] = -1
                else:
                    l += 1
                    a[i] = 1
        return a

    def Rank(self):
        if (self.variant and self.n and self.m) is not None:
            self.rank = self._Rank(self.variant, self.n, self.m)
            return self.rank

    def _Rank(self, v, n, m):
        if m == n:
            r = 0
        else:
            if v[0] == 0:
                r = self._Rank(v[1:], n - 1, m - 1)
            else:
                r = self._Rank(v[1:], n, m + 1) + self.DP_Cardinality(n - 1, m - 1)
        return r

    def Unrank(self):
        if (self.rank and self.n and self.m) is not None:
            self.variant = self._Unrank(self.rank, self.n, self.m)
            return self.variant

    def _Unrank(self, r, n, m):
        if m == n:
            v = []
        else:
            if r < self.DP_Cardinality(n - 1, m - 1):
                v = [0] + self._Unrank(r, n - 1, m - 1)
            else:
                v = [1] + self._Unrank(r - self.DP_Cardinality(n - 1, m - 1), n, m + 1)
        return v

"""
a = DyckPathWithReturnSteps(n = 5, m = 2)
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
"""
