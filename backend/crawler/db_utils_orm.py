from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session

Base = declarative_base()

# 定义一个示例模型（表）
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    age = Column(Integer)

    def __repr__(self):
        return f"<User(id={self.id}, name={self.name}, age={self.age})>"


class MySQLHelper:
    def __init__(self, user, password, host, port, database):
        """
        初始化数据库连接
        """
        self.engine = create_engine(
            f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}",
            echo=False,  # 设置为 True 可以打印 SQL
            pool_size=5,
            pool_recycle=3600
        )
        self.Session = scoped_session(sessionmaker(bind=self.engine))

        # 如果表不存在则自动创建
        Base.metadata.create_all(self.engine)

    def add(self, obj):
        """插入数据"""
        session = self.Session()
        try:
            session.add(obj)
            session.commit()
            return obj.id
        except Exception as e:
            session.rollback()
            print("插入失败:", e)
        finally:
            session.close()

    def execute(self, sql, params=None):
        """执行指定sql"""
        session = self.Session()
        try:
            result = session.execute(sql, params)
            session.commit()
            return result
        except Exception as e:
            session.rollback()
            print("执行失败:", e)
        finally:
            session.close()

    def query_all(self, model):
        """查询所有记录"""
        session = self.Session()
        try:
            return session.query(model).all()
        except Exception as e:
            print("查询失败:", e)
            return []
        finally:
            session.close()

    def query_filter(self, model, **kwargs):
        """条件查询"""
        session = self.Session()
        try:
            return session.query(model).filter_by(**kwargs).all()
        except Exception as e:
            print("条件查询失败:", e)
            return []
        finally:
            session.close()

    def update(self, model, filters: dict, updates: dict):
        """更新记录"""
        session = self.Session()
        try:
            rows = session.query(model).filter_by(**filters).update(updates)
            session.commit()
            return rows
        except Exception as e:
            session.rollback()
            print("更新失败:", e)
            return 0
        finally:
            session.close()

    def delete(self, model, **kwargs):
        """删除记录"""
        session = self.Session()
        try:
            rows = session.query(model).filter_by(**kwargs).delete()
            session.commit()
            return rows
        except Exception as e:
            session.rollback()
            print("删除失败:", e)
            return 0
        finally:
            session.close()


if __name__ == "__main__":
    db = MySQLHelper(user="root", password="your_pass", host="localhost", port=3306, database="testdb")

    # 插入
    new_user = User(name="Alice", age=25)
    user_id = db.add(new_user)
    print("插入用户 ID:", user_id)

    # 查询所有
    users = db.query_all(User)
    print("所有用户:", users)

    # 条件查询
    users = db.query_filter(User, name="Alice")
    print("条件查询:", users)

    # 更新
    rows = db.update(User, {"name": "Alice"}, {"age": 26})
    print("更新行数:", rows)

    # 删除
    rows = db.delete(User, name="Alice")
    print("删除行数:", rows)
