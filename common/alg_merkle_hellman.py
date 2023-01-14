import math
import random

from common.const import COUNT_BITS


class AlgMerkleHellman:
    def __init__(self):
        self.__primes = self.__sieve_sundarama(2000)
        self.__private_key = None

    def __create_keys(self):
        "Создание ключей"
        seq, weight = self.__super_growing_sequence(COUNT_BITS)
        r = None
        q = None
        private_key = None
        public_key = None

        "Сумма весов и поиск простого числа большего суммы"
        for num in self.__primes:
            if num > weight:
                q = num
                break

        if q is not None:
            "Поиск взаимно простого числа с q"
            while True:
                r = random.randint(2, q)
                a, x2, y2 = self.__gsd_advance(q, r, 0, 1, 1, 0)
                if a == 1:
                    break

            if r is not None:
                private_key = {
                    "sequence": seq,
                    "q": q,
                    "r": r,
                }
                public_key = [(s * r) % q for s in seq]

        return public_key, private_key

    def __gsd_advance(self, a: int, b: int, x1: int, x2: int, y1: int, y2: int):
        "Расширенный алгоритм Евклида"
        if b == 0:
            return a, x2, y2
        else:
            tmp = a % b
            div = a // b
            a = b
            b = tmp
            adXi = x2 - div * x1
            adYi = y2 - div * y1
            return self.__gsd_advance(a, b, adXi, x1, adYi, y1)

    def __super_growing_sequence(self, count: int):
        "Создание супер-возрастающей последовательности"
        first = random.randint(2, 5)
        seq = [first]
        sum = first

        for i in range(count - 1):
            num = sum + random.randint(2, 20) + i
            sum += num
            seq.append(num)
        return seq, sum

    def __sieve_sundarama(self, num: int):
        "Получение простых чисел 'Решетом Сундарама'"
        len = num + 1
        primes = [i for i in range(len)]
        res = [2]

        for i in range(1, math.floor(math.sqrt(2 * num + 1) / 2)):
            for j in range(i, math.floor((num - i) / (2 * i + 1))):
                ind = i + j + 2 * i * j
                if (ind) <= num:
                    primes[ind] = 0

        for i in range(1, len):
            if primes[i] != 0:
                res.append(primes[i] * 2 + 1)
        return res

    def CreateKeys(self):
        "Создание ключей"
        public_key, private_key = self.__create_keys()
        self.__private_key = private_key
        return public_key

    def Decrypt(self, text: str):
        "Расшифровка текста"
        q = self.__private_key["q"]
        "Поиск обратного числа для r по модулю q"
        a, x2, y2 = self.__gsd_advance(q, self.__private_key["r"], 0, 1, 1, 0)
        while y2 < 0:
            y2 += q

        res = ""
        seq = self.__private_key["sequence"]
        for ch in text:
            dec = 0
            ind_arr = len(seq) - 1
            dec_num = (ord(ch) * y2) % q

            while dec_num > 0:
                if seq[ind_arr] <= dec_num:
                    dec |= 1 << (COUNT_BITS - ind_arr - 1)
                    dec_num -= seq[ind_arr]
                ind_arr -= 1
            res += chr(dec)
        return res

    def Encrypt(self, text: str, key: list[int]):
        "Зашифровка текста"
        result = []
        for ch in text:
            num = 0
            # Проходим по битам
            for num_bit in range(COUNT_BITS):
                bit = (ord(ch) >> num_bit) & 1
                num += bit * key[COUNT_BITS - 1 - num_bit]
            result.append(num)
        return "".join([chr(s) for s in result])