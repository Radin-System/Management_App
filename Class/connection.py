import os, time, socket, struct, select, paramiko
from typing import Self
from Function.decorator import Connection_Required

ICMP_ECHO_REQUEST = 8

class Connection :

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

    def __enter__(self) -> Self :
        self.Connect()
        return self

    def __exit__(self,Eexception_Type, Exception_Value, Traceback) -> None :
        self.Disconnect()

    def __str__(self) -> str :
        return f'<Connection :{self.__class__.__name__}>'

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(*args,**Kwargs)'

class ICMP(Connection):
    def __init__(self, *, Host: str) -> None:
        self.Host = Host
        self.Client = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.getprotobyname("icmp"))

    def Connect(self) -> None:
        self.Client.connect((self.Host))

    @Connection_Required
    def Receive(self) -> str:
        raise NotImplemented('ICMP Request does not support Reciving')

    @Connection_Required
    def Send(self, Count: int = 4, Size: int = 36) -> list:
        self.Connect()
        Delays = []
        for _ in range(Count):
            Delay = self._do_one_ping(Size)
            if Delay is not None : Delays.append(Delay)
            time.sleep(0.5)
        return Delays

    @Connection_Required
    def Disconnect(self) -> None:
        self.Client.close()

    def Is_Connected(self) -> bool:
        try:
            self.Client.recv(16, socket.MSG_DONTWAIT | socket.MSG_PEEK)
        except BlockingIOError:return True
        except ConnectionResetError:return False
        return True

    def _checksum(self, source_string):
        """
        A function to calculate the checksum of our packet.
        """
        sum = 0
        count_to = (len(source_string) // 2) * 2
        count = 0

        while count < count_to:
            this_val = (source_string[count + 1]) * 256 + (source_string[count])
            sum = sum + this_val
            sum = sum & 0xffffffff
            count = count + 2

        if count_to < len(source_string):
            sum = sum + (source_string[len(source_string) - 1])
            sum = sum & 0xffffffff

        sum = (sum >> 16) + (sum & 0xffff)
        sum = sum + (sum >> 16)
        answer = ~sum
        answer = answer & 0xffff
        answer = answer >> 8 | (answer << 8 & 0xff00)
        return answer

    def _create_packet(self, id, size):
        """
        Create a new echo request packet based on the given "id" and "size".
        """
        header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, 0, id, 1)
        data = struct.pack("d", time.time()) + (size - struct.calcsize("d")) * b'Q'
        my_checksum = self._checksum(header + data)

        header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, socket.htons(my_checksum), id, 1)
        return header + data

    def _do_one_ping(self, size):
        """
        Send one ping to the given "dest_addr" and return the delay.
        """
        my_id = os.getpid() & 0xFFFF

        packet = self._create_packet(my_id, size)
        self.Client.sendto(packet, (self.Host, 1))
        delay = self._receive_one_ping(my_id)

        return delay

    def _receive_one_ping(self, packet_id):
        """
        Receive the ping from the socket.
        """
        time_left = 1
        while True:
            started_select = time.time()
            what_ready = select.select([self.Client], [], [], time_left)
            how_long_in_select = (time.time() - started_select)
            if what_ready[0] == []:  # Timeout
                return

            time_received = time.time()
            rec_packet, _ = self.Client.recvfrom(1024)

            icmp_header = rec_packet[20:28]
            _type, _code, _checksum, p_id, _sequence = struct.unpack("bbHHh", icmp_header)

            if p_id == packet_id:
                bytes_in_double = struct.calcsize("d")
                time_sent = struct.unpack("d", rec_packet[28:28 + bytes_in_double])[0]
                return time_received - time_sent

            time_left = time_left - how_long_in_select
            if time_left <= 0:
                return

class SSH(Connection):
    def __init__(self,*,
        Host:str,
        Port:int,
        Username:str,
        Password:str,
        Encoding:str = 'utf-8',
        ) -> None:

        self.Host = Host
        self.Port = Port
        self.Username = Username
        self.Password = Password
        self.Encoding = Encoding

        self.Client = paramiko.SSHClient()
        self.Client.set_missing_host_key_policy(paramiko.WarningPolicy())
        self.History = ''
        self.Shell = None

    def Connect(self) -> None:
        self.Client.connect(
            hostname = self.Host,
            port     = self.Port,
            username = self.Username,
            password = self.Password,
            )
        self.Shell  = self.Client.invoke_shell(width=0,height=0)
        self.Excute_Mode = self.Check_Multi_Channel_Support()
        self.Banner = self.Client.get_transport().remote_version

    def Check_Multi_Channel_Support(self):
        try : 
            self.Client.invoke_shell().close()
            return True
        except paramiko.ChannelException:
            return False

    @Connection_Required
    def Receive(self) -> str:
        if self.Shell.recv_ready():
            return self.Shell.recv(65536).decode(self.Encoding)

    @Connection_Required
    def Send(self, Message:str, Wait:float = 0.5) -> str:
        if not Message.endswith('\n'): Message += '\n'
        if self.Excute_Mode:
            _ , Stdout , _ = self.Client.exec_command(Message)
            time.sleep(Wait)
            Response = Stdout.read().decode(self.Encoding)
            self.History += Message
            self.History += Response.replace('\r\n','\n').strip() if Response else ''
            return str(Response).replace('\r\n','\n').strip() if Response else ''
        else:
            if not Message.endswith('\n'): Message += '\n'
            self.Shell.send(Message)
            time.sleep(Wait)
            Response = self.Receive()
            self.History += Response.replace('\r\n','\n') if Response else ''
            return str(Response).strip() if Response else ''

    @Connection_Required
    def Disconnect(self) -> None :
        self.Shell = None
        self.Client.close()

    def Is_Connected(self) -> bool:
        return True if self.Client.get_transport() is not None and self.Client.get_transport().is_active() else False

class TCPSocket(Connection):
    def __init__(self,*,
        Host:str,
        Port:int,
        Username:str,
        Password:str,
        Encoding:str = 'utf-8',
        ) -> None :

        self.Host = Host
        self.Port = Port
        self.Username = Username
        self.Password = Password
        self.Encoding = Encoding

        self.Client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.History = ''
        self.Shell = None
        self.Excute_Mode:bool = True

    def Connect(self) -> None :
        self.Client.connect((self.Host, self.Port))

    @Connection_Required
    def Receive(self) -> str :
        return self.Client.recv(65536).decode(self.Encoding)

    @Connection_Required
    def Send(self, Message:str, Wait:float = 0.2) -> str:
        self.Client.sendall(Message.encode())
        time.sleep(Wait)
        return self.Receive()

    @Connection_Required
    def Disconnect(self) -> None :
        self.Client.close()

    def Is_Connected(self) -> bool:
        try: self.Client.recv(16, socket.MSG_DONTWAIT | socket.MSG_PEEK)
        except BlockingIOError: return True
        except ConnectionResetError: return False
        return True
