from db import db
import json

class Tournament(db.Model):
    __tablename__ = 'tournaments'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    event_id = db.Column(db.Integer)
    event_name = db.Column(db.String(200))
    event_link = db.Column(db.String(500))
    status = db.Column(db.String(50))
    shop_id = db.Column(db.Integer)
    shop_name = db.Column(db.String(100))
    official_page = db.Column(db.String(200))
    start_time = db.Column(db.String(100))
    game_rule = db.Column(db.String(100))
    entry_fee = db.Column(db.Integer)
    re_entry = db.Column(db.String(100))
    prizes = db.Column(db.Text)
    prizes_original = db.Column(db.Text)
    address = db.Column(db.String(200))
    tel = db.Column(db.String(50))
    total_winners = db.Column(db.Integer)
    total_value_jpy = db.Column(db.Integer)
    reward_categories = db.Column(db.String(200))
    rank_list = db.Column(db.Text)

    
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
            "start_time": self.start_time,
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
            "rank_list": self.rank_list
        }

    def to_json(self):
        return json.dumps(self.to_dict(), ensure_ascii=False)