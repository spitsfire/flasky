from flask import Blueprint, jsonify, request, abort, make_response
from app import db
from app.models.breakfast import Breakfast
from app.models.menu import Menu

'''
class Breakfast():
    def __init__(self, id, name, rating, prep_time): # items, calories, 
        self.id = id
        self.name = name
        self.rating = rating
        self.prep_time = prep_time

breakfast_items = [
    Breakfast(1, "omelette", 4, 10),
    Breakfast(2, "french toast", 3, 15),
    Breakfast(3, "cereal", 1, 1),
    Breakfast(4, "oatmeal", 3, 10)
]
'''

breakfast_bp = Blueprint("breakfast", __name__, url_prefix="/breakfast")

@breakfast_bp.route('', methods=['GET'])
def get_all_breakfasts():
    rating_query_value = request.args.get("rating")
    if rating_query_value is not None:
        breakfasts = Breakfast.query.filter_by(rating=rating_query_value)
    else:
        breakfasts = Breakfast.query.all()

    #return("hello world")
    result = []
    
    for item in breakfasts:
        result.append(item.to_dict())
    
    return jsonify(result), 200

@breakfast_bp.route('/<breakfast_id>', methods=['GET'])
def get_one_breakfast(breakfast_id):
    chosen_breakfast = get_model_from_id(Breakfast, breakfast_id)

    return jsonify(chosen_breakfast.to_dict()), 200

@breakfast_bp.route('', methods=['POST'])
def create_one_breakfast():
    request_body = request.get_json()

    new_breakfast = Breakfast.from_dict(request_body)
    
    db.session.add(new_breakfast)
    db.session.commit()

    return jsonify({"msg":f"Successfully created Breakfast with id={new_breakfast.id}"}), 201
    
@breakfast_bp.route('/<breakfast_id>', methods=['PUT'])
def update_one_breakfast(breakfast_id):
    update_breakfast = get_model_from_id(Breakfast, breakfast_id)

    request_body = request.get_json()

    try:
        update_breakfast.name = request_body["name"]
        update_breakfast.rating = request_body["rating"]
        update_breakfast.prep_time = request_body["prep_time"]
    except KeyError:
        return jsonify({"msg": "Missing needed data"}), 400
    
    db.session.commit()
    return jsonify({"msg": f"Successfully updated breakfast with id {update_breakfast.id}"}), 200

@breakfast_bp.route('/<breakfast_id>', methods=['DELETE'])
def delete_one_breakfast(breakfast_id):
    breakfast_to_delete = get_model_from_id(Breakfast, breakfast_id)

    db.session.delete(breakfast_to_delete)
    db.session.commit()

    return jsonify({"msg": f"Successfully deleted breakfast with id {breakfast_to_delete.id}"}), 200


@breakfast_bp.route('/<breakfast_id>/', methods=['PATCH'])
def add_menu_to_breakfast(breakfast_id):
    breakfast = get_model_from_id(Breakfast, breakfast_id)

    request_body = request.get_json()

    try:
        menu_id = request_body['menu_id']
    except KeyError:
        return jsonify({"msg": "Missing menu id"}), 400

    menu = get_model_from_id(Menu, menu_id)

    breakfast.menu = menu
    
    db.session.commit()
    return jsonify({"msg": f"Added {breakfast.name} to {menu_id}"})



def get_model_from_id(cls, model_id):
    try:
        model_id = int(model_id)
    except ValueError:
        return abort(make_response({"msg": f"invalid id for model of type {cls.__name__}: {model_id}"}, 400))

    chosen_object = cls.query.get(model_id)

    if chosen_object is None:
        return abort(make_response({"msg": f"Could not find {cls.__name__} item with id: {model_id}"}, 404))
    
    return chosen_object

    
