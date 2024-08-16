from flask import Flask
from flask_login import LoginManager
from flask_htmlmin import HTMLMIN

from blueprints import Blueprints

App = Flask(__name__, static_folder="static", template_folder="templates")
Login_Manager = LoginManager()

## Configs
App.config['SECRET_KEY'] = "SDy9r3gbFDBjq0urv1398t0gsbuq0"

## Add-ins
HTMLMIN(App)
Login_Manager.init_app(App)

## Adding Functions
@Login_Manager.user_loader
def UserLoader(ID:int) -> Exception:
    raise NotImplementedError('No DB Management implemented')

## Registering blueprints
for Blueprint in Blueprints:
    App.register_blueprint(Blueprint)

if __name__ == '__main__' :
    App.run('0.0.0.0', 8080, debug=True)
