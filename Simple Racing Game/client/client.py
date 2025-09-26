import socket
import threading
import tkinter as tk
import json


class RaceClient:
    def __init__(self, host="127.0.0.1", port=5000):
        self.host = host
        self.port = port
        self.role = None
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.positions = {"btn1": 50, "btn2": 50}

        # GUI
        self.root = tk.Tk()
        self.root.title("Race Client")
        self.canvas = tk.Canvas(self.root, width=500, height=250, bg="white")
        self.canvas.pack()

        # Load assets
        self.car1_img = tk.PhotoImage(file="assets/car1.png").subsample(10, 10)
        self.car2_img = tk.PhotoImage(file="assets/car2.png").subsample(7, 7)

        # Draw players using images
        self.car1 = self.canvas.create_image(self.positions["btn1"], 50, image=self.car1_img, anchor="nw")
        self.label1 = self.canvas.create_text(75, 125, text="Btn1", font=("Arial", 10, "bold"))

        self.car2 = self.canvas.create_image(self.positions["btn2"], 50, image=self.car2_img, anchor="nw")
        self.label2 = self.canvas.create_text(75, 195, text="Btn2", font=("Arial", 10, "bold"))

        # Finish line
        self.canvas.create_line(350, 0, 350, 250, fill="black", dash=(4, 2), width=3)

        # Move button
        self.move_btn = tk.Button(self.root, text="Waiting for role...", state="disabled")
        self.move_btn.pack(pady=10)

    def connect(self):
        self.socket.connect((self.host, self.port))
        threading.Thread(target=self.listen_server, daemon=True).start()

    def send_move(self):
        if self.role:
            event = {"btn": self.role}
            self.socket.sendall(json.dumps(event).encode())

    def listen_server(self):
        while True:
            try:
                data = self.socket.recv(1024).decode()
                if not data:
                    break

                event = json.loads(data)

                if "role" in event:
                    # role assignment
                    self.role = event["role"]
                    self.positions = event["positions"]
                    self.move_btn.config(
                        text=f"Move {self.role.upper()}",
                        state="normal",
                        command=self.send_move,
                    )
                    self.root.title(f"Race Client - {self.role.upper()}")
                    self.update_positions()
                elif "winner" in event:
                    # Winner announcement
                    winner = event["winner"]
                    self.move_btn.config(state="disabled")
                    self.canvas.create_text(
                        200, 20,
                        text=f"{winner.upper()} Wins!",
                        font=("Arial", 16, "bold"),
                        fill="green"
                    )
                else:
                    # Update positions
                    self.positions = event
                    self.update_positions()

            except:
                break

    def update_positions(self):
        # Update image positions
        self.canvas.coords(self.car1, self.positions["btn1"], 75)
        self.canvas.coords(self.label1, self.positions["btn1"] + 25, 125)

        self.canvas.coords(self.car2, self.positions["btn2"], 145)
        self.canvas.coords(self.label2, self.positions["btn2"] + 25, 195)

    def run(self):
        self.connect()
        self.root.mainloop()


if __name__ == "__main__":
    RaceClient().run()
