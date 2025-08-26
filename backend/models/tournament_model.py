from db import db
import json

class Tournament(db.Model):
    __tablename__ = 'tournaments'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    event_id = db.Column(db.Integer, nullable=False, unique=True)
    event_name = db.Column(db.String(200), nullable=False)
    event_link = db.Column(db.String(500), default='')
    status = db.Column(db.String(50), nullable=False, default='upcoming')
    shop_id = db.Column(db.Integer, nullable=False)
    shop_name = db.Column(db.String(100), default='')
    official_page = db.Column(db.String(200), default='')
    start_time = db.Column(db.DateTime, nullable=False)
    game_rule = db.Column(db.String(100), default='')
    entry_fee = db.Column(db.Integer, nullable=False, default=0)
    re_entry = db.Column(db.String(100), default='')
    prizes = db.Column(db.Text, nullable=False)
    prizes_original = db.Column(db.Text, default='')
    address = db.Column(db.String(200), default='')
    tel = db.Column(db.String(50), default='')
    total_winners = db.Column(db.Integer, nullable=False, default=0)
    total_value_jpy = db.Column(db.Integer, nullable=False, default=0)
    reward_categories = db.Column(db.String(200), default='')
    rank_list = db.Column(db.Text, default='')

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
            "status": self.status,
            "shop_id": self.shop_id,
            "shop_name": self.shop_name,
            "official_page": self.official_page,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "game_rule": self.game_rule,
            "entry_fee": self.entry_fee,
            "re_entry": self.re_entry,
            "prizes": self.prizes,
            "prizes_original": self.prizes_original,
            "address": self.address,
            "tel": self.tel,
            "total_winners": self.total_winners,
            "total_value_jpy": self.total_value_jpy,
            "reward_categories": self.reward_categories,
            "rank_list": self.rank_list,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    def to_json(self):
        return json.dumps(self.to_dict(), ensure_ascii=False)