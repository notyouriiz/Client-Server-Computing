import socket
import select

# Function to send message to all connected clients
def send_to_all(sock, message):
    # Message not forwarded to server and sender itself
    for s in connected_list:
        if s != server_socket and s != sock:
            try:
                s.send(message.encode())  # encode to bytes
            except:
                # if connection not available
                s.close()
                if s in connected_list:
                    connected_list.remove(s)

if __name__ == "__main__":
    # dictionary to store address corresponding to username
    record = {}
    # List to keep track of socket descriptors
    connected_list = []
    buffer = 4096
    port = 5001

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # listen on all interfaces (works for localhost & LAN)
    server_socket.bind(("0.0.0.0", port))
    server_socket.listen(10)  # listen at most 10 connections at one time

    # Add server socket to the list of readable connections
    connected_list.append(server_socket)

    print("\33[32m \t\t\t\tSERVER WORKING \33[0m")

    while True:
        # Get the list sockets which are ready to be read through select
        rList, _, _ = select.select(connected_list, [], [])

        for sock in rList:
            # New connection
            if sock == server_socket:
                # Handle new connection
                sockfd, addr = server_socket.accept()
                try:
                    name = sockfd.recv(buffer).decode().strip()  # decode bytes
                except:
                    sockfd.close()
                    continue

                if not name:
                    sockfd.close()
                    continue

                connected_list.append(sockfd)

                # if repeated username
                if name in record.values():
                    sockfd.send("\r\33[31m\33[1m Username already taken!\n\33[0m".encode())
                    connected_list.remove(sockfd)
                    sockfd.close()
                    continue
                else:
                    # add name and address
                    record[addr] = name
                    print("Client (%s, %s) connected" % addr, " [", record[addr], "]")
                    sockfd.send("\33[32m\r\33[1m Welcome to chat room. Enter 'tata' anytime to exit\n\33[0m".encode())
                    send_to_all(sockfd, "\33[32m\33[1m\r " + name + " joined the conversation \n\33[0m")

            # Incoming message from a client
            else:
                try:
                    data1 = sock.recv(buffer)
                    if not data1:
                        # No data means client disconnected
                        raise Exception("Disconnected")

                    data = data1.decode().strip()
                    if not data:
                        continue

                    # get addr of client sending the message
                    i, p = sock.getpeername()
                    if data == "tata":
                        msg = "\r\33[1m\33[31m " + record[(i, p)] + " left the conversation \33[0m\n"
                        send_to_all(sock, msg)
                        print("Client (%s, %s) is offline" % (i, p), " [", record[(i, p)], "]")
                        del record[(i, p)]
                        connected_list.remove(sock)
                        sock.close()
                        continue
                    else:
                        msg = "\r\33[1m\33[35m " + record[(i, p)] + ": " + "\33[0m" + data + "\n"
                        send_to_all(sock, msg)

                # abrupt user exit
                except:
                    try:
                        (i, p) = sock.getpeername()
                        send_to_all(sock, "\r\33[31m \33[1m" + record[(i, p)] + " left the conversation unexpectedly\33[0m\n")
                        print("Client (%s, %s) is offline (error)" % (i, p), " [", record[(i, p)], "]\n")
                        del record[(i, p)]
                    except:
                        pass
                    if sock in connected_list:
                        connected_list.remove(sock)
                    sock.close()
                    continue

    server_socket.close()
