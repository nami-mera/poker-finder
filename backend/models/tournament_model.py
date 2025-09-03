from backend.db import db
import json
from sqlalchemy import text

class Tournament(db.Model):
    __tablename__ = 'tournaments'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    event_id = db.Column(db.Integer, nullable=False, unique=True)
    event_name = db.Column(db.String(200), nullable=False)
    event_link = db.Column(db.String(500), default='')
    start_date = db.Column(db.DateTime, nullable=False)
    start_time = db.Column(db.String(20), default='')
    late_time = db.Column(db.String(20), default='')
    entry_fee = db.Column(db.Integer, nullable=False, default=0)
    prizes_original = db.Column(db.Text)
    reward_categories = db.Column(db.String(200), default='')
    reward_summary = db.Column(db.Text)
    shop_id = db.Column(db.Integer, nullable=False)
    shop_name = db.Column(db.String(100), default='')
    shop_link = db.Column(db.String(200), default='')
    official_page = db.Column(db.String(200), default='')
    prefecture = db.Column(db.String(200), default='')
    city_ward = db.Column(db.String(200), default='')
    created_at = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now(), nullable=False)

    def __repr__(self):
        return self.to_json()

    def to_dict(self):
        return {
            "id": self.id,
            "event_id": self.event_id,
            "event_name": self.event_name,
            "event_link": self.event_link,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "start_time": self.start_time,
            "late_time": self.late_time,
            "entry_fee": self.entry_fee,
            # "prizes_original": self.prizes_original,
            "reward_categories": self.reward_categories,
            "reward_summary": self.reward_summary,
            "shop_id": self.shop_id,
            "shop_name": self.shop_name,
            "shop_link": self.shop_link,
            "official_page": self.official_page,
            "prefecture": self.prefecture,
            "city_ward": self.city_ward,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    def to_json(self):
        return json.dumps(self.to_dict(), ensure_ascii=False)

    @staticmethod
    def get_all_prefecture():
        sql = "SELECT DISTINCT prefecture FROM tournaments WHERE prefecture != '' ORDER BY prefecture"
        result = db.session.execute(text(sql))
        return [row[0] for row in result.fetchall()]

    @staticmethod
    def get_all_shop_name():
        sql = "SELECT DISTINCT shop_name FROM tournaments WHERE shop_name != '' ORDER BY shop_name"
        result = db.session.execute(text(sql))
        return [row[0] for row in result.fetchall()]

    @staticmethod
    def get_all_reward_categories():
        sql = "SELECT DISTINCT reward_categories FROM tournaments WHERE reward_categories != ''"
        result = db.session.execute(text(sql)).fetchall()
        categories = set()
        for row in result:
            rc_text = row[0]
            try:
                # 有的可能是json数组字符串
                cats = json.loads(rc_text)
                if isinstance(cats, list):
                    categories.update(cats)
                else:
                    # 万一有不是数组存储的，直接加进去
                    categories.add(str(cats))
            except Exception:
                # 解析失败，按纯文本添加
                categories.add(rc_text)
        return sorted(categories)
