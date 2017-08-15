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
    e = fg.encrypt("87,10,19,77,143,14,38,257,165,378,481,579,596,632,644,41,446,519")
    print e
    # d = fg.fliggy(e)
    # print d
    # print '-'
    # fgfdict2 = open(r'F:\wushijia\workspace\726\update\weight2q.txt', 'r')
    # fgfdict2Text = fgfdict2.readlines()
    # fgfdict2.close()
    # for line in fgfdict2Text:
    #     line = line[:line.find('\n')]
    #     print fg.encrypt(line)

