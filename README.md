# FTP Protocol Implementation

A Python project implementing both connection-oriented and connectionless file transfer protocols with a web interface.

## Features

### Connection-Oriented FTP
- Uses TCP sockets for reliable transmission
- File divided into 100-byte chunks
- Acknowledgments required for each chunk
- Timeout and retransmission mechanism
- Guaranteed delivery

### Connectionless FTP
- Uses UDP sockets for fast transmission
- File transferred line by line
- No acknowledgments or retransmissions
- Best-effort delivery

## Installation

1. Clone the repository or create the project structure
2. Install dependencies:
   ```bash
   pip install -r requirements.txt

## RUN
python app.py
http://localhost:5000