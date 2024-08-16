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
