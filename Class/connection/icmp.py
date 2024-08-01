import os, time, socket, struct, select
from Function.decorator import Connection_Required
from .base import Connection

ICMP_ECHO_REQUEST = 8

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
