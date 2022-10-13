import imp
from flask import abort
from flask_login import current_user

def check_permissions(allowed_roles=None, banned_roles=None, allowed_user=None ):
    # Check whether role has access
    if allowed_roles and current_user.role not in allowed_roles:
        abort(403)
    
    # Check whether role has access
    if banned_roles and current_user.role in banned_roles:
        abort(403)
    
    # Check if current user is allowed (admin can access anything meant for is role)
    if allowed_user and current_user != allowed_user and current_user.role != 'admin':
        abort(403)


def has_permissions(allowed_roles=None,  banned_roles=None, allowed_user=None):
    # Check whether role has access
    if allowed_roles and current_user.role not in allowed_roles:
        return False

    # Check whether role has access
    if banned_roles and current_user.role in banned_roles:
        return False

    # Check if current user is allowed (admin can access anything meant for is role)
    if allowed_user and current_user != allowed_user and current_user.role != 'admin':
        return False

    return True
    
 