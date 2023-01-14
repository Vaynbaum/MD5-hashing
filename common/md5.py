from math import sin
import struct


class MD5:
    def __init__(self):
        COUNT_ROUNDS = 16
        COUNT_STAGE=4
        self.__COUNT_ITERATIONS = COUNT_STAGE*COUNT_ROUNDS
        self.__TABLE_CONSTS = [int(0x100000000 * abs(sin(i))) for i in range(1, self.__COUNT_ITERATIONS+1)]
        self.__OFFSET = [ 
            7, 12, 17, 22,  7, 12, 17, 22,  7, 12, 17, 22,  7, 12, 17, 22,
            5,  9, 14, 20,  5,  9, 14, 20,  5,  9, 14, 20,  5,  9, 14, 20,
            4, 11, 16, 23,  4, 11, 16, 23,  4, 11, 16, 23,  4, 11, 16, 23,
            6, 10, 15, 21,  6, 10, 15, 21,  6, 10, 15, 21,  6, 10, 15, 21 ]
        self.__LEN_BLOCK = 512
        self.__LEN_BYTE = 8

    def __init(self, message: str):
        # Выравнивание потока
        m = message.encode("utf-8")
        len_message = (len(m) * self.__LEN_BYTE) % 0x10000000000000000
        m += struct.pack("B", 0x80)
        while True:
            m += struct.pack("B", 0x0)
            if (len(m) * self.__LEN_BYTE) % self.__LEN_BLOCK == 448:
                break
        # Добавление длины сообщения
        m += struct.pack("<Q", len_message)
        # Инициализация буфера
        buffer=[0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476]
        return m, buffer

    def __function_f(self, x: int, y: int, z: int) -> int:
        return (x & y) | (~x & z)

    def __function_g(self, x: int, y: int, z: int) -> int:
        return (x & z) | (~z & y)

    def __function_h(self, x: int, y: int, z: int) -> int:
        return x ^ y ^ z

    def __function_i(self, x: int, y: int, z: int) -> int:
        return y ^ (~z | x)

    def __rol(self, a: int, n: int) -> int:
        "Циклический сдвиг влево"
        n = n % (len(str(a)) * 8)
        t1 = a << n
        t2 = a >> (len(str(a)) * 8 - n)
        return t1 | t2

    def __modular_add(self, a, b):
        "Сложение чисел по модулю 2^32"
        return (a + b) % pow(2, 32)

    def Process(self, message: str):
        "Вычисление хэша сообщения"
        message_bytes, words = self.__init(message)
        message_len = len(message_bytes)
        step = self.__LEN_BLOCK // self.__LEN_BYTE
        # Берем сообщение блоками по 512 бит
        for i in range(0, message_len, step):
            block = message_bytes[i : i + step]
            # Делим блок на 16 подблоков по 32 бита
            x = struct.unpack("16L", block)
            a = words[0]
            b = words[1]
            c = words[2]
            d = words[3]
            for j in range(self.__COUNT_ITERATIONS):
                # 1 этап
                if 0 <= j <= 15:
                    f = self.__function_f(b, c, d)
                    k = j
                # 2 этап
                elif 16 <= j <= 31:
                    f = self.__function_g(b, c, d)
                    k = (5 * j + 1) % 16
                # 3 этап
                elif 32 <= j <= 47:
                    f = self.__function_h(b, c, d)
                    k = (3 * j + 5) % 16
                # 4 этап
                elif 48 <= i <= 63:
                    f = self.__function_i(b, c, d)
                    k = (7 * j) % 16
                f = self.__modular_add(f, x[k])
                f = self.__modular_add(f, self.__TABLE_CONSTS[j])
                f = self.__modular_add(f, a)
                f = self.__rol(f, self.__OFFSET[j])
                f = self.__modular_add(f, b)
                a = d
                d = c
                c = b
                b = f
            #  Прибавляем результат текущего "куска" к общему результату
            words[0] += a
            words[1] += b
            words[2] += c
            words[3] += d
        result = words[0] + (words[1] << 32) + (words[2] << 64) + (words[3] << 96)
        return f"{format(result, '08x')}"
