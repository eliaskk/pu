# _*_ encoding:utf-8 _*_


class Parent:
    def __init__(self):
        print "父类初始化了"

    def show(self):
        print "this is parent's show"


class Child(Parent):
    sex = "man"

    def __init__(self):
        Parent.__init__(self)
        print "子类初始化了"

    def show(self):
        print self.__sex
        print "this is child's show"

c = Child()
print c.sex
