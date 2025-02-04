# Ex. 2.7 template - protocol module
# This module defines the protocol for a remote command server
# Author: Barak Gonen, 2017 (Modified for Python 3, 2020)
import socket


LENGTH_FIELD_SIZE = 4
IP = '127.0.0.1'
PORT = 8820

# Dictionary to store command functions and their parameter counts
COMMANDS = {
    "DIR": ("glob.glob", 1),
    "DELETE": ("os.remove", 1),
    "COPY": ("shutil.copy", 2),
    "EXECUTE": ("subprocess.call", 1),
    "TAKE_SCREENSHOT": ("", 0),
    "SEND_PHOTO": ("", 1),
    "EXIT": ("", 0)
}


def available_commands():
    '''
    Build available menu options base on COMMANDS dictionary keys
    Returns: menu options as string
    '''
    menu_text = "Available commands: " + ", ".join(list(COMMANDS.keys()))
    return menu_text


def check_cmd(data):
    """
    Check if the command is defined in the protocol with the correct number of parameters.

    Args:
        data (str): The command and its parameters.

    Returns:
        bool: True if the command and parameters match the protocol; otherwise, False.
    """
    params = data.split()
    if params[0] not in COMMANDS:
        return False
    if len(params) - 1 != COMMANDS[params[0]][1]:
        return False
    return True


def create_msg(data):
    """
    Create a protocol message with a length field.

    Args:
        data (str): The message content.

    Returns:
        bytes: Encoded message with length header.
    """
    header = f"{len(data):0>4}"
    message = header + data
    return message.encode()


def get_msg(my_socket):
    """
    Extract message from protocol, without the length field.

    Args:
        my_socket (socket): The socket instance used for communication.

    Returns:
        tuple: (bool, str) - True and the command if protocol is valid; else False and "Error".
    """
    data = my_socket.recv(1024).decode()
    print(f"Data received: {data}")
    try:
        length = int(data[:4])
    except ValueError:
        return False, "Error"
    command = data[4:]
    if len(command) != length:
        return False, "Error"
    if not check_cmd(command):
        return False, "Error"
    return True, command


def test(function_to_check, reference):
    """
    Test a function against an expected result.

    Args:
        function_to_check (str): Function call as a string to evaluate.
        reference: Expected output to check against.
    """
    to_check = eval(function_to_check)
    if isinstance(to_check, bytes):
        to_check = to_check.decode()
    print(to_check)
    if to_check == reference:
        print(f"{function_to_check:40} expected result: {reference}. test pass successfully")
    else:
        print(f"{function_to_check:40} expected result: {reference}. test failed")


if __name__ == "__main__":
    # Example tests for the protocol functions
    test('check_cmd("DIR")', False)
    test('check_cmd("DIR C:\\cyber")', True)
    file_name = "C:\\\\cyber\\\\a.txt"
    test(f'create_msg("DELETE {file_name}")', f'0021DELETE C:\\cyber\\a.txt')
