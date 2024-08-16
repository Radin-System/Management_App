from flask       import redirect,url_for,abort,flash
from functools   import wraps
from flask_login import current_user

def login_required(Func):
    @wraps(Func)
    def Decorate(*args, **kwargs):
        if not current_user.is_authenticated :
            flash({'Content':'برای ورود به این بخش ؛ وارد حساب کاربری خود شوید !'}, 'warning')
            return redirect(url_for('Auth.Login'))
        return Func(*args, **kwargs)
    return Decorate

def register_required(Func):
    @wraps(Func)
    def Decorate(*args, **kwargs):
        if not (current_user.is_authenticated and current_user.registerd):
            return redirect(url_for('Auth.Register'))
        return Func(*args, **kwargs)
    return Decorate

def admin_required(Func):
    @wraps(Func)
    def Decorate(*args, **kwargs):
        if not (current_user.is_authenticated and current_user.admin) :
            return abort(401) ,401
        return Func(*args, **kwargs)
    return Decorate

def agent_required(Func):
    @wraps(Func)
    def Decorate(*args, **kwargs):
        if not (current_user.is_authenticated and current_user.agent) :
            return abort(401) ,401
        return Func(*args, **kwargs)
    return Decorate

def operator_required(Func):
    @wraps(Func)
    def Decorate(*args, **kwargs):
        if not (current_user.is_authenticated and current_user.operator) :
            return abort(401) ,401
        return Func(*args, **kwargs)
    return Decorate
