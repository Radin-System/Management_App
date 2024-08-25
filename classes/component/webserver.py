from flask import Flask
from flask_login import LoginManager, current_user
from flask_htmlmin import HTMLMIN
from .logger import Logger
from .sqlmanager import SQLManager
from ._base import Service, ServiceContainer

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

class WebServer(Service):
    def __init__(self,Name:str,*,
        App:Flask,
        Blueprints:list,
        ) -> None:
        super().__init__(Name)

        self.App = App
        self.Blueprints = Blueprints

        self.Init_App()
        self.Register_Blueprints()

    def Init_Dependancy(self) -> None:
        super().Init_Dependancy()
        self.SQLManager = ServiceContainer.Get('MainSQLManager')

    def Init_Config(self) -> None:
        self.Host = self.Config.Get('WEBSERVER','host')
        self.Port = self.Config.Get('WEBSERVER','port')
        self.Flask_Debug = self.Config.Get('WEBSERVER','flask_debug')
        self.Secret_Key = self.Config.Get('WEBSERVER','secret_key')

    def Start_Actions(self) -> None:
        self.Logger('Starting Flask Web Server', level='info')
        self.App.run(self.Host, self.Port, debug=self.Flask_Debug)

    def Stop_Actions(self) -> None:
        self.Logger('Stopping Flask Web Server', level='info')

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
        for Blueprint in self.Blueprints:
            self.App.register_blueprint(Blueprint(self.SQLManager))