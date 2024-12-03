import socket
import threading

def receive_messages(client_socket):
    while True:
        try:
            data, addr = client_socket.recvfrom(1024)
            message = data.decode()
            print(message)  # Display all received messages
        except Exception as e:
            print("Error receiving message:", e)
            break

def client():
    server_host = input("Enter server IP: ") or "127.0.0.1"
    server_port = 12345

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    username = input("Enter your username: ").strip()
    client_socket.sendto(username.encode(), (server_host, server_port))

    # Start a thread to receive messages
    threading.Thread(target=receive_messages, args=(client_socket,), daemon=True).start()

    print("You can start chatting now! Type your message and press Enter.")
    print("Type 'exit' to leave the chat.")
    try:
        while True:
            message = input()
            if message.lower() == "exit":
                print("Exiting chat...")
                break
            client_socket.sendto(f"client {username}: {message}".encode(), (server_host, server_port))
    except KeyboardInterrupt:
        print("\nClient stopped manually.")
    finally:
        client_socket.close()
        print("Disconnected from server.")

if __name__ == "__main__":
    client()
