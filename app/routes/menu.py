from flask import Blueprint, jsonify, request, abort, make_response
from app import db
from app.models.menu import Menu
from app.routes.breakfast import get_model_from_id

menu_bp = Blueprint("menu", __name__, url_prefix="/menu")

@menu_bp.route('', methods=['GET'])
def get_all_menus():
    menus = Menu.query.all()

    result = [item.to_dict() for item in menus]

    return jsonify(result), 200

@menu_bp.route('', methods=['POST'])
def create_one_menu():
    request_body = request.get_json()

    new_menu = Menu(restaurant_name = request_body.get("restaurant_name"), meal = request_body.get("meal"))

    db.session.add(new_menu)
    db.session.commit()

    return jsonify({"msg":f"Successfully created Menu with id={new_menu.id}"}), 201

@menu_bp.route('/<menu_id>/breakfasts', methods=['GET'])
def get_breakfasts_for_menu(menu_id):
    menu = get_model_from_id(Menu, menu_id)

    breakfasts = menu.get_breakfast_list()
    
    return jsonify(breakfasts), 200