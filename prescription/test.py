# _*_ encoding:utf-8 _*_
import threading
from time import sleep


def music():
    for i in range(2):
        print "I was listening to music..."
        sleep(1)


def movie():
    for i in range(2):
        print "I was at the movie..."
        sleep(5)


threads = []
t1 = threading.Thread(music())
threads.append(t1)
t2 = threading.Thread(movie())
threads.append(t2)

for t in threads:
    # t.setDaemon(True)
    t.start()
