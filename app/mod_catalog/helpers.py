from functools import wraps
from flask import abort
from flask import render_template
from app import db_session
from app import login_manager
from flask_login import login_required, login_user, logout_user, current_user


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


def render_new_item_page(title="", description="", category_id=None):
    # category_id used when editing not creating new item
    if category_id is not None:
        category_id = int(category_id)
    return render_template('new_edit_item.html.j2', page_heading='Create Item',
                           title=title, description=description,
                           category_id=category_id)
