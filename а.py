import math

class Polynomial:
    def __init__(self, koff):
        self.koff = koff

    def __add__(self, other):
        max_len = max(len(self.koff), len(other.koff))
        nov_koff = [0] * max_len
        self_koff = self.koff[::-1]
        other_koff = other.koff[::-1]

        for i in range(max_len):
            koff_1 = self_koff[i] if i < len(self_koff) else 0
            koff_2 = other_koff[i] if i < len(other_koff) else 0
            nov_koff[i] = koff_1 + koff_2

        return Polynomial(nov_koff[::-1])

    def __sub__(self, other):
        max_len = max(len(self.koff), len(other.koff))
        nov_koff = [0] * max_len
        self_koff = self.koff[::-1]
        other_koff = other.koff[::-1]

        for i in range(max_len):
            koff_1 = self_koff[i] if i < len(self_koff) else 0
            koff_2 = other_koff[i] if i < len(other_koff) else 0
            nov_koff[i] = koff_1 - koff_2

        return Polynomial(nov_koff[::-1])

    def __mul__(self, other):
        new_koff = [0] * (len(self.koff) + len(other.koff) - 1)
        for i in range(len(self.koff)):
            coeff1 = self.koff[i]
            for j in range(len(other.koff)):
                coeff2 = other.koff[j]
                new_koff[i + j] += coeff1 * coeff2

        return Polynomial(new_koff)

    def __truediv__(self, other):
        if len(other.koff) == 0 or (len(other.koff) == 1 and other.koff[0] == 0):
            raise ZeroDivisionError("Деление на ноль.")

        if len(other.koff) > len(self.koff):
            print("Многочлен не делится нацело (делитель имеет более высокую степень).")
            return Polynomial([0])  # Возвращаем нулевой многочлен, так как деление невозможно
        delimoe = self.koff[:] #
        delitel = other.koff
        koefficient = [0] * (len(delimoe) - len(delitel) + 1)  # Предварительно выделяем память для частного

        degree_diff = len(delimoe) - len(delitel)
        for i in range(degree_diff + 1):
            lead_coeff = delimoe[i] / delitel[0]
            koefficient[i] = lead_coeff
            for j in range(len(delitel)):
                delimoe[i + j] -= lead_coeff * delitel[j]

        # Проверка на остаток - более корректный способ
        remainder = delimoe[degree_diff + 1:]
        if any(remainder):
            print("Многочлен не делится нацело, остаток:", remainder)

        return Polynomial(koefficient)

    def __str__(self):
        if not self.koff:
            return "0"
        terms = []
        for i, coeff in enumerate(self.koff):
            if coeff == 0:
                continue
            if coeff == 1 and i > 0:
                coeff_str = ""
            elif coeff == -1 and i > 0:
                coeff_str = "-"
            else:
                coeff_str = str(coeff)
            if i == 0:
                term = coeff_str
            elif i == 1:
                term = f"{coeff_str}x"
            else:
                term = f"{coeff_str}x^{i}"
            terms.append(term)
        return " + ".join(terms)
    def get_show(self):
        show = ''
        if self.koff is not None:
            for i in range(len(self.koff)):
                koff_n = self.koff[i]
                if koff_n != 0:
                    top = len(self.koff) - i - 1
                    show += f"{koff_n}x^{top} + "
            show = show[:-3]
        else:
            return "Коэффициенты отсутствуют."
        return show

    def get_proiz(self):
        koff_pr = []
        length = len(self.koff)

        for i in range(length):
            if length - 1 - i > 0:
                koff_pr.append(self.koff[i] * (length - 1 - i))

        proiz = Polynomial(koff_pr)
        return proiz.get_show()

    def get_point(self, point: float):
        value = 0.0
        for i in range(len(self.koff)):
            koff_n = self.koff[i]
            if koff_n != 0:
                top = len(self.koff) - i - 1
                value += koff_n * point ** top
        return value

    def get_zero(self):
        def find_divisors(n):
            divisors = []
            for i in range(1, n + 1):
                if n % i == 0:
                    divisors.append(i)
            return divisors
        a_0 = self.koff[-1]
        a_n = self.koff[0]
        if a_0 < 0:
            a_0 = -a_0
        if a_n < 0:
            a_n = -a_n
        a_0_koff = find_divisors(a_0) #q
        a_n_koff = find_divisors(a_n) #p

        zero = []
        list_x =[]

        for p in a_0_koff:
            for q in a_n_koff:
                list_x.append(p / q)
                list_x.append(-p / q)

        list_x_sort = sorted(set(list_x))

        for x in list_x_sort:
            result = self.get_point(float(x))
            if abs(result) < 0.000000001:
                zero.append(float(x))

        return zero

    def get_factor(self):
        zero = self.get_zero()
        k = Polynomial(self.koff)
        decay = []

        for root in zero:
            decay.append([1.0, -root])

        for factor in decay:
            k = k / Polynomial(factor)

        if k.koff == [1.0]:
            return decay
        else:
            decay.append(k.koff)
            return decay

    def get_nod(self, other):
        """Находит наибольший общий делитель двух многочленов."""

        n1 = Polynomial(self.koff)  # Предполагается, что self.koff - это список коэффициентов
        n2 = Polynomial(other.koff)  # Предполагается, что other.koff - это список коэффициентов

        def normalize_polynomial(poly):
            """Нормализует многочлен, деля на НОД коэффициентов."""
            if not poly.koff:  # обработка случая пустого многочлена
                return Polynomial([0])
            gcd_coeff = math.gcd(*poly.koff)  # используем функцию gcd из math
            return Polynomial([c // gcd_coeff for c in poly.koff])

        n1 = normalize_polynomial(n1)
        n2 = normalize_polynomial(n2)

        factors1 = n1.get_factor()
        factors2 = n2.get_factor()

        common_factors = []
        for factor1 in factors1:
            for factor2 in factors2:
                if factor1 == factor2:  # Проверка на равенство после нормализации
                    common_factors.append(factor1)
                    break  # если нашли совпадение - идем дальше

        if not common_factors:
            return Polynomial([0])

        n_n = Polynomial([1])
        for factor in common_factors:
            n_n = n_n * Polynomial(factor)

        return n_n.get_show()
    def get_file(self, file_name):
        show = self.get_show()
        with open(file_name, 'w') as file:
            file.write(show)
k1 =Polynomial ([1,1,2,4])
k2 =Polynomial ([2,1,2,4])
print(k1.__add__(k2))

