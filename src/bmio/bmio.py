from queue import Queue
import socket
import struct
import random
import string
from threading import Thread
import json
from typing import Callable

from .rcon_model import RconRequest, RconEvent, RequestDataBase


from loguru import logger

from .data_coerce import initialize_class
from .rcon_model.command_types import Command


START_DELIMITER = b'\xe2\x94\x90'
END_DELIMITER = b'\xe2\x94\x94'

class Bmio:

    def __init__(
        self,
        host = 'localhost',
        port = 42070,
        password = 'admin',
        parallelism = 2,

    ):
        """An implementation of the Producer Consumer Queue for Rcon Objects."""
        self.sock = self.__connect(host, port, password)
        self.send_request(password, RconRequest.login)
        self.event_handlers = {}
        self.request_handlers = {}
        self.packet_queue = Queue(0)
        self.parallelism = parallelism


    def run(self):
        """Begins the processing of Rcon Packets"""
        writer_thread = Thread(target = self.__threadwrap(self.__start_read), args= (self,), daemon = True)
        writer_thread.start()
        
        for i in range(0, self.parallelism):
            reader_thread = Thread(target = self.__threadwrap(self.__handle_events), args= (self,), daemon = True)
            reader_thread.start()

        writer_thread.join()
        reader_thread.join()


    def handler(self, event: RconEvent):
        """Decorator for registering a handler"""
        def add_handler(event, f):
            """"Register a handler"""
            if not event in self.event_handlers:
                self.event_handlers[event] = [f]
            else:
                self.event_handlers[event].append(f)
        def decorator(f):
            add_handler(event, f)
            return f
        return decorator
    


    def send_command(self, command: Command, *args):
        """
            Sends a command over to the server
            
                Parameters:
                    command: The type of command
                    args*
        """
        full_command = command.value
        for arg in args:
            full_command += f' "{arg}"'
        self.send_request(full_command, RconRequest.command)


    def request_data(
        self, 
        request_type: RconRequest, 
        callback: Callable,
        request_params: str = "None"
    ):
        """
            Request game data from the server. When the data is returned, the callback function is called
            
                Parameters:
                    request_type: The type of request
                    callback: function that will be called when the data is returned
                    request_params: optional arguments that come with the request 
        """
        request_id = self.__generate_hash()
        self.send_request_with_id(
            request_id,
            request_params,
            request_type
        )
        self.request_handlers[request_id] = callback


    def __generate_hash(self):
        return ''.join(random.choices(string.ascii_lowercase, k=5))


    def __connect(self, host: str, port: int, password: str):
        """Get a _connection to the boring man rcon"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        return sock


    def __handle_events(self):
        """Handle packet events as they stream in"""
        while self.packet_queue:
            packet = self.packet_queue.get()
            
            if isinstance(packet, RequestDataBase):
                if packet.RequestID in self.request_handlers:
                    f = self.request_handlers.pop(packet.RequestID)
                    f(packet)

            elif packet.EventID in self.event_handlers:
                handlers = self.event_handlers[packet.EventID]
                for f in handlers:
                    f(packet)


    def send_request(self, request_data: str, request_type: RconRequest):
        """Send a simple request"""
        request_message = request_data + "\00" 
        request = struct.Struct(
            f'h{ len(bytes(request_message, "utf-8")) }s'
        ).pack(
            request_type.value, request_message.encode('utf-8')
        ) 
        self.sock.send(request)


    def send_request_with_id(self, request_id: str, request_params: str, request_type: RconRequest):
        """Send a request that comes with a request id
            Parameters
                request_id: The unique id associated with this request. Will be returned alongside the data
                request_params: optional parameters associated with the request
                request_type: the RconRequest enum of the request
        """
        request_message = f'"{request_id}" "{request_params}"'
        self.send_request(request_message, request_type)


    def __start_read(self):
        """Start reading and only stop when the delimiters are not present"""
        buffer = self.sock.recv(1024)
        while buffer.find(END_DELIMITER) != -1 and buffer.find(START_DELIMITER) != -1:

            start_index = buffer.find(START_DELIMITER)
            end_index = buffer.find(END_DELIMITER) + len(END_DELIMITER)

            data = buffer[start_index:end_index]
            buffer = buffer[end_index:]
            if data:
                data_info = struct.unpack_from('<'+'3s'+'h', data, 0)
                event_data = struct.unpack_from(
                    '<'+'3s'+'h'+'h'+str(data_info[1])+'s', data, 0)
                event_id = event_data[2]
                message_string = event_data[3].decode().strip()
                message_string = message_string[:-1]
                js = json.loads(message_string)
                logger.debug(js)
                self.packet_queue.put(initialize_class(js))
                if event_id == RconEvent.rcon_ping.value:
                    self.send_request("None", RconRequest.ping)
            buffer += self.sock.recv(1024)


    def __threadwrap(self, threadfunc):
        """"Wrap threads that should be restarted"""
        def wrapper(self):
            while True:
                try:
                    threadfunc()
                except BaseException as e:
                    logger.error('{!r}; restarting thread'.format(e))
                else:
                    logger.error(f'Thread exited normally: {threadfunc.__name__}')
        return wrapper


    