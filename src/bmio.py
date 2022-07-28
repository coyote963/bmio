from queue import Queue
import socket
import struct
from rcon_model import RconRequest, RconEvent, event_types
from threading import Thread
from collections import deque
import json

from loguru import logger

from data_coerce import initialize_class
START_DELIMITER = b'\xe2\x94\x90'
END_DELIMITER = b'\xe2\x94\x94'

class Bmio:

    def __init__(self, host, port, password):
        self.sock = self.connect(host, port, password)
        self.send_request(password, RconRequest.login)
        self.request_handlers = {}
        self.packet_queue = Queue(0)


    def connect(self, host: str, port: int, password: str):
        """Get a connection to the boring man rcon"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        return sock


    def run(self):
        """Begins the processing of Rcon Packets"""
        writer_thread = Thread(target = self.threadwrap(self.start_read), args= (self,), daemon = True)
        writer_thread.start()

        reader_thread = Thread(target = self.threadwrap(self.handle_events), args= (self,), daemon = True)
        reader_thread.start()

        writer_thread.join()
        reader_thread.join()

    
    def handle_events(self):
        """Handle packet events as they stream in"""
        while self.packet_queue:
            packet = self.packet_queue.get()

            if packet.EventID in self.request_handlers:
                handlers = self.request_handlers[packet.EventID]
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



    def send_request_with_id(self, request_id: str, request_data: str, request_type: RconRequest):
        """Send a request that comes with a request id"""
        request_message = f'"{request_id}" "{request_data}"'
        self.send_request(request_message, request_type)



    def handler(self, event: RconEvent):
        """Decorator for registering a handler"""
        def add_handler(event, f):
            """"Register a handler"""
            if not event in self.request_handlers:
                self.request_handlers[event] = [f]
            else:
                self.request_handlers[event].append(f)
        
        def decorator(f):
            add_handler(event, f)
            return f
        
        return decorator


    def start_read(self):
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
                # logger.debug(js)
                self.packet_queue.put(initialize_class(js))
                if event_id == RconEvent.rcon_ping.value:
                    self.send_request("None", RconRequest.ping)
            buffer += self.sock.recv(1024)


    def threadwrap(self, threadfunc):
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



