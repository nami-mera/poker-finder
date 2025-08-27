from flask import Flask
from flask_cors import CORS
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS
from db import db, init_db
from app.routers.tournament import tournament_bp
from logging_config import init_logging

init_logging()

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object('config')
    init_db(app)
    app.register_blueprint(tournament_bp, url_prefix='/api/tournament')

    @app.route("/dbtest")
    def dbtest():
        try:
            result = db.session.execute('SELECT 1')
            return "✅ 数据库连接成功！"
        except Exception as e:
            return f"❌ 数据库连接失败: {e}"
        
    return app
    
if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()  # 初始化表结构
    app.run(debug=True)