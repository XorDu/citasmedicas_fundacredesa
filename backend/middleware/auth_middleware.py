from functools import wraps
from flask import abort
from flask_login import current_user
from backend.models.permission import Permission

def require_role(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return abort(401)
            if current_user.role != role and current_user.role != 'superadmin':
                return abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def require_permission(permission_type):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return abort(401)
            
            # Superadmin bypass
            if current_user.role == 'superadmin':
                return f(*args, **kwargs)
                
            # If specialty user, check permissions
            if current_user.role == 'specialty' and current_user.specialty_id:
                perm = Permission.query.filter_by(specialty_id=current_user.specialty_id).first()
                if perm and getattr(perm, f'can_{permission_type}', False):
                    return f(*args, **kwargs)
                    
            return abort(403)
        return decorated_function
    return decorator
