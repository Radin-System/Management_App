from flask import Flask,Blueprint
from flask_login import LoginManager, current_user
from flask_htmlmin import HTMLMIN

from classes.tool import ToolContainer

from ._base import Component
from ._container import ComponentContainer
from .sqlmanager import SQLManager

class WebServer(Component):
    def __init__(self,Name:str,*,
        App:Flask,
        Blueprints:list[Blueprint],
        ) -> None:
        super().__init__(Name)

        self.App = App
        self.Blueprints = Blueprints

        self.Process_Type: str = 'Static'

    def Init_WebApp(self) -> None:
        ## Configs
        self.App.config['SECRET_KEY'] = self.Secret_Key

        # Replace Flask's default logger with your custom logger
        self.App.logger.handlers = self.Logger.logger.handlers
        self.App.logger.setLevel(self.Logger.logger.level)

        ## Add-ins
        Login_Manager = LoginManager()
        HTMLMIN(self.App)
        Login_Manager.init_app(self.App)

        ## Registering Blueprints
        self.Logger('Registering Blueprints', 'debug')
        for BP_Function in self.Blueprints:
            Bp:Blueprint = BP_Function(ComponentContainer, ToolContainer)
            self.Logger(f'- Blueprint: {Bp} prefix:{Bp.url_prefix}', 'debug')
            try:
                self.App.register_blueprint(Bp)

            except ValueError as e:
                if 'is already registered' in str(e):
                    self.Logger(f'- Blueprint: {Bp} prefix:{Bp.url_prefix} Already registered', 'debug')
                else:
                    raise e

            except Exception as e:
                self.Logger(f'{type(e).__name__}: {e}')
                raise e

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
            return dict(Current_User=current_user, PageSetting=self.Config.Parser['WEBPAGESETTINGS'])

    def Init_Dependancy(self) -> None:
        super().Init_Dependancy()
        self.SQLManager:SQLManager = ComponentContainer.Get('Main_SQLManager')

    def Init_Config(self) -> None:
        self.Host = self.Config.Get('WEBSERVER', 'host')
        self.Port = self.Config.Get('WEBSERVER', 'port')
        self.Secret_Key = self.Config.Get('WEBSERVER','secret_key')

    def Loop(self) -> None:
        self.App.run(self.Host, self.Port)
        self.Stop()

    def Start_Actions(self) -> None:
        self.Logger('Starting Flask Web Server')
        self.Init_WebApp()

    def Stop_Actions(self) -> None:
        self.Logger('Stopping Flask Web Server')