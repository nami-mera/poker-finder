import json
from flask import Blueprint, Response, request
from backend.models.tournament_model import Tournament
from sqlalchemy import and_, or_

tournament_bp = Blueprint('tournament', __name__)


@tournament_bp.route('/query', methods=['GET'])
def get_tournaments():
    # 模糊匹配，event_name，reward_summary，shop_name，address，prizes_original，reward_categories
    key_word = request.args.get("key_word", type=str)
    # 字符串模糊匹配，reward_categories
    reward_categories = request.args.get("reward_categories", type=str)
    # 数字范围，entry_fee
    min_entry_fee = request.args.get("min_entry_fee", type=int)
    max_entry_fee = request.args.get("max_entry_fee", type=int)
    # 完全匹配，city_ward，prefecture
    city_ward = request.args.get("city_ward", type=str)
    prefecture = request.args.get("prefecture", type=str)
    # shop_name，多选
    shop_name = request.args.get("shop_name", type=str)
    shop_name_array = shop_name.split(',') if shop_name else []

    # 时间选择器
    start_date = request.args.get("start_date", type=str)
    end_date = request.args.get("end_date", type=str)

    query = Tournament.query
    filters = []
    
    if key_word:
        key_word_filter = or_(
            Tournament.event_name.ilike(f"%{key_word}%"),
            Tournament.reward_summary.ilike(f"%{key_word}%"),
            Tournament.shop_name.ilike(f"%{key_word}%"),
            Tournament.prizes_original.ilike(f"%{key_word}%"),
            Tournament.reward_categories.ilike(f"%{key_word}%"),
        )
        filters.append(key_word_filter)
    if reward_categories:
        filters.append(Tournament.reward_categories.ilike(f"%{reward_categories}%"))
    if min_entry_fee is not None:
        filters.append(Tournament.entry_fee >= min_entry_fee)
    if max_entry_fee is not None:
        filters.append(Tournament.entry_fee <= max_entry_fee)
    if city_ward:
        filters.append(Tournament.city_ward == city_ward)
    if shop_name:
        filters.append(Tournament.shop_name.in_(shop_name_array))
    if prefecture:
        filters.append(Tournament.prefecture == prefecture)
    if start_date:
        filters.append(Tournament.start_date >= start_date)
    if end_date:
        filters.append(Tournament.start_date <= end_date)

    if filters:
        query = query.filter(and_(*filters))

    results = query.all()
    data = [t.to_dict() for t in results]
    resp = {
        "data": data,
        "total": len(data)
    }
    return Response(
        json.dumps(resp, ensure_ascii=False, default=str),
        content_type='application/json; charset=utf-8'
    )


@tournament_bp.route('/config', methods=['GET'])
def config():
    all_prefecture = Tournament.get_all_prefecture()
    all_shop_name = Tournament.get_all_shop_name()  
    all_reward_categories = Tournament.get_all_reward_categories()
    resp = {
        "data": {
            "all_prefecture": all_prefecture,
            "all_shop_name": all_shop_name,
            "all_reward_categories": all_reward_categories,
        }
    }
    return Response(
        json.dumps(resp, ensure_ascii=False, default=str),
        content_type='application/json; charset=utf-8'
    )