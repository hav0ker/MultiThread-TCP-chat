import socket
import threading
import sys

port = int(sys.argv[1]) if len(sys.argv) > 1 else 5000

clients = {}
lock = threading.Lock()


def broadcast(text, sender=None):
    with lock:
        targets = [s for s in clients if s is not sender]
    for s in targets:
        try:
            s.sendall((text + "\n").encode())
        except OSError:
            pass


def handle_client(sock):
    f = sock.makefile("r", encoding="utf-8", errors="replace")
    name = None
    try:
        sock.sendall(b"enter your name: ")
        name = f.readline().strip()[:20] or "anonymous"
        with lock:
            clients[sock] = name
        print(f"* {name} joined")
        broadcast(f"* {name} joined", sender=sock)

        for line in f:
            line = line.strip()
            if line:
                print(f"{name}: {line}")
                broadcast(f"{name}: {line}", sender=sock)
    except OSError:
        pass
    finally:
        with lock:
            clients.pop(sock, None)
        sock.close()
        if name:
            print(f"* {name} left")
            broadcast(f"* {name} left")


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("0.0.0.0", port))
    server.listen()
    server.settimeout(1.0)
    print(f"chat server is listening on port {port} (ctrl+c to stop)")
    try:
        while True:
            try:
                sock, _ = server.accept()
            except socket.timeout:
                continue
            threading.Thread(target=handle_client, args=(sock,), daemon=True).start()
    except KeyboardInterrupt:
        print("\nshutting down...")
    finally:
        server.close()


if __name__ == "__main__":
    main()