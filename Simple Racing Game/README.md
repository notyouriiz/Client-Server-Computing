# 🏎️ Simple Racing Game (Client-Server with Python)

This project is a **simple racing game** built using **Python socket programming** for the networking part and **Tkinter** for the GUI.  
Two clients connect to a central server, each controlling their own "car". The first car to cross the finish line wins.

## 📸 Expected Output

Here’s how the game looks when running:

![Expected Output](output/Expected%20Output.png)


## ⚙️ Requirements

- Python 3.10+
- Tkinter (comes with Python standard library)
- [Pillow](https://pypi.org/project/pillow/) (only if you want JPG support)

Install Pillow (optional):

```bash
pip install pillow
```

## ▶️ How to Run
1. Start the server
``` bash
python server/server.py
```

2. Start the Player (add another terminal for another player)
``` bash
python client/client.py
```

## 🎮 How to Play
- Each player gets a "Move" button in their client window.

- Clicking Move shifts their car forward.

- The first car to cross the finish line (black dashed line) is declared the winner.

- Once a winner is announced, the game stops and no more moves are allowed.


## 🖼️ Customizing Cars
Replace the images inside client/assets/ with your own PNG files.

```python
# Load assets
self.car1_img = tk.PhotoImage(file="assets/car1.png").subsample(10, 10)
self.car2_img = tk.PhotoImage(file="assets/car2.png").subsample(7, 7)
```