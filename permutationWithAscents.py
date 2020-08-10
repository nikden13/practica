from combobject import CombObject

class PermutationWithAscents(CombObject):

    def __init__(self, object = None, variant = None, rank = None, n = None, m = None):
        super().__init__(object, variant, rank)
        self.n = n
        self.m = m

    @staticmethod
    def _CountAscents(a):
        k = 0
        if len(a) > 1:
            for i in range(len(a) - 1):
                if a[i] < a[i + 1]:
                    k += 1
        return k

    @staticmethod
    def _AddAscent(n, k, v):
        countD, i = 0, 0
        if len(v) == 0:
            v.insert(i, n)
            return v
        while countD != k + 1:
            i += 1
            if i == len(v):
                countD = k + 1
            elif v[i - 1] > v[i]:
                countD += 1
        v.insert(i, n)
        return v

    @staticmethod
    def _AddDescent(n, k, v):
        countA, i = 0, 0
        while countA != k:
            i += 1
            if v[i - 1] < v[i]:
                countA += 1
        v.insert(i, n)
        return v

    @staticmethod
    def PA_Cardinality(n, m):
        if m == 0:
            return 1
        elif m == n:
            return 0
        else:
            s = 0
            for i in range(m + 1):
                s += (-1)**i * CombObject.Binomial(n + 1, i) * (m + 1 - i)**n
            return s

    def Cardinality(self):
        if (self.n and self.m) is not None:
            return self.PA_Cardinality(self.n, self.m)

    def ToVariant(self):
        if (self.object and self.n and self.m) is not None:
            self.variant = self._ToVariant(self.object, self.n, self.m)
            return self.variant

    def _ToVariant(self, a, n, m):
        v, va, vb = [], 0, 0
        aa = a.copy()
        for i in range(n, 0, -1):
            if va == n - m - 1 or vb == m:
                break
            as1 = self._CountAscents(aa)
            p = aa.index(i)
            k = self._CountAscents(aa[:p + 1])
            aa.remove(i)
            as2 = self._CountAscents(aa)
            if as1 == as2:
                v += [0, k + 1]
                va += 1
            else:
                v += [1, p - k + 1]
                vb += 1
            if va == n - m - 1 or vb == m:
                break
        return v

    def ToObject(self):
        if (self.variant and self.n and self.m) is not None:
            self.object = self._ToObject(self.variant, self.n, self.m)
            return self.object

    def _ToObject(self, v, n, m):
        a, s1, s2 = [], 0, 0
        vv = v.copy()
        for i in range(len(vv) // 2):
            if vv[2 * i] == 0:
                s1 += 1
            else:
                s2 += 1
        if s2 == m:
            for i in range(s1 + s2, n):
                vv += [0, 1]
        else:
            for i in range(s1 + s2, n):
                vv += [1, 1]
            vv += [0, 1]
        p = 2 * n - 1
        for i in range(n):
            if vv[p - 1] == 0:
                self._AddDescent(i + 1, vv[p] - 1, a)
            else:
                self._AddAscent(i + 1, vv[p] - 1, a)
            p -= 2
        return a

    def Rank(self):
        if (self.variant and self.n and self.m) is not None:
            self.rank = self._Rank(self.variant, self.n, self.m)
            return self.rank

    def _Rank(self, v, n, m):
        if m == 0 or m == n - 1:
            r = 0
        else:
            if v[0] == 0:
                r = v[1] - 1 + (m + 1) * self._Rank(v[2:], n - 1, m)
            else:
                r = v[1] - 1 + (n - m) * self._Rank(v[2:], n - 1, m - 1) + (m + 1) * self.PA_Cardinality(n - 1, m)
        return r

    def Unrank(self):
        if (self.rank and self.n and self.m) is not None:
            self.variant = self._Unrank(self.rank, self.n, self.m)
            return self.variant

    def _Unrank(self, r, n, m):
        if m == 0 or m == n - 1:
            v = []
        else:
            if r < (m + 1) * self.PA_Cardinality(n - 1, m):
                p = r % (m + 1)
                r //= (m + 1)
                v = [0, p + 1] + self._Unrank(r, n - 1, m)
            else:
                r -= (m + 1) * self.PA_Cardinality(n - 1, m)
                p = r % (n - m)
                r //= (n - m)
                v = [1, p + 1] + self._Unrank(r, n - 1, m - 1)
        return v
"""
a = PermutationWithAscents(n = 4, m = 2)
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