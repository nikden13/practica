class CombObject:

    def __init__(self, object = None, variant = None, rank = None):
        self.object = object
        self.variant = variant
        self.rank = rank

    def Cardinality(self):
        pass

    def ToVariant(self):
        pass

    def ToObject(self):
        pass

    def Rank(self):
        pass

    def Unrank(self):
        pass

    @staticmethod
    def Factorial(n):
        a = 1
        for i in range(2, n + 1):
            a *= i
        return a

    @staticmethod
    def Binomial(n, m):
        a = 1
        b = 1
        if m > n:
            return 0
        if m < n - m:
            for i in range(n - m + 1, n + 1):
                a *= i
            for i in range(2, m + 1):
                b *= i
        else:
            for i in range(m + 1, n + 1):
                a *= i
            for i in range(2, n - m + 1):
                b *= i
        return int(a / b)
