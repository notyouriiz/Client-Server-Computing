import socket, sys, threading

# Helper function (formatting)
def display():
    you = "\33[33m\33[1m" + " You: " + "\33[0m"
    sys.stdout.write(you)
    sys.stdout.flush()

def handle_send(sock):
    """Thread for sending messages"""
    while True:
        msg = sys.stdin.readline().strip()
        if not msg:
            continue
        if msg == "tata":
            sock.send(msg.encode())
            print("\nExiting chat...")
            sock.close()
            sys.exit()
        else:
            sock.send(msg.encode())
            display()

def main():
    if len(sys.argv) < 2:
        host = "localhost"
    else:
        host = sys.argv[1]

    port = 5001 #make sure it the same with server.py

    # asks for user name
    name = input("\33[34m\33[1m CREATING NEW ID:\n Enter username: \33[0m")

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # remove timeout so it doesn’t disconnect too early
    # s.settimeout(2)

    # connecting host
    try:
        s.connect((host, port))
    except Exception as e:
        print(f"\33[31m\33[1m Can't connect to the server ({e}) \33[0m")
        sys.exit()

    # if connected
    s.send(name.encode())
    display()

    # start input thread
    threading.Thread(target=handle_send, args=(s,), daemon=True).start()

    while True:
        try:
            data = s.recv(4096)
            if not data:
                print('\33[31m\33[1m \rDISCONNECTED!!\n \33[0m')
                break
            else:
                sys.stdout.write(data.decode())
                display()
        except ConnectionResetError:
            print("\n\33[31m Server closed the connection. \33[0m")
            break
        except Exception as e:
            print(f"\n\33[31m Error: {e}\33[0m")
            break

    print("Exiting client...")
    s.close()
    sys.exit()

if __name__ == "__main__":
    main()
