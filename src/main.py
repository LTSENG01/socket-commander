import socket
import threading
import requests

HOST = ''           # Accepts all connections
PORT = 65433        # Port to listen on (non-privileged ports are > 1023)
STOP = "STOP"       # Command to shutdown the server


def handle_connection(conn, addr):
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                # send EOF (Command + D) to end its own connection
                break

            decoded = data.decode("utf-8")
            print(str(addr) + ": " + decoded)

            if decoded == "start_vacuum":
                print("Handling start_vacuum.")
                requests.get("https://maker.ifttt.com/trigger/start_vacuum/with/key/bzpgfudiKkSFwcPARaQqGf")
            if decoded == "return_vacuum":
                print("Handling return_vacuum.")
                requests.get("https://maker.ifttt.com/trigger/return_vacuum/with/key/bzpgfudiKkSFwcPARaQqGf")

            if STOP in decoded:
                # if the program receives STOP
                print("Server closing.")
                raise ConnectionAbortedError()


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen()

    print(f"Server is listening on {PORT}.")
    while True:
        try:
            conn, addr = s.accept()
            threading.Thread(target=handle_connection, args=(conn, addr)).start()
        except ConnectionAbortedError:
            s.shutdown(socket.SHUT_RDWR)
            s.close()
