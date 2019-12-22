# encoding:utf-8
from AES import *
import sys
k = 0x0f1571c947d9e8590cb7add6af7f6798
padding_len = 0


# 输入：字节流  ---》 输出：字符串
def AESEncode(m_bytes, key):
    global padding_len
    padding_len = 0
    en_string = ""
    # m_bytes = m_string.encode()
    numbers = int(len(m_bytes)/16)+1
    M = str(bytearray(m_bytes).hex())

    # 扩展密钥
    setKey(key)
    updateW()

    # 除了最后一块以外的16bytes的密文加密
    for i in range(numbers):
        if i != (numbers-1):
            # 每2个十六进制数1个字节，16个字节有32个十六进制数
            block = int(M[i*32:i*32+32], 16)
            setM(block)
            # 加密
            firstRound()
            midRounds()
            lastRound()
            # 将加密密文添加到en_string
            en_string = en_string + getM()

        else:
            if (len(M) % 16) != 0:
                # 取剩余部分
                block = int(M[i*32:], 16)
                # 记录填充长度
                padding_len = 32 - len(M) % 32
                setM(block)
                # 加密
                firstRound()
                midRounds()
                lastRound()
                # 将加密密文添加到en_string
                en_string = en_string + getM()
    return en_string


def AESDecode(C, key):
    # 扩展密钥
    setKey(key)
    updateW()
    de_string = ""
    numbers = int(len(C)/32)

    for i in range(numbers):
        block = int(C[i*32:i*32+32], 16)
        setM(block)

        # 解密
        inverseFirstRound()
        inverseMidRounds()
        inverseLastRounds()

        de_string = de_string + getM()

    m1 = de_string[:(numbers-1)*32]
    m2 = de_string[((numbers-1)*32+padding_len):]
    m3 = m1 + m2
    return m3


# 将filename加密
def enFile(filename):
    # 以字节流的形式读出
    f = open(filename, "rb")
    string = (f.read())
    f.close()
    C = AESEncode(string, k)

    # 覆盖写密文
    f = open(filename, "w")
    f.write(C+"$"+str(padding_len))
    f.close()

# 将filename解密


def deFile(filename):
    global padding_len
    f = open(filename, "r")
    text = f.read()
    f.close()

    arr = text.split("$")
    padding_len = int(arr[1], 10)
    b = AESDecode(arr[0], k)

    plaintext = bytearray.fromhex(b)

    # 覆盖写明文
    f = open(filename, "wb")
    # 以字节流的形式写回去
    f.write(bytearray.fromhex(b))
    f.close()


if __name__ == "__main__":
    if sys.argv[1] == "-help":
        print("You can select the following options to do so\n",
              "encode file: -encode filename\n", "decode file: -decode filename")
    elif sys.argv[1] == "-encode":
        enFile(sys.argv[2])
        print("Encryption successful!\n")
    elif sys.argv[1] == "-decode":
        deFile(sys.argv[2])
        print("Decrypting successfully!\n")
    else:
        print("Entered an invalid option!")
