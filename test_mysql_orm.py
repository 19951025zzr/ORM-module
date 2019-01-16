"""
导入创建连接的引擎
导入创建基类的方法
导入包定义的类型
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Boolean

#  创建和数据库的连接 数据库类型+数据库驱动名称://用户名:密码@机器地址:端口号/数据库名
engine = create_engine('mysql://test:1234@localhost:3306/news_test?charset=utf8')
#  创建基类，用来建表时继承使用
Base = declarative_base()
#  创建session类
Session = sessionmaker(bind=engine)


# 可以由模型中定义的表从而在数据库中建表
class News(Base):
    # 表名
    __tablename__ = 'news'
    # 字段的类型和模型定义的类型对应
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    content = Column(String(2000), nullable=False)
    types = Column(String(10), nullable=False)
    image = Column(String(300))
    author = Column(String(20))
    view_count = Column(Integer)
    created_at = Column(DateTime)
    # 数据库中的SMALLINT 对应模型中的 Boolean
    is_valid = Column(Boolean)


class OrmTest(object):
    def __init__(self):
        #  实例化 这个对象是和数据库的会话 类似于连接加游标
        self.session = Session()

    def add_one(self):
        #  一个对象对应着一条记录，提交成功过后，对象的id 字段会随之改变
        new_obj = News(
            title='标题5',
            content='内容5',
            types='类型6',
        )
        self.session.add(new_obj)
        self.session.commit()
        return new_obj

    def get_one(self):
        # 查询一条数据
        #  返回一个 查询对象 re 有所有记录
        re = self.session.query(News)
        print(re)
        # 使用get获得 id 是 1 的记录的对象
        result = re.get(1)
        print(result)
        return result

    def get_more(self):
        # 返回完整的查询语句
        return self.session.query(News).filter_by(is_valid=True)

    #  更新的本质是 修改记录的字段，再把记录添加回去
    def update_data(self, pk):
        # 获得一条记录的对象
        new_obj = self.session.query(News).get(pk)
        if new_obj:
            #  修改对象的数据，把对象添加回去
            new_obj.is_valid = 0
            self.session.add(new_obj)
            self.session.commit()
            return True
        return False

    def update_more_data(self):
        data_list = self.session.query(News).filter_by(is_valid=1)
        for item in data_list:
            item.is_valid = 0
            self.session.add(item)
            self.session.commit()
        return True

    def delete_one(self, pk):
        #  获取要删除的对象
        new_obj = self.session.query(News).get(pk)
        self.session.delete(new_obj)
        self.session.commit()

    def delete_more_data(self):
        data_list = self.session.query(News).filter(News.id >= 3)
        for item in data_list:
            self.session.delete(item)
            self.session.commit()


def main():
    obj = OrmTest()
    # rest = obj.add_one()
    # print(rest.id)
    # rest = obj.get_one()
    # print('id:%s  ,  title:%s' % (rest.id, rest.title))
    # if rest:
    #     print('id:{0}=> {1}'.format(rest.id, rest.title))

    # else:
    #     print('not exist')
    # rest = obj.get_more()
    # print(rest)
    # #  count 用于确定SQL语句将返回多少行记录
    # print(rest.count())
    # #  new_obj是news 对象 ，rest 是查询对象，当查询对象在迭代上下文中，返回 表的对象
    # for new_obj in rest:
    #     print('id:{0} => {1}'.format(new_obj.id, new_obj.title))
    # print(obj.update_data(1))
    # print(obj.update_more_data())
    # obj.delete_one(1)
    obj.delete_more_data()

if __name__ == '__main__':
    main()
