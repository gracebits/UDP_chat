import socket
import threading

def broadcast_message(message, server_socket, clients):
    for client in clients:
        try:
            server_socket.sendto(message.encode(), client)
        except Exception as e:
            print(f"Error broadcasting to {client}: {e}")

def handle_server_input(server_socket, clients):
    while True:
        try:
            message = input()
            if message.lower() == "shutdown":
                print("Shutting down the server...")
                broadcast_message("server: shutdown", server_socket, clients)
                break
            broadcast_message(f"server: {message}", server_socket, clients)
            print(f"server: {message}")  # Show server's own messages
        except Exception as e:
            print(f"Error handling server input: {e}")
            break

def server():
    host = "192.168.1.4"  # Use 127.0.0.1 for localhost testing
    port = 12345

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 65536)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 65536)
    server_socket.bind((host, port))

    clients = set()
    print("Server is running and ready to broadcast messages.")

    # Start a separate thread to handle server input
    input_thread = threading.Thread(target=handle_server_input, args=(server_socket, clients), daemon=True)
    input_thread.start()

    try:
        while True:
            data, addr = server_socket.recvfrom(1024)
            message = data.decode().strip()

            if addr not in clients:
                clients.add(addr)
                broadcast_message(f"server: welcome {message}", server_socket, clients)
                print(f"server: welcome {message}")
            else:
                broadcast_message(f"{message}", server_socket, clients)
                print(message)  # Display all messages
    except KeyboardInterrupt:
        print("\nServer stopped manually.")
    finally:
        server_socket.close()
        print("Socket closed. Server shutdown complete.")

if __name__ == "__main__":
    server()
