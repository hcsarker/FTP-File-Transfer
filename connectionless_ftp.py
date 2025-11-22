import socket
import os
import threading

class ConnectionlessFTPServer:
    def __init__(self, host='localhost', port=2122):
        self.host = host
        self.port = port
        self.running = False
        self.server_socket = None
        
    def start_server(self, upload_dir='uploads_connectionless'):
        """Start the connectionless FTP server"""
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)
            
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.bind((self.host, self.port))
        self.running = True
        
        print(f"Connectionless FTP Server listening on {self.host}:{self.port}")
        
        current_file = None
        file_handle = None
        
        while self.running:
            try:
                data, client_address = self.server_socket.recvfrom(65536)  # Max UDP packet size
                
                # Check if this is a new file transmission
                if data.startswith(b"FILE:"):
                    if file_handle:
                        file_handle.close()
                    
                    filename = data[5:].decode().strip()
                    filepath = os.path.join(upload_dir, filename)
                    file_handle = open(filepath, 'w', encoding='utf-8')
                    current_file = filename
                    print(f"Starting to receive file: {filename}")
                    
                elif data == b"END":
                    if file_handle:
                        file_handle.close()
                        file_handle = None
                        print(f"File {current_file} received successfully")
                        current_file = None
                        
                elif file_handle:
                    # Write line to file
                    line = data.decode('utf-8', errors='ignore')
                    file_handle.write(line + '\n')
                    
            except Exception as e:
                print(f"Server error: {e}")
                if file_handle:
                    file_handle.close()
                    file_handle = None
    
    def stop_server(self):
        """Stop the server"""
        self.running = False
        if self.server_socket:
            self.server_socket.close()


class ConnectionlessFTPClient:
    def __init__(self):
        pass
        
    def send_file(self, server_host, server_port, filepath):
        """Send a file using connectionless FTP (no acknowledgments)"""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File {filepath} not found")
            
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        try:
            filename = os.path.basename(filepath)
            
            # Send filename first
            filename_packet = f"FILE:{filename}".encode()
            client_socket.sendto(filename_packet, (server_host, server_port))
            
            with open(filepath, 'r', encoding='utf-8') as file:
                for line in file:
                    # Remove newline and send line
                    line = line.strip()
                    if line:  # Skip empty lines
                        client_socket.sendto(line.encode(), (server_host, server_port))
            
            # Send end of transmission signal
            client_socket.sendto(b"END", (server_host, server_port))
            
            print(f"File {filename} sent successfully")
            return True
            
        except Exception as e:
            print(f"Error sending file: {e}")
            return False
        finally:
            client_socket.close()