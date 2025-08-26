import json
from flask import Blueprint, Response, request
from models.tournament import Tournament

tournament_bp = Blueprint('tournament', __name__)

@tournament_bp.route('/', methods=['GET'])
def list_tournament():
    data = Tournament.query.all()
    data = [t.to_dict() for t in data]
    resp = {
        "data": data
    }
    return Response(
        json.dumps(resp, ensure_ascii=False),
        content_type='application/json; charset=utf-8'
    )