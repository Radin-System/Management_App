from Class.device.mikrotik import Mikrotik
from Class.device.cisco import Cisco
from Class.connection.ssh import SSH

if __name__ == '__main__' :

    MyDevice = Mikrotik()
    MyDevice.Connect(via=SSH,Host='192.168.1.56',Port=22,Username='admin',Password='admin')

    with MyDevice.Connection :
        Hostname = MyDevice.Get_Hostname()
        #Configs = MyDevice.Get_Export()
        Result = MyDevice.Get_Interfaces()
        for K,V in Result.items():
            for i in V :
                print (i.name)
