import socket
import time
import os
import threading

class ConnectionOrientedFTPServer:
    def __init__(self, host='localhost', port=2121):
        self.host = host
        self.port = port
        self.timeout = 5  # 5 seconds timeout
        self.chunk_size = 100
        self.running = False
        self.server_socket = None
        
    def start_server(self, upload_dir='uploads_connection_oriented'):
        """Start the connection-oriented FTP server"""
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)
            
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.running = True
        
        print(f"Connection-oriented FTP Server listening on {self.host}:{self.port}")
        
        while self.running:
            try:
                client_socket, client_address = self.server_socket.accept()
                print(f"Connection from {client_address}")
                
                # Handle client in a new thread
                client_thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket, client_address, upload_dir)
                )
                client_thread.daemon = True
                client_thread.start()
                
            except Exception as e:
                if self.running:
                    print(f"Server error: {e}")
    
    def handle_client(self, client_socket, client_address, upload_dir):
        """Handle a single client connection"""
        try:
            client_socket.settimeout(self.timeout)
            
            # Receive filename first
            filename_data = client_socket.recv(1024)
            if not filename_data:
                return
                
            filename = filename_data.decode().strip()
            filepath = os.path.join(upload_dir, filename)
            
            print(f"Receiving file: {filename}")
            
            with open(filepath, 'wb') as file:
                sequence_number = 0
                
                while True:
                    try:
                        # Receive chunk
                        chunk = client_socket.recv(self.chunk_size + 10)  # Extra space for sequence number
                        if not chunk:
                            break
                            
                        # Extract sequence number and data
                        try:
                            seq_str, data = chunk.split(b':', 1)
                            received_seq = int(seq_str.decode())
                        except:
                            print("Invalid packet format")
                            break
                        
                        # Write data to file
                        file.write(data)
                        
                        # Send acknowledgment
                        ack = f"ACK:{received_seq}".encode()
                        client_socket.send(ack)
                        
                        sequence_number = received_seq + 1
                        
                        # Check if this was the last chunk (less than chunk_size)
                        if len(data) < self.chunk_size:
                            break
                            
                    except socket.timeout:
                        print(f"Timeout waiting for chunk {sequence_number}")
                        continue
                    except Exception as e:
                        print(f"Error receiving chunk: {e}")
                        break
            
            print(f"File {filename} received successfully")
            client_socket.close()
            
        except Exception as e:
            print(f"Error handling client {client_address}: {e}")
            client_socket.close()
    
    def stop_server(self):
        """Stop the server"""
        self.running = False
        if self.server_socket:
            self.server_socket.close()


class ConnectionOrientedFTPClient:
    def __init__(self, timeout=5):
        self.timeout = timeout
        self.chunk_size = 100
        self.max_retries = 3
        
    def send_file(self, server_host, server_port, filepath):
        """Send a file using connection-oriented FTP with acknowledgments"""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File {filepath} not found")
            
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.settimeout(self.timeout)
        
        try:
            client_socket.connect((server_host, server_port))
            filename = os.path.basename(filepath)
            
            # Send filename first
            client_socket.send(filename.encode())
            time.sleep(0.1)  # Small delay to ensure server is ready
            
            with open(filepath, 'rb') as file:
                sequence_number = 0
                
                while True:
                    chunk = file.read(self.chunk_size)
                    if not chunk:
                        break
                    
                    # Send chunk with sequence number
                    packet = f"{sequence_number}:".encode() + chunk
                    retries = 0
                    
                    while retries < self.max_retries:
                        try:
                            client_socket.send(packet)
                            
                            # Wait for acknowledgment
                            ack = client_socket.recv(1024).decode()
                            if ack.startswith("ACK:") and int(ack.split(":")[1]) == sequence_number:
                                break
                            else:
                                print(f"Invalid ACK received: {ack}")
                                retries += 1
                                
                        except socket.timeout:
                            print(f"Timeout for chunk {sequence_number}, retrying...")
                            retries += 1
                    
                    if retries == self.max_retries:
                        raise Exception(f"Failed to send chunk {sequence_number} after {self.max_retries} retries")
                    
                    sequence_number += 1
                    
            print(f"File {filename} sent successfully")
            return True
            
        except Exception as e:
            print(f"Error sending file: {e}")
            return False
        finally:
            client_socket.close()