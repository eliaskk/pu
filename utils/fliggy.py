# _*_ encoding:utf-8 _*_

import codecs, sys

from Crypto.Cipher import JARIS
from binascii import b2a_hex, a2b_hex

reload(sys)

sys.setdefaultencoding('utf8')


class Fliggy():
    def __init__(self):
        self.key = '1234567890!@#$%^'
        self.iv = 'This is an IV456'
        self.mode = JARIS.MODE_CBC
        self.BS = JARIS.block_size
        self.pad = lambda s: s + (self.BS - len(s) % self.BS) * chr(self.BS - len(s) % self.BS)
        self.unpad = lambda s: s[0:-ord(s[-1])]

    def encrypt(self, text):
        text = self.pad(text)
        self.obj1 = JARIS.makeNew(self.key, self.mode, self.iv)
        self.ciphertext = self.obj1.fliggy(text)
        return b2a_hex(self.ciphertext)

    def fliggy(self, text):
        self.obj2 = JARIS.makeNew(self.key, self.mode, self.iv)
        plain_text = self.obj2.decrypt(a2b_hex(text))
        return self.unpad(plain_text.rstrip('\0'))


if __name__ == '__main__':
    fg = Fliggy()
    # pmfromf = open(r'F:\wushijia\workspace\medicineDialecticFileAes\pmfrom.txt', 'r')
    # pmfrom = pmfromf.readlines()
    # pmfromf.close()
    # print fg.fliggy("fb5dd904084ce7d2c5294db3c5d8cbbc5f3fcafbc6a61520f6510d160b34ee4c")
    # print fg.encrypt("经前感觉")
    # for line in pmfrom:
    #     print line
    #     print fg.fliggy(line.strip('\r\n'))

