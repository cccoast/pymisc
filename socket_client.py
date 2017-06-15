import socket

if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('127.0.0.1', 9876))
    import time
    time.sleep(2)
    sock.send('hello world')
    print sock.recv(1024)
    sock.close()