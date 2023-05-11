from select import select
from socket import socket, AF_INET, SOCK_STREAM
from typing import Callable, Generator, List


class BaseSocket:
    BATCH_SIZE = 1024
    ENCODING = 'utf-8'

    __sockets = list()

    def __init__(self, uri: str, port: int):
        self._uri = uri
        self._port = port
        self._socket = socket(AF_INET, SOCK_STREAM)

    def register_socket(self) -> None:
        self.__class__.__sockets.append(self._socket)

    def unregister_socket(self) -> None:
        self.__class__.__sockets.remove(self._socket)

    def socket_list(self) -> List[socket]:
        return self.__class__.__sockets
    
    def is_ready_to_read(self) -> bool:
        ready_to_read, _, _ = select(self.socket_list(), [], [], 0)
        return self._socket in ready_to_read
    
    def is_ready_to_write(self) -> bool:
        _, ready_to_write, _ = select([], self.socket_list(), [], 0)
        return self._socket in ready_to_write
    
    def wait_socket(self, is_ready: Callable) -> Generator:
        while not is_ready():
            yield

    def recieve(self) -> Generator:
        msg = list()
        while self.is_ready_to_read():
            batch = self._socket.recv(self.BATCH_SIZE)
            msg.append(batch.decode(self.ENCODING))
            yield
        return ''.join(msg)


class ServerSocket(BaseSocket):
    def handle(self, handler: Generator):
        self._socket.bind((self._uri, self._port))
        self._socket.listen()
        self.register_socket()

        # wait for socket is ready to read
        yield from self.wait_socket(self.is_ready_to_read)

        # read message
        self._socket.accept()
        request = yield from self.recieve()
        
        # handle message
        response = yield from handler(request)

        # wait for socket is ready to write
        yield from self.wait_socket(self.is_ready_to_write)

        # send response
        self._socket.sendall(response.encode(self.ENCODING))
        self.unregister_socket()
        self._socket.close()


class ClientSocket(BaseSocket):
    def request(self, request: str) -> str:
        self.register_socket()
        self._socket.connect((self._uri, self._port))
        # self._socket.sendall(request.encode(self.ENCODING))

        # wait for socket is ready to write
        yield from self.wait_socket(self.is_ready_to_write)
        
        # send request
        self._socket.sendall(request.encode(self.ENCODING))

        # wait for socket is ready to read
        yield from self.wait_socket(self.is_ready_to_read)

        # read message
        response = yield from self.recieve()
        self.unregister_socket()
        self._socket.close()
        return response