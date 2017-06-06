from flask import Blueprint, request, render_template, \
    flash, g, session, redirect, url_for, abort
from sqlalchemy import and_
from app import app
from app import db_session
from app import login_manager
from flask_login import login_required, current_user
from app.mod_auth.models import User
from app.mod_catalog.models import Item, Category
from app.mod_catalog.helpers import render_new_item_page, check_item_creator


mod_catalog = Blueprint('catalog', __name__, url_prefix='/catalog')


@mod_catalog.route('/')
def home():
    """Show list of categories and a list of the latest items
    """
    top_items = db_session.query(Item).order_by(
        Item.created_at.desc()).limit(10).all()
    return render_template('home.html.j2', top_items=top_items)


@mod_catalog.route('/<category_name>')
@mod_catalog.route('/<category_name>/items')
def items_by_category(category_name):
    """Retrieves all items in a specific category

    Args:
        category_name: String, name of category
    """
    category = Category.by_name(category_name)
    if not category:
        return "Error, no category found", 404
    items = Item.by_category(category)
    return render_template("category_items.html.j2",
                            category_name=category.name, items=items)


@mod_catalog.route('/<category_name>/<item_title>')
def get_item(category_name, item_title):
    """Retrieves a specific individual item

    Checks item exists with given category. Pass item to template, returns view
    Args:
        category_name: String, name of category
        item_title: String, title of item
    """
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
    """Handles creating new catalog item

    GET request returns form for creating item.
    POST request takes data from form and creates a new Item in database with
    given data.
    """
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
        """Handles editing catalog item

        GET returns form for editing given item (pre-filled with current data)
        POST request takes data from form and a updates Item in database with
        given data.

        Args:
            item_title: String, title of item to edit
        """
    # Check item exists and current user is authorized to edit it
    item = Item.by_title(item_title)
    check_item_creator(item) # 403 error if current user != item creator

    if request.method == 'GET':
        return render_new_item_page(item.title, item.description,
                                    item.category_id)
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


@mod_catalog.route('/<item_title>/delete', methods=['GET', 'POST'])
@login_required
def delete_item(item_title):
    """Handles deleting catalog item

    GET returns confirmation page for deleting item.
    POST request removes item from database, then redirect to homepage.

    Args:
        item_title: String, title of item to delete
    """
    item = Item.by_title(item_title)
    check_item_creator(item)
    if request.method == 'GET':
        return render_template('delete_item.html.j2', item=item)
    if request.method == 'POST':
        db_session.delete(item)
        db_session.commit()
        flash("%s successfully deleted" % item_title)
        return redirect(url_for('catalog.home'))
