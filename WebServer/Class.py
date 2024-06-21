from flask                import Flask, redirect, request, url_for
from flask_login          import LoginManager , current_user
from flask_htmlmin        import HTMLMIN
from Global.Constant      import WEBSERVER_DEBUG , WEBSERVER_FLASK_DEBUG , WEBSERVER_LOG , WEBSERVER_SECRET_KEY , WEBSERVER_MINIFY_HTML , WEBSERVER_TIDYFY_HTML , WEBSERVER_MAX_CONTENT_LENGTH
from Global.Constant      import NAME , ENCODE , LANGUAGE
from Global.Decorator     import Do_Log
from Global.Class.Logger  import Logger
from Global.Class.Network import IPv4 , Port
from SQLManager           import SQLManager

class FlaskWebServer :
    def __init__(self , Host : IPv4 , Port : Port) -> None:
        self.Logger = Logger('Web Server' , WEBSERVER_LOG , WEBSERVER_DEBUG)
        self.Host = Host
        self.Port = Port

        self.App  = Flask(__name__ , static_folder = "Static" , template_folder = "Templates")
        Login_Manager = LoginManager()
        Login_Manager.init_app(self.App)
        self.App.config['MINIFY_HTML']        = WEBSERVER_MINIFY_HTML
        self.App.config['SECRET_KEY']         = WEBSERVER_SECRET_KEY
        self.App.config['MAX_CONTENT_LENGTH'] = WEBSERVER_MAX_CONTENT_LENGTH

        if self.App.config['MINIFY_HTML'] : self.HTMLmin = HTMLMIN(self.App)
    
    @Do_Log('Registering Blueprints...','Done!')
    def Init_Blueprints(self , Blueprints : list) -> None :
        if self.Valid :
            for Item in Blueprints :
                self.Logger(f'Registering : {Item.__Prefix__}')
                try    : self.App.register_blueprint(Item , url_prefix = Item.__Prefix__)
                except Exception as e : self.Logger(f'Unable to Register {Item} : {e}')

    @Do_Log('Initiating Flask Main Loop...')
    def Start(self) -> None :
        self.App.run(host=self.Host.IPv4, port=self.Port.Number, debug=WEBSERVER_FLASK_DEBUG)

    @Do_Log('Stoping...','Stopped!')
    def Stop(self) -> None :
        pass

    def __str__(self) -> str:
        return f'< FlaskApp {self.App.name} >'

    def __bool__(self) -> bool :
        return self.Valid