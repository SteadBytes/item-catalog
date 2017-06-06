from functools import wraps
from flask import abort
from flask import render_template
from app import db_session
from app import login_manager
from flask_login import login_required, login_user, logout_user, current_user


def item_exists(func):
    """Wrapper for checking an item query.

    Database query will return None if the item isn't found. Wrapper will give
    a 404 error if it is none. Else it returns the wrapped function.
    The wrapped function must have the item as a parameter.
    """
    @wraps(func)
    def wrapper(item, *args, **kwargs):
        if not item:
            abort(404)
        else:
            return func(item, *args, **kwargs)
    return wrapper


@item_exists
def check_item_creator(item):
    """ Checks if given item is owned by the current user

    Used for authorization when editing/deleting items

    Args:
        item: Result of a DB query for an item -> Item Object or None
    """
    if current_user != item.user:
        abort(403)


def render_new_item_page(title="", description="", category_id=None):
    """Renders page for creating and editing items.

    Editing and creating both use the same template 'new_edit_item.html.j2'
    When editing the form is just pre-filled with current data as apposed to
    being empty when creating a new item.
    The category_id is only used when editing an existing item.
    """
    # category_id used when editing not creating new item
    if category_id is not None:
        category_id = int(category_id)
    return render_template('new_edit_item.html.j2', page_heading='Create Item',
                           title=title, description=description,
                           category_id=category_id)
