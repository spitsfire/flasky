from flask import Blueprint, jsonify, request, abort, make_response
from app.models.ingredient import Ingredient
from app.routes.helpers import get_model_from_id
from app import db

ingredient_bp = Blueprint("ingredient", __name__, url_prefix="/ingredients")

@ingredient_bp.route('', methods=['GET'])
def get_all_ingredients():
    rating_query_value = request.args.get("rating")
    if rating_query_value is not None:
        ingredients = Ingredient.query.filter_by(rating=rating_query_value)
    else:
        ingredients = Ingredient.query.all()

    result = []
    for item in ingredients:
        result.append(item.to_dict())
    
    return jsonify(result), 200

@ingredient_bp.route('/<ingredient_id>', methods=['GET'])
def get_one_ingredient(ingredient_id):
    chosen_ingredient = get_model_from_id(Ingredient, ingredient_id)

    return jsonify(chosen_ingredient.to_dict()), 200

@ingredient_bp.route('', methods=['POST'])
def create_one_ingredient():
    request_body = request.get_json()

    new_ingredient = Ingredient.from_dict(request_body)
    
    db.session.add(new_ingredient)
    db.session.commit()

    return jsonify({"msg":f"Successfully created ingredient with id={new_ingredient.id}"}), 201