import json
from flask import Blueprint, Response, request
from models.tournament_model import Tournament
from sqlalchemy import and_

tournament_bp = Blueprint('tournament', __name__)

# @tournament_bp.route('/', methods=['GET'])
# def list_tournament():
#     data = Tournament.query.all()
#     data = [t.to_dict() for t in data]
#     resp = {
#         "data": data
#     }
#     return Response(
#         json.dumps(resp, ensure_ascii=False),
#         content_type='application/json; charset=utf-8'
#     )


@tournament_bp.route('/', methods=['GET'])
def get_tournaments():
    event_name = request.args.get("reward_categories", type=str)
    min_total = request.args.get("min_total_value_jpy", type=int)
    max_total = request.args.get("max_total_value_jpy", type=int)
    
    query = Tournament.query

    filters = []
    
    if event_name:
        # 模糊匹配
        filters.append(Tournament.event_name.ilike(f"%{event_name}%"))
    if min_total is not None:
        filters.append(Tournament.total_value_jpy >= min_total)
    if max_total is not None:
        filters.append(Tournament.total_value_jpy <= max_total)

    if filters:
        query = query.filter(and_(*filters))

    results = query.all()

    data = [t.to_dict() for t in results]
    resp = {
        "data": data
    }
    return Response(
        json.dumps(resp, ensure_ascii=False),
        content_type='application/json; charset=utf-8'
    )