if __name__ == '__main__' :
    CONFIGFILE = '.configfiles/config.ini'

    from Class.config import Config
    from Class.component.sqlmanager import SQLManager
    from Model   import Base,Models


    Main_Config = Config(
        Config_File = CONFIGFILE,
        )

    sql = SQLManager(
        Host        = Main_Config.Get('SQLMANAGER','host'),
        Port        = Main_Config.Get('SQLMANAGER','port'),
        Username    = Main_Config.Get('SQLMANAGER','username'),
        Password    = Main_Config.Get('SQLMANAGER','password'),
        DataBase    = Main_Config.Get('SQLMANAGER','database'),
        Mode        = Main_Config.Get('SQLMANAGER','mode'),
        SQLite_Path = Main_Config.Get('SQLMANAGER','sqlite_path'),
        Verbose     = Main_Config.Get('SQLMANAGER','verbose'),
        Base        = Base ,
        Models      = Models ,
        )
    
    with sql :
        ## Testing Users
        Admin = sql.User(username='admin',password='asd@123',en_firstname='Administrator',en_lastname=' ',fa_firstname=' ',fa_lastname=' ',admin=True)
        New_User = sql.User(username='m.heydari',password='asd@123',en_firstname='Mohammad',en_lastname='Heydari',fa_firstname='محمد',fa_lastname='حیدری')
        ## Testing Company 
        Radin = sql.Company(en_name='Radin System',fa_name='رادین سیستم',domain='rsto.ir',owner=Admin)
        Amanfilter = sql.Company(en_name='AmanFilter',fa_name='امان پالایش ایرانیان',domain='AmanFilter.ir',owner=Admin)
        ## Testing Location
        Office = sql.Location(type='Office',en_name='Headquarter',fa_name='دفتر مرکزی',company=Amanfilter,owner=Admin)
        ## Testing auth
        Radius = sql.Authentication(type='radius',username='admin',password='asd@123',enable='dsa@321',owner=Admin)
        ## Testing Device
        Device = sql.Device(hostname='SW-Core',fqdn='SW-Core.office.amanfilter.ir',type='Cisco',management_address='192.168.1.1',connection_method='SSH',connection_port=22,company=Amanfilter,location=Office,authentication=Radius,owner=Admin)
        ## Testing Node
        Node = sql.Node(hostname='QC-F1',fqdn='QC-F1.Amanfilter.ir',company=Amanfilter,location=Office,owner=Admin)
        ## Testing Personnel
        Person = sql.Personnel(username='Soraya.khodaei',agent=True,en_firstname='soraya',en_lastname='khodayi', fa_firstname='صریا',fa_lastname='خدایی',email='H.N54678@gmail.com',extension=800,mobile_number='09112345678',company=Amanfilter,location=Office,owner=Admin)

        Records = [Admin,New_User,Radin,Amanfilter,Office,Radius,Device,Node,Person]
        for Record in Records :
            sql.Create(Record)