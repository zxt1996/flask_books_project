图书管理

1.配置数据库
   a.导入SQLAlchemy扩展
   b.创建db对象，并配置参数
   c.终端创建数据库

2.添加书和作者模型
   a.模型继承db.Model
   b.__tablename__:表名
   c.db.Column:字段
   d.db.relationship：关系引用

3.添加数据

4.使用模板显示数据库查询的数据
    a.查询所有的作者信息，让信息传递给模板
    b.模板中按照格式，依次for循环作者和书籍即可（作者获取书籍，用的是关系引用）

5.使用WTF显示表单
   a.自定义表单类
   b.模板中显示
   c.secret_key/编码/csrf_token

6.实现相关的增删逻辑
   a.增加数据
   b.删除书籍  url_for的使用  / for else 的使用   / redirect的使用
   c.删除作者
