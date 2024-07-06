if __name__ == '__main__' :
    from Global import Main_Logger,Main_Config
    
    Main_Logger('Configs and Logging system Loaded')
    Main_Logger('App Works Fine')
    Main_Logger(Main_Config.__dict__)