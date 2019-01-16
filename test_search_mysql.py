import MySQLdb


class MysqlSearch(object):

    def __init__(self):
        #  每次调用都要建立连接，还有就是给实例绑定属性，方便其他方法中调用
        self.conn = None
        self.get_conn()
    # 每一次查询都要获取连接，关闭连接，因此封装成公用方法

    def get_conn(self):
        try:
            #  给实例绑定属性，方便在其他方法中调用
            self.conn = MySQLdb.connect(
                host='127.0.0.1',
                user='test',
                passwd='1234',
                db='news',
                port=3306,
                charset='utf8'
            )

        except MySQLdb.Error as e:
            print('Error: %s' % e)

    def close_conn(self):
        try:
            if self.conn:
                self.conn.close()
        except MySQLdb.Error as e:
            print('Error: %s' % e)

    def get_one(self):
        #  准备SQL
        sql = 'SELECT * FROM news WHERE types = %s ORDER BY created_at DESC;'
        # 找到游标
        cursor = self.conn.cursor()
        # 执行 SQL
        cursor.execute(sql, ('最新',))
        # 拿到结果 desciption 是cursor的属性，返回第一个元素是字段的元祖，fetchone返回记录的元祖
        #  Zip 把两个序列对应匹配，形成元祖，dict转换成字典
        rest = dict(zip([k[0] for k in cursor.description], cursor.fetchone()))
        # 处理数据
        print(rest['title'])
        # 关闭游标，连接
        cursor.close()
        self.close_conn()

    def get_more(self):
        #  准备SQL
        sql = 'SELECT * FROM news WHERE types = %s ORDER BY created_at DESC;'
        # 找到游标
        cursor = self.conn.cursor()
        # 执行 SQL
        cursor.execute(sql, ('最新',))
        #  迭代结果集的每一行，每一行的记录是一个字典，把查到的字典转换成列表
        rest = [dict(zip([k[0] for k in cursor.description], row))
                for row in cursor.fetchall()]
        # 关闭游标，连接
        cursor.close()
        self.close_conn()
        return rest

    def get_more_by_page(self, page, page_size):
        #  分页查询 就是限制一次查询的固定记录数
        offset = (page - 1) * page_size
        #  准备SQL,第一个S是起始位置(从0开始)，第二个s 是页的大小也就是记录数
        sql = 'SELECT * FROM news WHERE types = %s ORDER BY created_at DESC LIMIT %s, %s;'
        # 找到游标
        cursor = self.conn.cursor()
        # 执行 SQL
        cursor.execute(sql, ('最新', offset, page_size))
        #  迭代结果集的每一行，每一行的记录是一个字典，把查到的字典转换成列表
        rest = [dict(zip([k[0] for k in cursor.description], row))
                for row in cursor.fetchall()]
        # 关闭游标，连接
        cursor.close()
        self.close_conn()
        return rest

    def add_one(self):
        try:
            # 准备SQL
            sql = 'INSERT news (title, content, types, author, is_valid) VALUES (%s, %s, %s, %s, %s);'
            #  获取链接和cursor
            cursor = self.conn.cursor()
            # 执行SQL 提交数据
            cursor.execute(sql, ('标题1', '内容1', '最新', '作者16', 1))
            cursor.execute(sql, ('标题2', '内容2', '最新', '作者17', 0))

            #  提交事务
            self.conn.commit()
            #  关闭cursor
            cursor.close()

        except MySQLdb.Error:
            print('error')
            #  rollback 的作用就是提交多条数据，一条错误，全部提交失败
            self.conn.rollback()
            #   self.conn.commit()  多条数据部分出错，commit 后，正确的SQL 语句依旧提交成功
        self.conn.close()

    def update_one(self):
        try:
            #  准备SQL
            sql = 'UPDATE news SET types=%s WHERE id=10; '
            # 获取连接和cursor
            cursor = self.conn.cursor()
            #  执行SQL
            cursor.execute(sql, ('当代',))
            #  提交事务
            self.conn.commit()
            #  关闭cursor
            cursor.close()

        except MySQLdb.Error:
            print('error')
            self.conn.rollback()

        self.close_conn()

    def delete_one(self):
        try:
            #  准备SQL
            sql = 'DELETE FROM news WHERE id=%s; '
            # 获取连接和cursor
            cursor = self.conn.cursor()
            # 执行SQL
            cursor.execute(sql, (16,))
            # 提交事务
            self.conn.commit()
            #  关闭cursor
        except MySQLdb.Error:
            print('error')
            self.conn.rollback()
        self.close_conn()


#  调用方法的入口
def main():
    obj = MysqlSearch()
    # obj.get_one()
    # rest = obj.get_more()
    # for item in rest:
    #     print(item)
    #     print('------')
    # rest = obj.get_more_by_page(2, 3)
    # for item in rest:
    #     print(item)
    #     print('------')
    # obj.add_one()
    # obj.update_one()
    obj.delete_one()

# 只有自身运行才调用main,被调用导入时屏蔽main
if __name__ == '__main__':
    main()
