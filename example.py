from datetime import datetime

from src.aio import Loop
from src.aiosocket import ClientSocket


# example 1

def func1():
    for i in range(10):
        print(f'step {i}')
        yield
    return 13

def func2():
    for i in range(30, 33):
        print(f'jump {i}')
        yield
    return 130

print(Loop([
    func1(),
    func2(),
]).run())


# example 2

def request():
    http_request = (
        'GET / HTTP/1.1\n'
        'Host: clipdeclipreapet.ru:443\n\n'
    )
    t = datetime.now()
    print(f'start request {t}')
    socket = ClientSocket('185.22.233.176', 80)
    response = yield from socket.request(http_request)
    print(f'finish request {datetime.now()}, running time: {datetime.now() - t}')
    return response

result = Loop([
    request(),
    request()
]).run()
print(result)