from db import db

class Shop(db.Model):
    __tablename__ = 'poker_shop'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    shop_name = db.Column(db.String(100), nullable=False)
    shop_id = db.Column(db.Integer, nullable=False, unique=True)
    shop_link = db.Column(db.String(500), default='')
    address = db.Column(db.String(200), default='')
    map_link = db.Column(db.String(500), default='')
    phone = db.Column(db.String(50), default='')
    homepage = db.Column(db.String(200), default='')
    business_hours = db.Column(db.String(200), default='')

    created_at = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now(), nullable=False)

    def __repr__(self):
        return f"<Shop id={self.id} shop_id={self.shop_id} name={self.shop_name}>"

    def to_dict(self):
        return {
            'id': self.id,
            'shop_name': self.shop_name,
            'shop_id': self.shop_id,
            'shop_link': self.shop_link,
            'address': self.address,
            'map_link': self.map_link,
            'phone': self.phone,
            'homepage': self.homepage,
            'business_hours': self.business_hours,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }