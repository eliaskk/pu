# _*_ encoding:utf-8 _*_

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import sessionmaker

engine = create_engine("mysql://root:w1020392881@127.0.0.1/news_test?charset=utf8")
Base = declarative_base()

Session = sessionmaker(bind=engine)


class News(Base):
    __tablename__ = 'news'
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    content = Column(String(200), nullable=False)
    types = Column(String(10), nullable=False)
    image = Column(String(300))
    author = Column(String(20))
    view_count = Column(Integer)
    create_at = Column(DateTime)
    is_valid = Column(Boolean)


class OrmTest(object):
    def __init__(self):
        self.session = Session()

    def add_one(self):
        '''新增记录'''
        new_obj = News(
            title='title',
            content='content',
            types='1',
        )
        self.session.add(new_obj)
        self.session.commit()
        return new_obj

    def get_one(self):
        '''查询一条数据'''
        return self.session.query(News).get(2)

    def get_more(self):
        '''查询多条数据'''
        return self.session.query(News).filter_by(title='title')

    def update_data(self, pk):
        '''修改数据'''

        # 修改多条数据
        # data_list = self.session.query(News).filter_by(is_valid=True)
        # data_list = self.session.query(News).filter(News.id>5)
        # for item in data_list:
        #     item.is_valid = 0
        #     self.session.add(item)
        # self.session.commit()

        obj = self.session.query(News).get(pk)
        if obj:
            obj.is_valid = 1
            self.session.add(obj)
            self.session.commit()
            return True
        return False

    def delete_data(self, pk):
        '''删除数据'''
        # 获取要删除的数据
        new_obj = self.session.query(News).get(pk)
        self.session.delete(new_obj)
        self.session.commit()

obj = OrmTest()
obj.delete_data(2)
