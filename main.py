import hashlib

NUM1 = 89178634375
NUM2 = 89868029530
NUM3 = 89856014239
NUM4 = 89649710998
NUM5 = 89858857607

SALTS = [11111111, 22222222, 33333333, 44444444, 55555555, 66666666, 77777777, 88888888, 99999999,
         123456789, 1000000, 9999999, 381, 1, 226677881]
saltsArr = [0] * len(SALTS)
md5s = [0] * len(SALTS)
sha1s = [0] * len(SALTS)
sha256s = [0] * len(SALTS)


def addDict(key, dict):
    if key not in dict.keys():
        dict.setdefault(key, 1)
    else:
        dict[key] += 1


def writeToFile(file, array):
    f = open(file, "w")
    for i in range(len(array)):
        f.write(str(array[i]) + '\n')
    f.close()


def hashMD5(data):
    h = hashlib.md5(str(data).encode('utf-8'))
    return h.hexdigest()


def hashSHA1(data):
    h = hashlib.sha1(str(data).encode('utf-8'))
    return h.hexdigest()


def hashSHA256(data):
    h = hashlib.sha256(str(data).encode('utf-8'))
    return h.hexdigest()


numbers = []
dictt = {}

f = open("hacked.txt", "r")
lines = f.readlines()
for line in lines:
    numbers.append(int(line[-12:-1]))

# вычитаем из данных эталонные номера
ar1 = list(map(lambda x: x - NUM1, numbers))
ar2 = list(map(lambda x: x - NUM2, numbers))
ar3 = list(map(lambda x: x - NUM3, numbers))
ar4 = list(map(lambda x: x - NUM4, numbers))
ar5 = list(map(lambda x: x - NUM5, numbers))

# составляем словарь солей
for i in range(len(ar1)):
    addDict(ar1[i], dictt)
    addDict(ar2[i], dictt)
    addDict(ar3[i], dictt)
    addDict(ar4[i], dictt)
    addDict(ar5[i], dictt)

# ищем соль, которая встречается 5 раз, это и есть искомая соль
salt0 = 0  # 34000319
for key, value in dictt.items():
    if value == 5:
        salt0 = key
        print(key)

# ищем оригинальные номера без соли и солим их тестовыми солями
noSaltNumbers = list(map(lambda x: x - salt0, numbers))
writeToFile("noSaltNumbers.txt", noSaltNumbers)

# хешируем номера и записываем хеши в файлы
for i in range(len(SALTS)):
    saltsArr[i] = list(map(lambda x: x + SALTS[i], noSaltNumbers))

    md5s[i] = list(map(lambda x: hashMD5(x), saltsArr[i]))
    writeToFile("md5_%i.txt" % i, md5s[i])

    sha1s[i] = list(map(lambda x: hashSHA1(x), saltsArr[i]))
    writeToFile("sha1_%i.txt" % i, sha1s[i])

    sha256s[i] = list(map(lambda x: hashSHA256(x), saltsArr[i]))
    writeToFile("sha256_%i.txt" % i, sha256s[i])
