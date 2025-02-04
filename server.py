import shutil
import socket
import subprocess

import protocol
import pyautogui
import glob
import os

# Ex. 2.7 template - server side
# This module handles server-side operations for the remote command protocol

PHOTO_PATH = "images/server/"  # Directory for saving server screenshots


def check_client_request(cmd):
    """
    Validate the client's command and parameters.

    Args:
        cmd (str): Command string from client.

    Returns:
        tuple: (bool, str, list) - True if valid, the command name, and parameter list.
    """
    params = []
    if protocol.check_cmd(cmd):
        items = cmd.split()
        command = items[0]
        if len(items) > 1:
            params = items[1:]
        return True, command, params
    return False, None, params


def send_file(file_name):
    """
    Send a file's contents line by line.

    Args:
        file_name (str): Name of the file to send.

    Returns:
        list: List of file data in chunks.
    """
    ret_lines = []
    with open(file_name, 'rb') as f:
        while chunk := f.read(1024):
            ret_lines.append(chunk)
    ret_lines.append(b"end sending")
    print(ret_lines)
    return ret_lines


def send_response_to_client(response, client_socket):
    """
    Send a response to the client, handling short responses or files.

    Args:
        response: The response data to send (str or list of bytes).
        client_socket (socket): The client socket instance.
    """
    if isinstance(response, list):
        for lines in response:
            client_socket.send(lines)
    else:
        client_socket.send(response.encode())


def handle_client_request(command, params):
    """
    Create a response based on the command and parameters.

    Args:
        command (str): Command name.
        params (list): Command parameters.

    Returns:
        str or list: Response string or list of bytes.
    """
    if command == 'TAKE_SCREENSHOT':
        screenshot_file = PHOTO_PATH + "screenshot.png"
        pyautogui.screenshot(screenshot_file)
        return send_file(screenshot_file)
    elif command == 'SEND_PHOTO':
        return send_file(params[0])
    elif command == 'DIR':
        return "\n".join(glob.glob(params[0] + "\\*.*"))
    elif command == 'DELETE':
        os.remove(params[0])
        return f'The file {params[0]} was deleted'
    elif command == 'COPY':
        shutil.copy(params[0], params[1])
        return f'The file {params[0]} was copied to {params[1]}'
    elif command == 'EXECUTE':
        subprocess.call(params[0])
        return "Execution completed"
    else:
        return "Closing the Server"


def main():
    """
    Main server loop handling client connections and requests.
    """
    server_socket = socket.socket()
    server_socket.bind((protocol.IP, protocol.PORT))
    server_socket.listen(1)
    print(f"Server listening on {protocol.IP}:{protocol.PORT}")
    client_socket, client_address = server_socket.accept()
    print(f"Client connected at {client_address}")

    while True:
        valid_protocol, cmd = protocol.get_msg(client_socket)
        if valid_protocol:
            valid_cmd, command, params = check_client_request(cmd)
            if valid_cmd:
                response = handle_client_request(command, params)
            else:
                response = 'Bad command or parameters'
            send_response_to_client(response, client_socket)
        else:
            send_response_to_client('Protocol error', client_socket)
            client_socket.recv(1024)
    print("Closing connection")


if __name__ == '__main__':
    main()
