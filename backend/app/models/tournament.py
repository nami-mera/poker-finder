from db import db

class Tournament(db.Model):
    __tablename__ = 'tournament'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    bonus = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return dict(id=self.id, name=self.name, bonus=self.bonus)