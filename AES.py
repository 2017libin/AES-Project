from AESOperate import *

m = [[0]*4 for i in range(4)]
key = [0 for i in range(16)]
w = [[0]*4 for i in range(44)]


# 更新W
def updateW():
    global w
    w = keyExpansion(key)


def getW():
    return w


def getM():
    return m

# 输入明文

def setM(M):
    global m
    # 将一串密钥转换为数组
    arr = [0 for i in range(16)]
    for i in range(16):
        tmp = M >> (8*i)
        arr[15-i] = tmp & 0xff

    for j in range(4):
        for i in range(4):
            m[i][j] = arr[j*4+i]

# 输入密钥


def setKey(k):
    global key
    # 把一串密钥转换为数组
    arr = [0 for i in range(16)]
    for i in range(16):
        tmp = k >> (8*i)
        arr[15-i] = tmp & 0xff

    for i in range(16):
        key[i] = arr[i]


def firstRound():
    global m
    m = addRoundKey(m, w, 0)


def midRounds():
    global m
    for z in range(1, 10):
        tmp = shiftRows(m)
        for j in range(4):
            x0, y0 = getPosition(tmp[0][j])
            x1, y1 = getPosition(tmp[1][j])
            x2, y2 = getPosition(tmp[2][j])
            x3, y3 = getPosition(tmp[3][j])
            t0, t1, t2, t3 = T0[x0][y0], T1[x1][y1], T2[x2][y2], T3[x3][y3]
            # 本轮密钥
            k = w[z*4+j]
            for i in range(4):
                m[i][j] = (t0[i] ^ t1[i] ^ t2[i] ^ t3[i] ^ k[i])


def lastRound():
    global m
    m = substituteBytes(m)
    m = shiftRows(m)
    m = addRoundKey(m, w, 40)


def inverseFirstRound():
    global m
    addRoundKey(m, w, 40)
#     print(m)


def inverseMidRounds():
    global m
    for i in range(1, 10):
        m = inverseShiftRows(m)
        m = inverseSubtituteBytes(m)
        m = addRoundKey(m, w, (40-i*4))
        m = inverseMixColums(m)
        # print(m)


def inverseLastRounds():
    global m
    m = inverseShiftRows(m)
    m = inverseSubtituteBytes(m)
    m = addRoundKey(m, w, 0)
#     print("")


def getM():
    tmp = 0
    for i in range(4):
        for j in range(4):
            dis = ((3-j)*4+3-i)*8
            tmp = tmp | (m[i][j] << dis)
        #     print("%x" % tmp)
    # 将结果转换为字符串
    string = hex(tmp)+""
    string = string[2:]
    if len(string) < 32:
        string = (32-len(string))*"0" + string

    return string
