import socket
import threading
import json
import os
from datetime import datetime

# ==============================
# Server Configuration
# ==============================

HOST = "127.0.0.1"
PORT = 5000

clients = []
usernames = []

CHAT_HISTORY = "chat_history.json"
USERS_FILE = "users.json"


# ==============================
# Initialize Files
# ==============================

def initialize_files():
    """Create required JSON files if they don't exist."""

    if not os.path.exists(CHAT_HISTORY):
        with open(CHAT_HISTORY, "w") as file:
            json.dump([], file, indent=4)

    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w") as file:
            json.dump([], file, indent=4)


# ==============================
# Load Registered Users
# ==============================

def load_users():

    with open(USERS_FILE, "r") as file:
        return json.load(file)


# ==============================
# Save Registered Users
# ==============================

def save_users(users):

    with open(USERS_FILE, "w") as file:
        json.dump(users, file, indent=4)


# ==============================
# Register New User
# ==============================

def register_user(username):

    users = load_users()

    if username not in users:
        users.append(username)
        save_users(users)


# ==============================
# Save Chat History
# ==============================

def save_chat(username, message):

    with open(CHAT_HISTORY, "r") as file:
        history = json.load(file)

    history.append({

        "username": username,

        "message": message,

        "time": datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    })

    with open(CHAT_HISTORY, "w") as file:
        json.dump(history, file, indent=4)


# ==============================
# Broadcast Message
# ==============================

def broadcast(message):

    disconnected_clients = []

    for client in clients:

        try:
            client.send(message)

        except Exception:
            disconnected_clients.append(client)

    for client in disconnected_clients:

        if client in clients:

            index = clients.index(client)

            clients.remove(client)

            usernames.pop(index)

            client.close()
# ==============================
# Handle Individual Client
# ==============================

def handle_client(client):

    while True:

        try:

            message = client.recv(1024)

            if not message:
                break

            decoded_message = message.decode()

            username = decoded_message.split(":", 1)[0]
            text = decoded_message.split(":", 1)[1]

            print(f"[{username}] {text}")

            save_chat(username, text)

            broadcast(message)

        except Exception:

            break

    if client in clients:

        index = clients.index(client)

        clients.remove(client)

        username = usernames[index]

        usernames.remove(username)

        client.close()

        print(f"{username} disconnected.")

        leave_message = f"SERVER : {username} has left the chat."

        broadcast(leave_message.encode())


# ==============================
# Accept New Connections
# ==============================

def receive_connections():

    while True:

        client, address = server.accept()

        print(f"Connected with {address}")

        client.send("USERNAME".encode())

        username = client.recv(1024).decode()

        register_user(username)

        usernames.append(username)

        clients.append(client)

        print(f"{username} joined the chat.")

        welcome = f"SERVER : {username} joined the chat."

        broadcast(welcome.encode())

        client.send(
            "Successfully connected to the chat server.".encode()
        )

        thread = threading.Thread(
            target=handle_client,
            args=(client,)
        )

        thread.daemon = True

        thread.start()


# ==============================
# Display Active Users
# ==============================

def display_active_users():

    print("\n==============================")
    print(" Active Users ")
    print("==============================")

    if not usernames:

        print("No active users.")

    else:

        for index, user in enumerate(usernames, start=1):

            print(f"{index}. {user}")

    print("==============================\n")
# ==============================
# Server Initialization
# ==============================

def start_server():

    global server

    initialize_files()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:

        server.bind((HOST, PORT))

    except OSError:

        print("Port already in use.")
        return

    server.listen()

    print("=" * 50)
    print("      REAL-TIME CHAT SERVER")
    print("=" * 50)
    print(f"Server Running on {HOST}:{PORT}")
    print("Waiting for clients...")
    print("=" * 50)

    receive_connections()


# ==============================
# Server Information
# ==============================

def show_server_info():

    print("\n")
    print("=" * 50)
    print("SERVER INFORMATION")
    print("=" * 50)
    print(f"Host           : {HOST}")
    print(f"Port           : {PORT}")
    print(f"Connected Users: {len(usernames)}")
    print("=" * 50)
    print()


# ==============================
# Main Menu
# ==============================

def menu():

    while True:

        print("\n========== SERVER MENU ==========")
        print("1. View Active Users")
        print("2. Server Information")
        print("3. Exit")
        print("=================================")

        choice = input("Enter choice: ")

        if choice == "1":

            display_active_users()

        elif choice == "2":

            show_server_info()

        elif choice == "3":

            print("Stopping Server...")

            for client in clients:

                try:

                    client.send(
                        "SERVER : Server shutting down.".encode()
                    )

                    client.close()

                except Exception:

                    pass

            server.close()

            print("Server Closed Successfully.")

            break

        else:

            print("Invalid Choice.")


# ==============================
# Program Entry
# ==============================

if __name__ == "__main__":

    server_thread = threading.Thread(
        target=start_server
    )

    server_thread.daemon = True

    server_thread.start()

    try:

        menu()

    except KeyboardInterrupt:

        print("\nServer Interrupted.")

        for client in clients:

            try:

                client.close()

            except Exception:

                pass

        try:

            server.close()

        except Exception:

            pass

        print("Server Closed.")
