
# 定义在G(2^8)中的乘法
def mul2(x):
    if(x & 0x80):
        return ((x << 1) ^ 27) & 255
    else:
        return (x << 1) & 255

# G(2^8)上的乘法
def mul(x, y):
    r, tmp = 0, x
    while y:
        # nonlocal r,tmp
        if y % 2:
            r ^= tmp
        tmp = mul2(tmp)
        y /= 2
        y = int(y)
    return r


def hight_index(x):
    if x == 0:
        return 0
    index = 1
    while x >> 1:
        x >>= 1
        index += 1
    return index

# G(2^8)上的除法
def divi(a, b):
    tmp, r, q = 0, 0, 0
    while b <= a:
        tmp = 1
        indexA, indexB = hight_index(a), hight_index(b)
        dis = indexA - indexB
        tmp = tmp << dis
        q += tmp
        a = a ^ (tmp*b)
    r = a

    return q, r

# ax + by = d = gcd(a,b), 其中a>b


def egcd(a, b):
    x1, y1, x2, y2 = 1, 0, 0, 1
    tmp_x, tmp_y = 0, 0
    while b:
        q, r = divi(a, b)
        tmp_x, tmp_y = x2, y2
        # 1式 - 2式 * q, 亦或就是减法
        x2, y2 = x1 ^ mul(x2, q), y1 ^ mul(y2, q)
        x1, y1 = tmp_x, tmp_y
        a, b = b, r
    return y1


def inverSbox():
    global s_box
    for i in range(16):
        for j in range(16):
            s_box[i][j] = i*16+j
    for i in range(16):
        for j in range(16):
            s_box[i][j] = egcd(283, s_box[i][j])


def getIndexBit(x, index):
    return (x >> index) & 1


def transform(x):
    trans_x = 0
    c = 0x63
    for i in range(8):
        tmp = 0
        tmp = getIndexBit(x, i) ^ getIndexBit(x, (i+4) % 8) ^ getIndexBit(x, (i+5) %
                                                                          8) ^ getIndexBit(x, (i+6) % 8) ^ getIndexBit(x, (i+7) % 8) ^ getIndexBit(c, i)
        trans_x = trans_x | (tmp << i)
    return trans_x


def transformSBox():
    global s_box
    for i in range(16):
        for j in range(16):
            s_box[i][j] = transform(s_box[i][j])


def printBox():
    for i in range(16):
        for j in range(16):
            print('%x' % inverse_s_box[i][j], " ", end="")
        print("")

# 将一个8bits的z转换为坐标x(x,y)


def getPosition(z):
    x = (z >> 4) & 15
    y = z & 15
    return x, y


def initInverSBox():
    global inverse_s_box
    for i in range(16):
        for j in range(16):
            x, y = getPosition(s_box[i][j])
            inverse_s_box[x][y] = i*16+j


# s_box = [([0]*16) for i in range(16)]
# inverse_s_box = [([0]*16) for i in range(16)]
# inverSbox()
# transformSBox()
# initInverSBox()
s_box = [[99, 124, 119, 123, 242, 107, 111, 197, 48, 1, 103, 43, 254, 215, 171, 118], [202, 130, 201, 125, 250, 89, 71, 240, 173, 212, 162, 175, 156, 164, 114, 192], [183, 253, 147, 38, 54, 63, 247, 204, 52, 165, 229, 241, 113, 216, 49, 21], [4, 199, 35, 195, 24, 150, 5, 154, 7, 18, 128, 226, 235, 39, 178, 117], [9, 131, 44, 26, 27, 110, 90, 160, 82, 59, 214, 179, 41, 227, 47, 132], [83, 209, 0, 237, 32, 252, 177, 91, 106, 203, 190, 57, 74, 76, 88, 207], [208, 239, 170, 251, 67, 77, 51, 133, 69, 249, 2, 127, 80, 60, 159, 168], [81, 163, 64, 143, 146, 157, 56, 245, 188, 182, 218, 33, 16, 255, 243, 210], [
    205, 12, 19, 236, 95, 151, 68, 23, 196, 167, 126, 61, 100, 93, 25, 115], [96, 129, 79, 220, 34, 42, 144, 136, 70, 238, 184, 20, 222, 94, 11, 219], [224, 50, 58, 10, 73, 6, 36, 92, 194, 211, 172, 98, 145, 149, 228, 121], [231, 200, 55, 109, 141, 213, 78, 169, 108, 86, 244, 234, 101, 122, 174, 8], [186, 120, 37, 46, 28, 166, 180, 198, 232, 221, 116, 31, 75, 189, 139, 138], [112, 62, 181, 102, 72, 3, 246, 14, 97, 53, 87, 185, 134, 193, 29, 158], [225, 248, 152, 17, 105, 217, 142, 148, 155, 30, 135, 233, 206, 85, 40, 223], [140, 161, 137, 13, 191, 230, 66, 104, 65, 153, 45, 15, 176, 84, 187, 22]]
inverse_s_box = [[82, 9, 106, 213, 48, 54, 165, 56, 191, 64, 163, 158, 129, 243, 215, 251], [124, 227, 57, 130, 155, 47, 255, 135, 52, 142, 67, 68, 196, 222, 233, 203], [84, 123, 148, 50, 166, 194, 35, 61, 238, 76, 149, 11, 66, 250, 195, 78], [8, 46, 161, 102, 40, 217, 36, 178, 118, 91, 162, 73, 109, 139, 209, 37], [114, 248, 246, 100, 134, 104, 152, 22, 212, 164, 92, 204, 93, 101, 182, 146], [108, 112, 72, 80, 253, 237, 185, 218, 94, 21, 70, 87, 167, 141, 157, 132], [144, 216, 171, 0, 140, 188, 211, 10, 247, 228, 88, 5, 184, 179, 69, 6], [208, 44, 30, 143, 202, 63, 15, 2, 193, 175, 189, 3, 1, 19, 138, 107], [
    58, 145, 17, 65, 79, 103, 220, 234, 151, 242, 207, 206, 240, 180, 230, 115], [150, 172, 116, 34, 231, 173, 53, 133, 226, 249, 55, 232, 28, 117, 223, 110], [71, 241, 26, 113, 29, 41, 197, 137, 111, 183, 98, 14, 170, 24, 190, 27], [252, 86, 62, 75, 198, 210, 121, 32, 154, 219, 192, 254, 120, 205, 90, 244], [31, 221, 168, 51, 136, 7, 199, 49, 177, 18, 16, 89, 39, 128, 236, 95], [96, 81, 127, 169, 25, 181, 74, 13, 45, 229, 122, 159, 147, 201, 156, 239], [160, 224, 59, 77, 174, 42, 245, 176, 200, 235, 187, 60, 131, 83, 153, 97], [23, 43, 4, 126, 186, 119, 214, 38, 225, 105, 20, 99, 85, 33, 12, 125]]
