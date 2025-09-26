import socket
import threading
import json


class RaceServer:
    def __init__(self, host="127.0.0.1", port=5000):
        self.host = host
        self.port = port
        self.clients = {}  # {conn: role}
        self.positions = {"btn1": 50, "btn2": 50}  # starting positions
        self.available_roles = ["btn1", "btn2"]  # assign in order
        self.lock = threading.Lock()

    def broadcast(self, message):
        with self.lock:
            for conn in list(self.clients.keys()):
                try:
                    conn.sendall(message.encode())
                except:
                    del self.clients[conn]

    def handle_client(self, conn, addr):
        print(f"[CONNECTED] {addr}")

        # Assign role to client
        with self.lock:
            if not self.available_roles:
                conn.sendall(json.dumps({"error": "No more roles available"}).encode())
                conn.close()
                return
            role = self.available_roles.pop(0)
            self.clients[conn] = role

        # Send initial data (role + positions)
        init_data = {"role": role, "positions": self.positions}
        conn.sendall(json.dumps(init_data).encode())

        while True:
            try:
                data = conn.recv(1024).decode()
                if not data:
                    break

                event = json.loads(data)
                if "btn" in event:
                    btn = event["btn"]
                    self.positions[btn] += 10  # move forward
                    print(f"[UPDATE] {btn} -> {self.positions[btn]}")
                    self.broadcast(json.dumps(self.positions))

                if self.positions[btn] >= 350:
                    print(f"[WINNER] {btn.upper()} reached finish line!")
                    self.broadcast(json.dumps({"winner": btn}))
                    break

            except:
                break

        with self.lock:
            if conn in self.clients:
                freed_role = self.clients[conn]
                self.available_roles.insert(0, freed_role)
                del self.clients[conn]

        conn.close()
        print(f"[DISCONNECTED] {addr} released {role}")

    def start(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)
        print(f"[LISTENING] Server started on {self.host}:{self.port}")

        while True:
            conn, addr = server_socket.accept()
            thread = threading.Thread(target=self.handle_client, args=(conn, addr))
            thread.start()


if __name__ == "__main__":
    RaceServer().start()
