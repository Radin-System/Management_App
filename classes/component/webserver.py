from flask import Flask
from flask_login import LoginManager
from flask_htmlmin import HTMLMIN

from .sqlmanager import SQLManager
from .base import Component

class WebServer(Component):
    def __init__(self,*,
        Host:str,
        Port:int,
        Flask_Debug:bool=False,
        Secret_Key:str,
        SQLManager:SQLManager,
        Blueprints:list,
        ) -> None:

        self.Host = Host
        self.Port = Port
        self.Flask_Debug = Flask_Debug
        self.Secret_Key = Secret_Key
        self.SQLManager = SQLManager
        self.Blueprints = Blueprints

    def Start_Actions(self) -> None:
        self.Init_App()
        self.Register_Blueprints()
        self.App.run(self.Host, self.Port, debug=self.Flask_Debug)

    def Stop_Actions(self) -> None:
        pass

    def Init_App(self) -> None:
        
        ## Initing Apps
        self.App = Flask(__name__, static_folder="static", template_folder="templates")

        ## Configs
        self.App.config['SECRET_KEY'] = self.Secret_Key
        Login_Manager = LoginManager()

        ## Add-ins
        HTMLMIN(self.App)
        Login_Manager.init_app(self.App)

        ## Adding Functions
        @Login_Manager.user_loader
        def User_Loader(ID:int) -> Exception:
            raise NotImplementedError('No DB Management implemented')

    def Register_Blueprints(self) -> None:
        for Blueprint in self.Blueprints:
            self.App.register_blueprint(Blueprint)