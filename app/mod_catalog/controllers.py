# Import flask dependencies
from flask import Blueprint, request, render_template, \
    flash, g, session, redirect, url_for, abort
from sqlalchemy import and_
from app import app
from app import db_session
from app import login_manager
from flask_login import login_required, login_user, logout_user, current_user
from app.mod_auth.models import User
from app.mod_catalog.models import Item, Category

from functools import wraps
mod_catalog = Blueprint('catalog', __name__, url_prefix='/catalog')


def render_new_item_page(title="", description="", category_id=None):
    categories = db_session.query(Category).all()
    # category_id used when editing not creating new item
    if category_id is not None:
        category_id = int(category_id)
    return render_template('new_edit_item.html.j2', page_heading='Create Item',
                           categories=categories,
                           title=title, description=description,
                           category_id=category_id)


@mod_catalog.route('/')
def home():
    # Show list of categories and a list of the latest items
    categories = db_session.query(Category).all()
    top_items = db_session.query(Item).order_by(
        Item.created_at.desc()).limit(10).all()
    return render_template('home.html.j2', categories=categories, top_items=top_items)


@mod_catalog.route('/<category_name>')
@mod_catalog.route('/<category_name>/items')
def items_by_category(category_name):
    category = Category.by_name(category_name)
    if not category:
        return "Error, no category found", 404
    items = Item.by_category(category)
    return render_template("category_items.html.j2", category_name=category.name, items=items)


@mod_catalog.route('/<category_name>/<item_title>')
def get_item(category_name, item_title):
    category = Category.by_name(category_name)
    if not category:
        return "Error, no category found", 404
    item = db_session.query(Item).filter(
        and_(Item.title == item_title, Item.category == category)).first()
    if not item:
        return "Error, no item found", 404

    return render_template('item_view.html.j2', item=item)


@mod_catalog.route('/items/new', methods=['GET', 'POST'])
@login_required
def new_item():
    if request.method == 'GET':
        return render_new_item_page()

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        category_id = request.form['category_id_inp']

        if not title or not description or not category_id:
            flash("Missing input")
            return render_new_item_page(title, description, category_id)

        category = Category.by_id(category_id)

        if Item.by_title(title):
            flash("Item with title \"%s\" already exists." % title)
            return render_new_item_page(title, description, category_id)

        item = Item(title=title, description=description,
                    category_id=category_id, creator_id=current_user.id)
        db_session.add(item)
        db_session.commit()
        return redirect(url_for('catalog.get_item',
                                category_name=item.category.name,
                                item_title=item.title))


@mod_catalog.route('/<item_title>/edit', methods=['GET', 'POST'])
@login_required
def edit_item(item_title):
    item = Item.by_title(item_title)
    if not item:
        return "Error, no item found", 404
    if current_user != item.user:
        return "You do not own this item", 403

    if request.method == 'GET':
        return render_new_item_page(item.title, item.description, item.category_id)
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        category_id = request.form['category_id_inp']
        if not title or not description or not category_id:
            flash("Missing input")
            return render_new_item_page(title, description, category_id)
        item.title = title
        item.description = description
        itme.category_id = category_id
        db_session.add(item)
        db_session.commit()
        return redirect(url_for('catalog.get_item',
                                category_name=item.category.name,
                                item_title=item.title))


def item_exists(func):
    @wraps(func)
    def wrapper(item, *args, **kwargs):
        if not item:
            abort(404)
        else:
            return func(item, *args, **kwargs)
    return wrapper


@item_exists
def check_item_creator(item):
    if current_user != item.user:
        abort(403)


@mod_catalog.route('/<item_title>/delete', methods=['GET', 'POST'])
@login_required
def delete_item(item_title):
    item = Item.by_title(item_title)
    check_item_creator(item)
    if request.method == 'GET':
        return render_template('delete_item.html.j2')
    if request.method == 'POST':
        db_session.delete(item)
        db_session.commit()
        flash("%s successfully deleted" % item_title)
        return redirect(url_for('catalog.home'))
