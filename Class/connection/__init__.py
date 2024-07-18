class Connection :
    def __init__(self,*,
        Host:str,
        Port:int,
        Username:str,
        Password:str,
        ) -> None :

        self.Host = Host
        self.Port = Port
        self.Username = Username
        self.Password = Password

    def Connect(self) -> None :
        raise NotImplementedError('Please provide an action for connecting with this method')

    def Receive(self) -> str :
        raise NotImplementedError('Please provide an action for getting data')

    def Send(self, Message:str, Wait:float = 0.2) -> str:
        raise NotImplementedError('Please provide an action for sending data')

    def Disconnect(self) -> None :
        raise NotImplementedError('Please provide an action for disconnecting')

    def Is_Connected(self) -> bool:
        raise NotImplementedError('Please provide an action for getting connection status')

    def __bool__(self) -> bool :
        return self.Is_Connected()

    def __enter__(self) -> None :
        self.Connect()

    def __exit__(self,Eexception_Type, Exception_Value, Traceback) -> None :
        self.Disconnect()

    def __str__(self) -> str :
        return f'<Connection :{self.__class__.__name__}>'

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(Host={self.Host},Port={self.Port})'