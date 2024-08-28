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
        App:Flask,
        Blueprints:list[Blueprint],
        ) -> None:
        super().__init__(Name)

        self.App = App
        self.Blueprints = Blueprints

        self.Process_Type: str = 'Static'

        ## Configs
        self.App.config['SECRET_KEY'] = self.Secret_Key

        # Replace Flask's default logger with your custom logger
        self.App.logger.handlers = self.Logger.logger.handlers
        self.App.logger.setLevel(self.Logger.logger.level)

        Login_Manager = LoginManager()

        ## Add-ins
        HTMLMIN(self.App)
        Login_Manager.init_app(self.App)

        ## Registering Blueprints
        self.Logger('Registering Blueprints', 'debug')
        for Blueprint in self.Blueprints:
            Blueprint = Blueprint(self.SQLManager)
            self.Logger(f'- Blueprint: {Blueprint} prefix:{Blueprint.url_prefix}', 'debug')
            self.App.register_blueprint(Blueprint)

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

    def Init_Dependancy(self) -> None:
        super().Init_Dependancy()
        self.SQLManager:SQLManager = ComponentContainer.Get('MainSQLManager')

    def Init_Config(self) -> None:
        self.Host = self.Config.Get('WEBSERVER','host')
        self.Port = self.Config.Get('WEBSERVER','port')
        self.Secret_Key = self.Config.Get('WEBSERVER','secret_key')

    def Loop(self) -> None:
        self.App.run(self.Host, self.Port)
        self.Stop()

    def Start_Actions(self) -> None:
        self.Logger('Starting Flask Web Server')

    def Stop_Actions(self) -> None:
        self.Logger('Stopping Flask Web Server')