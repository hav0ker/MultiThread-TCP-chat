import os
import socket
import sys
import threading

host = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
port = int(sys.argv[2]) if len(sys.argv) > 2 else 5000

def receive(sock):
    try:
        while True:
            data = sock.recv(4096)
            if not data:
                break
            print(data.decode(errors="replace"), end="", flush=True)
    except OSError:
        pass
    print("\ndisconnected")
    os._exit(0)  


def main():
    sock = socket.create_connection((host, port))
    threading.Thread(target=receive, args=(sock,), daemon=True).start()
    try:
        while True:
            sock.sendall((input() + "\n").encode())
    except (EOFError, KeyboardInterrupt, OSError):
        pass
    finally:
        sock.close()


if __name__ == "__main__":
    main()