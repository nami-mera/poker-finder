import json
from sqlalchemy import inspect, Column, Integer, String, Text
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Shop(Base):
    __tablename__ = "poker_shop"
    id = Column(Integer, primary_key=True, autoincrement=True)
    shop_name = Column(String(100))
    shop_id = Column(Integer)
    shop_link = Column(String(500))
    address = Column(String(200))
    map_link = Column(String(500))
    phone = Column(String(50))
    homepage = Column(String(200))
    business_hours = Column(String(200))    

    def __repr__(self):
        return self.to_json()

    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self.__class__).attrs}

    def to_json(self):
        return json.dumps(self.to_dict(), ensure_ascii=False)


class Tournament(Base):
    __tablename__ = "tournaments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    event_id = Column(Integer)
    event_name = Column(String(200))
    event_link = Column(String(500))
    status = Column(String(50))
    shop_id = Column(Integer)
    shop_name = Column(String(100))
    official_page = Column(String(200))
    start_time = Column(String(100))
    game_rule = Column(String(100))
    entry_fee = Column(Integer)
    re_entry = Column(String(100))
    prizes = Column(Text)
    prizes_original = Column(Text)
    address = Column(String(200))
    tel = Column(String(50))
    total_winners = Column(Integer)
    total_value_jpy = Column(Integer)
    reward_categories = Column(String(200))
    rank_list = Column(Text)

    def __repr__(self):
        return self.to_json()

    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self.__class__).attrs}

    def to_json(self):
        return json.dumps(self.to_dict(), ensure_ascii=False)
