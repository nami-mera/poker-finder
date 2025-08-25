from flask import Blueprint, request, jsonify
from models.tournament import Tournament
from db import db_session

tournament_bp = Blueprint('tournament', __name__)

@tournament_bp.route('/', methods=['GET'])
def list_tournament():
    # 查询
    return jsonify([t.to_dict() for t in Tournament.query.all()])