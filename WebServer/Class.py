import tidylib as _
from flask                import Flask, redirect, request, url_for
from flask_login          import LoginManager , current_user
from flask_htmlmin        import HTMLMIN
from Global.Constant      import WEBSERVER_DEBUG , WEBSERVER_FLASK_DEBUG , WEBSERVER_LOG , WEBSERVER_TLS_MODE , WEBSERVER_SECRET_KEY , WEBSERVER_MINIFY_HTML , WEBSERVER_TIDYFY_HTML , WEBSERVER_MAX_CONTENT_LENGTH
from Global.Constant      import NAME , ENCODE , LANGUAGE
from Global.Decorator     import Do_Log
from Global.Class.Logger  import Logger
from Global.Class.Network import IPv4 , Port
from SQLManager           import SQLManager

class PageSetting :
    class DefaultBaseSetting :
        def __init__(self , Title) -> None:
            self.Dir       = 'rtl' if LANGUAGE == 'fa' else 'ltr'
            self.Charset   = ENCODE.upper()
            self.Appname   = NAME
            self.Language  = LANGUAGE
            self.PageTitle = Title

    class DefaultStaticFile :
        def __init__(self) -> None:
            self.Main         = True
            self.JQuery       = True
            self.Bootstrap    = True
            self.FontAwesome  = True
            self.FontVazirmtn = True

    def __init__(self , Title : str = NAME , Mode : str = 'Full') -> None:
        self.Mode = Mode
        self.BaseSetting = PageSetting.DefaultBaseSetting(Title)
        self.StaticFile  = PageSetting.DefaultStaticFile()

class BreadCrumb :
    def __init__(self , Icon : str = 'fas fa-home') -> None:
        self.Icon = Icon
        pass

class FlaskWebServer :
    def __init__(self , Host : IPv4 , Port : Port) -> None:
        self.Logger = Logger('Web Server' , WEBSERVER_LOG , WEBSERVER_DEBUG)
        
        self.Host = Host
        self.Port = Port
        self.Valid = self.Validate()
        if self.Valid :
            self.App  = Flask(__name__ , static_folder = "Static" , template_folder = "Templates")
            Login_Manager = LoginManager()
            Login_Manager.init_app(self.App)
            self.App.config['MINIFY_HTML']        = WEBSERVER_MINIFY_HTML
            self.App.config['TIDYFY_HTML']        = WEBSERVER_TIDYFY_HTML
            self.App.config['SECRET_KEY']         = WEBSERVER_SECRET_KEY
            self.App.config['TLS_Mode']           = WEBSERVER_TLS_MODE
            self.App.config['MAX_CONTENT_LENGTH'] = WEBSERVER_MAX_CONTENT_LENGTH
            if WEBSERVER_MINIFY_HTML : self.HTMLmin = HTMLMIN(self.App)

            @Login_Manager.user_loader
            def UserLoader(ID:int) -> None: return SQLManager.Query(SQLManager.User , Eager = True , First = True , id = ID)
            
            @self.App.context_processor
            def ContextProcessor() -> None: return dict(current_user=current_user , PageSetting=PageSetting())

    def Validate(self) -> None:
        return bool(self.Host and self.Port)
    
    @Do_Log('Registering Blueprints...','Done!')
    def Init_Blueprints(self , Blueprints : list) -> None :
        if self.Valid :
            for Item in Blueprints :
                self.Logger(f'Registering : {Item.__Prefix__}')
                try    : self.App.register_blueprint(Item , url_prefix = Item.__Prefix__)
                except Exception as e : self.Logger(f'Unable to Register {Item} : {e}')

    @Do_Log('Wraping TLS...')
    def WrapTLS(self) -> tuple:
        self.Logger('TLS not implemented !')
        return None

    @Do_Log('Initiating Flask Main Loop...')
    def Start(self) -> None :
        if WEBSERVER_TLS_MODE : self.App.run(host=self.Host.IPv4,port=self.Port.Number,ssl_context=self.WrapTLS(),debug=WEBSERVER_FLASK_DEBUG)
        else                  : self.App.run(host=self.Host.IPv4,port=self.Port.Number                           ,debug=WEBSERVER_FLASK_DEBUG)

    @Do_Log('Stoping...','Stopped!')
    def Stop(self) -> None :
        pass

    def __str__(self) -> str:
        return f'< FlaskApp {self.App.name} >'

    def __bool__(self) -> bool :
        return self.Valid