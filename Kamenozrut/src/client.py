import socket
from threading import Thread
import http.client as httplib
import re
import json

HOST = "127.0.0.1"
PORT = 5555
callback_on_message = None


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
def connect_to_server(on_message=None):
    global callback_on_message
    callback_on_message = on_message
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
        # multiplayer_error = "Nickname accepted, you are now online!"
        if callback_on_message:
            callback_on_message("Nickname accepted, you are now online!")
    elif msg_type == "NICKNAME_TAKEN":
        # multiplayer_error = "Nickname already taken, choose another one."
        if callback_on_message:
            callback_on_message("Nickname already taken, choose another one.")
    elif msg_type == "NICKNAME_INVALID":
        # multiplayer_error = "Invalid nickname format."
        if callback_on_message:
            callback_on_message("Invalid nickname format.")
    elif msg_type == "MATCH_FOUND":
        opponent = message.get("opponent")
        if callback_on_message:
            callback_on_message("Match found. Your opponent is {opponent}".format(opponent=opponent),
            opponent=opponent)
    elif msg_type == "OPPONENTS_GRID":
        opponents_grid = message.get("grid")
        opponents_color_scheme = message.get("color_scheme")
        if callback_on_message:
            callback_on_message("Opponent's grid and color scheme received.",
            opponents_grid=opponents_grid,
            opponents_color_scheme=opponents_color_scheme)


def is_valid_nickname(nickname):
    if nickname is None or len(nickname) == 0:
        return "Nickname is required."
    elif not re.match(r"^[A-Za-z0-9_]{1,15}$", nickname):
        return "Nickname can only contain letters without diacritics, numbers and underscores."
    else:
        return True
