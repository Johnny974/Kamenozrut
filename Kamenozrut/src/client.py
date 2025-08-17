import socket
from threading import Thread
import http.client as httplib

HOST = "127.0.0.1"
PORT = 5555


def check_internet_connection(url, timeout):
    connection = httplib.HTTPConnection(url, timeout=timeout)
    try:
        connection.request("HEAD", "/")
        connection.close()
        print("Internet On")
        return True
    except Exception as exep:
        print(exep)
        return False


def receive_messages(sock):
    while True:
        try:
            msg = sock.recv(1024)
            if not msg:
                print("Connection closed.")
                break
            print(f"[SERVER]: {msg.decode()}")
        except Exception as e:
            print(f"Error receiving data from server.{e}")
            break

# TODO Error handling
def connect_to_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((HOST, PORT))
    except ConnectionRefusedError:
        print("Server is not running.")
        return
    print("Connected to server.")

    Thread(target=receive_messages, args=(sock,), daemon=True).start()

    return sock

# TODO: send function method and think about data format

# if check_internet_connection("www.google.com", 3):
#     connect_to_server()
