from flask import Flask
from flask_login import LoginManager, current_user
from flask_htmlmin import HTMLMIN

from .sqlmanager import SQLManager
from ._base import Component

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
    def __init__(self,App:Flask,*,
        Host:str,
        Port:int,
        Flask_Debug:bool=False,
        Secret_Key:str,
        SQLManager:SQLManager,
        Blueprints:list,
        ) -> None:

        self.App = App
        self.Host = Host
        self.Port = Port
        self.Flask_Debug = Flask_Debug
        self.Secret_Key = Secret_Key
        self.SQLManager = SQLManager
        self.Blueprints = Blueprints
        self.Init_App()
        self.Register_Blueprints()

    def Start_Actions(self) -> None:
        self.App.run(self.Host, self.Port, debug=self.Flask_Debug)

    def Stop_Actions(self) -> None:
        pass

    def Init_App(self) -> None:
        ## Configs
        self.App.config['SECRET_KEY'] = self.Secret_Key
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