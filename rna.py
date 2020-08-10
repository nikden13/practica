from combobject import CombObject
import math

class RNA(CombObject):

    def __init__(self, object = None, variant = None, rank = None, n = None, m = None):
        super().__init__(object, variant, rank)
        self.n = n
        self.m = m

    @staticmethod
    def RNA_Cardinality(n, m):
        if m == 0:
            return 1
        elif m >= math.ceil(n / 2):
            return 0
        else:
            return int((1 / (n - m) * CombObject.Binomial(n - m, m) * CombObject.Binomial(n - m, m + 1)))

    def Cardinality(self):
        if (self.n and self.m) is not None:
            return self.RNA_Cardinality(self.n, self.m)

    def ToVariant(self):
        if (self.object and self.n and self.m) is not None:
            self.variant = self._ToVariant(self.object, self.n, self.m)
            return self.variant

    def _ToVariant(self, a, n, m):
        if m == 0:
            v = []
        elif a[0] == 0:
            v = [0] + [self._ToVariant([a[i] for i in range(1, n)], n - 1, m)]
        else:
            I, J = 0, 0
            s1, s2 = 0, 0
            for i in range(1, n + 1):
                if a[i - 1] == 1:
                    s1 += 1
                if a[i - 1] == -1:
                    s2 += 1
                if s1 == s2:
                    I = m - s1
                    J = n - i
                    break
            vl = self._ToVariant([a[i] for i in range(1, n - J - 1)], n - 2 - J, m - 1 - I)
            vr = self._ToVariant([a[i] for i in range(n - J, n)], J, I)
            v = [1, [I, J, vl, vr]]
        return v

    def ToObject(self):
        if (self.variant and self.n and self.m) is not None:
            self.object = self._ToObject(self.variant, self.n, self.m)
            return self.object

    def _ToObject(self, v, n, m):
        if m == 0:
            a = [0 for i in range(n)]
        elif v[0] == 0:
            a = [0] + self._ToObject(v[1], n - 1, m)
        else:
            [I, J, vl, vr] = v[1]
            b = self._ToObject(vl, n - 2 - J, m - 1 - I)
            c = self._ToObject(vr, J, I)
            a = [1] + b + [-1] + c
        return a

    def Rank(self):
        if (self.variant and self.n and self.m) is not None:
            self.rank = self._Rank(self.variant, self.n, self.m)
            return self.rank

    def _Rank(self, v, n, m):
        if m == 0:
            r = 0
        elif v[0] == 0:
            r = self._Rank(v[1], n - 1, m)
        else:
            [I, J, vl, vr] = v[1]
            l1 = self._Rank(vl, n - 2 - J, m - 1 - I)
            l2 = self._Rank(vr, J, I)
            s1, s2 = 0, 0
            for i in range(I):
                for j in range(2 * i, n - 2 * (m - i)):
                    s1 += self.RNA_Cardinality(n - 2 - j, m - 1 - i) * self.RNA_Cardinality(j, i)
            for i in range(2 * I, J):
                s2 += self.RNA_Cardinality(n - 2 - i, m - 1 - I) * self.RNA_Cardinality(i, I)
            r = l1 + self.RNA_Cardinality(n - 2 - J, m - 1 - I) * l2 + self.RNA_Cardinality(n - 1, m) + s1 + s2
        return r

    def Unrank(self):
        if (self.rank and self.n and self.m) is not None:
            self.variant = self._Unrank(self.rank, self.n, self.m)
            return self.variant

    def _Unrank(self, r, n, m):
        if m == 0:
            v = []
        elif r < self.RNA_Cardinality(n - 1, m):
            v = [0] + [self._Unrank(r, n - 1, m)]
        else:
            r -= self.RNA_Cardinality(n - 1, m)
            s, I, J = 0, 0, 0
            while s + self.RNA_Cardinality(n - 2 - J, m - 1 - I) * self.RNA_Cardinality(J, I) <= r:
                s += self.RNA_Cardinality(n - 2 - J, m - 1 - I) * self.RNA_Cardinality(J, I)
                if J <= n - 2 * (m - I) - 1:
                    J += 1
                else:
                    I += 1
                    J = 2 * I
            r -= s
            l1 = r % self.RNA_Cardinality(n - 2 - J, m - 1 - I)
            l2 = r // self.RNA_Cardinality(n - 2 - J, m - 1 - I)
            vl = self._Unrank(l1, n - 2 - J, m - 1 - I)
            vr = self._Unrank(l2, J, I)
            v = [1, [I, J, vl, vr]]
        return v

a = RNA(n = 7, m = 2)
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
