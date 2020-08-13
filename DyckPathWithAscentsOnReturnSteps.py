from CombObject import CombObject
from Combination import Combination
from DyckPathWithReturnSteps import DyckPathWithReturnSteps
from Permutation import Permutation
from PermutationWithAscents import PermutationWithAscents

class DyckPathWithAscentsOnReturnSteps(CombObject):

    def __init__(self, object = None, variant = None, rank = None, n = None, m = None):
        super().__init__(object, variant, rank)
        self.n = n
        self.m = m

    def Cardinality(self):
        if (self.n and self.m) is not None:
            return self._Cardinality(self.n, self.m)

    @staticmethod
    def _Cardinality(n, m):
        s = 0
        if n == m == 0:
            s = 1
        else:
            for i in range(m + 1, n + 1):
                s += DyckPathWithReturnSteps._Cardinality(n, i) * Combination._Cardinality(n, i) * PermutationWithAscents._Cardinality(i, m) * Permutation._Cardinality(n - i)
        return s

    def ToVariant(self):
        if (self.object and self.n and self.m) is not None:
            self.variant = self._ToVariant(self.object, self.n, self.m)
            return self.variant

    def _ToVariant(self, a, n, m):
        if n == 0:
            return []
        ct_object, e_object, c_object, p_object = a[0], [], [], []
        a2, a21, a22, s = a[1], [], [], 0
        for i in range(2 * n):
            if ct_object[i] == 1:
                s += 1
            else:
                s -= 1
                if s == 0:
                    a21.append(a2[0])
                else:
                    a22.append(a2[0])
                a2 = a2[1:]
        for i in range(1, n + 1):
            if i in a22:
                c_object.append(0)
            else:
                c_object.append(1)
        k = len(a21)
        for i in range(k):
            q = 0
            for j in range(k):
                if a21[i] >= a21[j]:
                    q += 1
            e_object.append(q)
        for i in range(n - k):
            q = 0
            for j in range(n - k):
                if a22[i] >= a22[j]:
                    q += 1
            p_object.append(q)
        v1 = DyckPathWithReturnSteps(object = ct_object, n = n, m = k).ToVariant()
        v2 = Combination(object = c_object, n = n, m = k).ToVariant()
        v3 = PermutationWithAscents(object = e_object, n = k, m = m).ToVariant()
        v4 = Permutation(object = p_object, n = n - k).ToVariant()
        return [k, v1, v2, v3, v4]

    def ToObject(self):
        if (self.variant and self.n and self.m) is not None:
            self.object = self._ToObject(self.variant, self.n, self.m)
            return self.object

    def _ToObject(self, v, n, m):
        if n == 0:
            return []
        a2, a21, a22, a23, a24, s = [], [], [], [], [], 0
        ct_object = DyckPathWithReturnSteps(variant = v[1], n = n, m = v[0]).ToObject()
        c_object = Combination(variant = v[2], n = n, m = v[0]).ToObject()
        e_object = PermutationWithAscents(variant = v[3], n = v[0], m = m).ToObject()
        p_object = Permutation(variant = v[4], n = n - v[0]).ToObject()
        for i in range(n):
            if c_object[i] == 1:
                a21.append(i + 1)
            else:
                a22.append(i + 1)
        for i in range(v[0]):
            a23.append(a21[e_object[i] - 1])
        for i in range(n - v[0]):
            a24.append(a22[p_object[i] - 1])
        for i in range(2 * n):
            if ct_object[i] == 1:
                s += 1
            else:
                s -= 1
                if s == 0:
                    a2.append(a23[0])
                    a23 = a23[1:]
                else:
                    a2.append(a24[0])
                    a24 = a24[1:]
        return [ct_object, a2]

    def Rank(self):
        if (self.variant and self.n and self.m) is not None:
            self.rank = self._Rank(self.variant, self.n, self.m)
            return self.rank

    def _Rank(self, v, n, m):
        if n == 0:
            return 0
        l1 = DyckPathWithReturnSteps(variant = v[1], n = n, m = v[0]).Rank()
        l2 = Combination(variant = v[2], n = n, m = v[0]).Rank()
        l3 = PermutationWithAscents(variant = v[3], n = v[0], m = m).Rank()
        l4 = Permutation(variant = v[4], n = n - v[0]).Rank()
        r0 = 0
        for i in range(m + 1, v[0]):
            r0 += DyckPathWithReturnSteps._Cardinality(n, i) * Combination._Cardinality(n, i) * PermutationWithAscents._Cardinality(i, m) * Permutation._Cardinality(n - i)
        return l1 + DyckPathWithReturnSteps._Cardinality(n, v[0]) * (l2 + Combination._Cardinality(n, v[0]) * (l3 + PermutationWithAscents._Cardinality(v[0], m) * l4)) + r0

    def Unrank(self):
        if (self.rank and self.n and self.m) is not None:
            self.variant = self._Unrank(self.rank, self.n, self.m)
            return self.variant

    def _Unrank(self, r, n, m):
        if n == 0:
            return []
        k = m + 1
        s = 0
        while s + DyckPathWithReturnSteps._Cardinality(n, k) * Combination._Cardinality(n, k) * PermutationWithAscents._Cardinality(k, m) * Permutation._Cardinality(n - k) <= r:
            s += DyckPathWithReturnSteps._Cardinality(n, k) * Combination._Cardinality(n, k) * PermutationWithAscents._Cardinality(k, m) * Permutation._Cardinality(n - k)
            k += 1
        r -= s
        ct = DyckPathWithReturnSteps._Cardinality(n, k)
        c = Combination._Cardinality(n, k)
        e = PermutationWithAscents._Cardinality(k, m)
        v1 = DyckPathWithReturnSteps(rank = r % ct, n = n, m = k)
        r //= ct
        v2 = Combination(rank = r % c, n = n, m = k)
        r //= c
        v3 = PermutationWithAscents(rank = r % e, n = k, m = m)
        v4 = Permutation(rank = r // e, n = n - k)
        return [k, v1.Unrank(), v2.Unrank(), v3.Unrank(), v4.Unrank()]