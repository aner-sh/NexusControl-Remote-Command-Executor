# Remote Admin Server

A Python-based client-server system that allows remote execution of commands such as file operations, directory listing, screenshot capture, and more. Built using socket programming and a custom command protocol.

## 📌 Project Overview

This project simulates a remote administration tool that communicates over TCP/IP. The client sends commands using a fixed-length header protocol, and the server performs actions accordingly.

### Supported Commands

| Command          | Parameters                     | Description                                 |
|------------------|--------------------------------|---------------------------------------------|
| `DIR <path>`     | 1 parameter (directory path)   | Lists all files in the specified directory  |
| `DELETE <path>`  | 1 parameter (file path)        | Deletes the specified file                  |
| `COPY <src> <dst>` | 2 parameters (source, target) | Copies a file from source to target         |
| `EXECUTE <path>` | 1 parameter (file to run)      | Executes a file on the server               |
| `TAKE_SCREENSHOT`| 0 parameters                   | Captures a screenshot on the server machine |
| `SEND_PHOTO <path>` | 1 parameter (image path)    | Sends an image file from server to client   |
| `EXIT`           | 0 parameters                   | Ends the session                            |


## ⚙️ How It Works

- **Protocol**:
  - Each message sent from the client starts with a 4-digit length field, followed by the command string.
  - The server decodes the message, validates it against the supported command list, and performs the appropriate action.

- **File Transfers**:
  - Binary files like images are sent in 1024-byte chunks.
  - A sentinel value `b"end sending"` marks the end of file transmission.

- **Screenshot Capture**:
  - Uses `pyautogui` to take screenshots on the server side and send them back to the client.

## 🧪 Example Usage

1. Start the server:
   ```python server.py```
2. Start the client in a different terminal or machine:
   ```python client.py```
3. Enter commands like:
```
  DIR C:\Users\Username\Desktop
  TAKE_SCREENSHOT
  DELETE C:\temp\file.txt
  COPY C:\source\file.txt C:\target\file.txt
  SEND_PHOTO C:\images\photo.png
  EXECUTE C:\Program Files\App\app.exe
  EXIT
  ```

## 🛠 Requirements
- Python 3.7+

- pyautogui

- Runs on Windows (due to use of C:\ paths and .exe execution)


## 🔒 Disclaimer
This project is for educational purposes only. Do not use it on machines or networks without proper authorization. Unauthorized remote control of systems is illegal and unethical.

## 👨‍💻 Author
Template originally authored by Barak Gonen (2017), updated to Python 3 in 2020.
Modified and extended for instructional purposes.
