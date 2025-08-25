from flask import Flask
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS, SECRET_KEY
from db import db, init_db
from routers.tournament import user_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object('config')
    init_db(app)
    app.register_blueprint(user_bp, url_prefix='/api/users')
    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()  # 初始化表结构
    app.run(debug=True)