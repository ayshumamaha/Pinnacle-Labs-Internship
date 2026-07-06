import socket
import threading
import os
from datetime import datetime

# ==============================
# Client Configuration
# ==============================

HOST = "127.0.0.1"
PORT = 5000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

USERNAME = ""

LOG_FILE = "client_chat_log.txt"


# ==============================
# Save Local Chat Log
# ==============================

def save_log(message):

    with open(LOG_FILE, "a", encoding="utf-8") as file:

        file.write(

            f"[{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}] "

            + message

            + "\n"

        )


# ==============================
# Receive Messages
# ==============================

def receive_messages():

    global USERNAME

    while True:

        try:

            message = client.recv(1024).decode()

            if message == "USERNAME":

                client.send(USERNAME.encode())

            else:

                print("\n" + message)

                save_log(message)

        except ConnectionResetError:

            print("\nConnection Lost.")

            break

        except OSError:

            break

        except Exception:

            print("\nDisconnected from Server.")

            break


# ==============================
# Send Messages
# ==============================

def send_messages():

    while True:

        try:

            text = input()

            if not text.strip():

                continue

            if text.lower() == "/exit":

                print("Leaving Chat...")

                client.close()

                break

            message = f"{USERNAME}:{text}"

            client.send(message.encode())

        except KeyboardInterrupt:

            client.close()

            break

        except Exception:

            print("Unable to send message.")

            break


# ==============================
# Connect To Server
# ==============================

def connect():

    global USERNAME

    print("=" * 45)
    print(" REAL-TIME CHAT APPLICATION ")
    print("=" * 45)

    USERNAME = input("Enter Username : ").strip()

    while USERNAME == "":

        USERNAME = input("Username cannot be empty : ").strip()

    try:

        client.connect((HOST, PORT))

    except ConnectionRefusedError:

        print("\nServer is Offline.")

        exit()

    except Exception:

        print("\nUnable to connect.")

        exit()
# ==============================
# Client Menu
# ==============================

def show_help():

    print("\n")
    print("=" * 50)
    print("CHAT COMMANDS")
    print("=" * 50)
    print("Type your message and press ENTER.")
    print("/help  - Show Commands")
    print("/clear - Clear Screen")
    print("/exit  - Exit Chat")
    print("=" * 50)


# ==============================
# Start Client
# ==============================

def start_chat():

    receive_thread = threading.Thread(
        target=receive_messages
    )

    receive_thread.daemon = True

    receive_thread.start()

    show_help()

    while True:

        try:

            message = input()

            if message.strip() == "":
                continue

            if message.lower() == "/help":

                show_help()

                continue

            if message.lower() == "/clear":

                os.system("cls" if os.name == "nt" else "clear")

                continue

            if message.lower() == "/exit":

                try:

                    client.send(
                        f"{USERNAME}:Left the chat".encode()
                    )

                except Exception:

                    pass

                print("\nDisconnected Successfully.")

                client.close()

                break

            final_message = f"{USERNAME}:{message}"

            client.send(final_message.encode())

            save_log(final_message)

        except KeyboardInterrupt:

            print("\nClosing Client...")

            try:

                client.close()

            except Exception:

                pass

            break

        except BrokenPipeError:

            print("\nServer Connection Lost.")

            break

        except Exception as error:

            print("Error :", error)

            break


# ==============================
# Client Information
# ==============================

def display_client_info():

    print("\n")
    print("=" * 50)
    print("CLIENT INFORMATION")
    print("=" * 50)
    print(f"Username : {USERNAME}")
    print(f"Server   : {HOST}")
    print(f"Port     : {PORT}")
    print(f"Chat Log : {LOG_FILE}")
    print("=" * 50)


# ==============================
# Program Entry
# ==============================

if __name__ == "__main__":

    connect()

    display_client_info()

    start_chat()

    print("\nThank you for using the Real-Time Chat Application.")
