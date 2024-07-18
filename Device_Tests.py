from Class.device.mikrotik import Mikrotik
from Class.connection.ssh import SSH

if __name__ == '__main__' :

    MyDevice = Mikrotik('Test Device',Host='192.168.1.56',Port=22,Username='admin',Password='admin')
    MyDevice.Connect(via=SSH)

    with MyDevice.Connection :
        Hostname = MyDevice.Get_Hostname()
        Configs = MyDevice.Get_Export()

    with open('config.txt','w') as f :
        f.write(Configs)