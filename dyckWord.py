from combobject import CombObject

class DyckWord(CombObject):

    def __init__(self, object = None, variant = None, rank = None, n = None):
        super().__init__(object, variant, rank)
        self.n = n

    @staticmethod
    def DW_Cardinality(n):
        return int(1 / (n + 1) * CombObject.Binomial(2 * n, n))

    def Cardinality(self):
        if self.n is not None:
            return self.DW_Cardinality(self.n)

    def ToVariant(self):
        if (self.object and self.n) is not None:
            self.variant = self._ToVariant(self.object, self.n, 0)
            return self.variant

    def _ToVariant(self, a, n, m):
        v = []
        if n == 0:
            v = []
        elif a[m] == -1:
            v = [0]
        else:
            while a[m] == 1:
                vv = self._ToVariant(a, n, m + 1)
                v += vv
                m += 2 * (vv[0] + 1)
                if m >= 2 * n:
                    break
            if m < 2 * n:
                v.insert(0, len(v))
        return v



    def ToObject(self):
        if (self.variant and self.n) is not None:
            self.object = self._ToObject(self.variant, self.n)
            return self.object

    def _ToObject(self, v, n):
        a = [0] * 2 * n
        m = 0
        for i in range(2 * n):
            if a[i] == 0:
                a[i] = 1
                a[i + 1 + 2 * v[m]] = -1
                m += 1
        return a

    def Rank(self):
        if (self.variant and self.n) is not None:
            self.rank = self._Rank(self.variant, self.n)
            return self.rank

    def _Rank(self, v, n):
        if n == 0:
            r = 0
        else:
            m = v[0]
            w = 0
            for i in range(m):
                w += self.DW_Cardinality(i) * self.DW_Cardinality(n - i - 1)
            l1 = self._Rank(v[1:m + 1], m)
            l2 = self._Rank(v[m + 1: n], n - m - 1)
            r = w + l1 + self.DW_Cardinality(m) * l2
        return r

    def Unrank(self):
        if (self.rank and self.n) is not None:
            self.variant = self._Unrank(self.rank, self.n)
            return self.variant

    def _Unrank(self, r, n):
        if n == 0:
            return []
        else:
            s = 0
            for i in range(n):
                l1 = self.DW_Cardinality(i)
                l2 = self.DW_Cardinality(n - i - 1)
                w = l1 * l2
                if s + w > r:
                    l = r - s
                    left = self._Unrank(l % l1 , i)
                    right = self._Unrank(l // l1, n - i - 1)
                    v = [i] + left + right
                    return v
                else:
                    s += w

"""
a = DyckWord(n = 4)
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


