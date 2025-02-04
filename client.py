# Ex. 2.7 template - client side
# This module is for the client operations and handling server responses
import socket
import protocol
import os


SAVED_PHOTO_LOCATION = "images/client/"  # Directory for saving screenshots on client side


def handle_server_response(my_socket, cmd):
    """
    Handle the server's response based on the client's request.

    Args:
        my_socket (socket): The client's socket connection.
        cmd (str): The command string sent to the server.
    """
    if 'TAKE_SCREENSHOT' in cmd:
        received_file = SAVED_PHOTO_LOCATION + "screenshot.png"
        with open(received_file, 'wb') as f:
            while data := my_socket.recv(1024):
                if data == b"end sending":
                    break
                f.write(data)
        print(f"Screenshot saved as {received_file}")
    elif 'SEND_PHOTO' in cmd:
        file_name = os.path.basename(cmd.split()[1])
        save_file_to = SAVED_PHOTO_LOCATION + file_name
        with open(save_file_to, 'wb') as f:
            while data := my_socket.recv(1024):
                if data == b"end sending":
                    break
                f.write(data)
        print(f"Received file saved as {file_name}")
    else:
        print(my_socket.recv(1024).decode('utf-8'))


def main():
    """
    Connect to the server and send commands interactively.
    """
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.connect((protocol.IP, protocol.PORT))
    print("Connected to the server.")
    print("Available commands: TAKE_SCREENSHOT, SEND_PHOTO, DIR, DELETE, COPY, EXECUTE, EXIT")

    while True:
        cmd = input("Please enter command:\n")
        if protocol.check_cmd(cmd):
            my_socket.send(protocol.create_msg(cmd))
            handle_server_response(my_socket, cmd)
            if cmd == 'EXIT':
                break
        else:
            print("Invalid command or missing parameters\n")
    my_socket.close()


if __name__ == '__main__':
    main()
