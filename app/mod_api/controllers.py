from app import app
import json
from flask import Flask, jsonify, Blueprint
from app import db_session
from app.mod_catalog.models import Item, Category

# JSON API endpoint for Catalog application

mod_api = Blueprint('api', __name__, url_prefix='/api')


@mod_api.route('/categories')
def get_categories():
    """Returns list of all categories and their information.
    """
    categories = db_session.query(Category).all()
    if categories:
        return jsonify(Categories=[i.serialize for i in categories])
    else:
        return jsonify({"Error": "No categories found"}), 404


@mod_api.route('/items')
def get_items():
    """Returns list of all items and their information.
    """
    items = db_session.query(Item).all()
    if items:
        return jsonify(Items=[i.serialize for i in items])
    else:
        return jsonify({"Error": "No items found"}), 404


@mod_api.route('/catalog')
def get_catalog():
    """Returns list of all items and their information,broken down by category.
    """
    categories = db_session.query(Category).all()
    result = {}
    for category in categories:
        items = db_session.query(Item).filter_by(category=category).all()
        result[category.name] = [i.serialize for i in items]
    return jsonify(result)
