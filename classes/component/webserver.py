import os
from flask import Flask,Blueprint
from flask_login import LoginManager, current_user
from flask_htmlmin import HTMLMIN
from .sqlmanager import SQLManager
from ._base import *

class PageSetting :
    class DefaultBaseSetting :
        def __init__(self) -> None:
            self.Dir       = 'rtl'
            self.Charset   = 'UTF-8'
            self.Appname   = 'support_portal'
            self.Language  = 'fa'
            self.PageTitleEn = 'Support Portal'
            self.PageTitleFa = 'پرتال پشتیبانی'

    class DefaultStaticFile :
        def __init__(self) -> None:
            self.Main         = True
            self.JQuery       = True
            self.Bootstrap    = True
            self.FontAwesome  = True
            self.FontVazirmtn = True

    def __init__(self) -> None:
        self.BaseSetting = PageSetting.DefaultBaseSetting()
        self.StaticFile  = PageSetting.DefaultStaticFile()

class WebServer(Component):
    def __init__(self,Name:str,*,
        Blueprints:list[Blueprint],
        ) -> None:
        super().__init__(Name)

        self.Blueprints = Blueprints

        self.Process_Type: str = 'Process'

    def Init_Dependancy(self) -> None:
        super().Init_Dependancy()
        self.SQLManager:SQLManager = ComponentContainer.Get('MainSQLManager')

    def Init_Config(self) -> None:
        self.Host = self.Config.Get('WEBSERVER','host')
        self.Port = self.Config.Get('WEBSERVER','port')
        self.Secret_Key = self.Config.Get('WEBSERVER','secret_key')

    def Loop(self) -> None:
        self.App.run(self.Host, self.Port)

    def Start_Actions(self) -> None:
        # Define absolute paths
        base_dir = os.path.dirname(os.path.abspath(__file__))
        static_path = os.path.join(base_dir, 'static')
        templates_path = os.path.join(base_dir, 'templates')
        self.Logger(f'Flask Static Path:{static_path}')
        self.Logger(f'Flask Template Path:{templates_path}')
        # Create the Flask App
        self.App = Flask(__name__, static_folder=static_path, template_folder=templates_path)
        self.Init_App()
        self.Register_Blueprints()
        self.Logger('Starting Flask Web Server')

    def Stop_Actions(self) -> None:
        self.Logger('Stopping Flask Web Server')

    def Init_App(self) -> None:
        ## Configs
        self.App.config['SECRET_KEY'] = self.Secret_Key

        # Replace Flask's default logger with your custom logger
        self.App.logger.handlers = self.Logger.logger.handlers
        self.App.logger.setLevel(self.Logger.logger.level)

        Login_Manager = LoginManager()

        ## Add-ins
        HTMLMIN(self.App)
        Login_Manager.init_app(self.App)

        ## Adding Functions
        @Login_Manager.user_loader
        def User_Loader(ID:int):
            return self.SQLManager.Query(self.SQLManager.User, 
                Detached=True,
                Eager = True,
                First = True,
                id = ID
                )

        @self.App.context_processor
        def Context_Processor() -> dict:
            return dict(Current_User=current_user, PageSetting=PageSetting())

    def Register_Blueprints(self) -> None:
        self.Logger('Registering Blueprints', 'debug')
        for Blueprint in self.Blueprints:
            Blueprint = Blueprint(self.SQLManager)
            self.Logger(f'- Blueprint: {Blueprint} prefix:{Blueprint.url_prefix}', 'debug')
            self.App.register_blueprint(Blueprint)