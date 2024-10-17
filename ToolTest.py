CONFIGFILE = '.configfiles/config.ini'

if __name__ == '__main__' :
    from classes.component import *

    from classes.tool import *

    Main_Config = Config('MainConfig', Config_File=CONFIGFILE)
    Main_Logger = Logger('MainLogger')

    nc = NetboxClient(
        Main_Config.Get('TOOL', 'netbox_url'),
        Main_Config.Get('TOOL', 'netbox_token'),
        )

    zb = ZabbixClient(
        Main_Config.Get('TOOL', 'zabbix_url'),
        Main_Config.Get('TOOL', 'zabbix_token'),
    )

    Data = nc.core.data_sourcess.get(id=4)
    print(Data)
    