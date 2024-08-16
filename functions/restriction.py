from flask       import redirect,url_for,abort
from functools   import wraps
from flask_login import current_user

def login_required(Func):
    @wraps(Func)
    def Decorate(*args, **kwargs):
        if not current_user.is_authenticated :
            return redirect(url_for('Auth.Login'))
        return Func(*args, **kwargs)
    return Decorate

def admin_required(Func):
    @wraps(Func)
    def Decorate(*args, **kwargs):
        if not (current_user.is_authenticated and current_user.admin) :
            return abort(401) ,401
        return Func(*args, **kwargs)
    return Decorate
