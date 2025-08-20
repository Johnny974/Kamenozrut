import socket
from threading import Thread
import http.client as httplib
import re
import json

HOST = "127.0.0.1"
PORT = 5555


def check_internet_connection(url, timeout):
    connection = httplib.HTTPConnection(url, timeout=timeout)
    try:
        connection.request("HEAD", "/")
        connection.close()
        return True
    except Exception as exep:
        print(exep)
        return False


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


def send_message(sock, message_type, data):
    message = {
        "type": message_type,
        "data": data
    }
    json_message = json.dumps(message) + '\n'
    sock.sendall(json_message.encode('utf-8'))


def receive_messages(sock):
    buffer = ""
    try:
        while True:
            data = sock.recv(1024).decode("utf-8")
            if not data:
                break
            buffer += data
            while "\n" in buffer:
                line, buffer = buffer.split("\n", 1)
                if line.strip():
                    try:
                        msg = json.loads(line)
                        handle_server_message(msg)
                    except json.JSONDecodeError:
                        print(f"Invalid JSON from server: {line}")
    except Exception as e:
        print(f"Connection error: {e}")
    finally:
        print("Disconnected from server.")


def handle_server_message(message):
    msg_type = message.get("type")

    if msg_type == "NICKNAME_OK":
        print("Nickname accepted, you are now online!")
    elif msg_type == "NICKNAME_TAKEN":
        print("Nickname already taken, choose another one.")
    elif msg_type == "NICKNAME_INVALID":
        print("Invalid nickname format.")
    elif msg_type == "MATCH_FOUND":
        print(f"Match found: {message.get('opponent')}")
    else:
        print(f"ℹ️ Unknown message from server: {message}")


def is_valid_nickname(nickname):
    if nickname is None or len(nickname) == 0:
        return "Nickname is required."
    elif not re.match(r"^[A-Za-z0-9_]{1,15}$", nickname):
        return "Nickname can only contain letters, numbers and underscores."
    else:
        return True
