from flask import Flask, render_template, request, jsonify, send_file
import threading
import os
import time
from connection_oriented_ftp import ConnectionOrientedFTPServer, ConnectionOrientedFTPClient
from connectionless_ftp import ConnectionlessFTPServer, ConnectionlessFTPClient

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Server instances
co_server = None
cl_server = None
co_server_thread = None
cl_server_thread = None

def start_connection_oriented_server():
    global co_server
    co_server = ConnectionOrientedFTPServer(port=2121)
    co_server.start_server('uploads_connection_oriented')

def start_connectionless_server():
    global cl_server
    cl_server = ConnectionlessFTPServer(port=2122)
    cl_server.start_server('uploads_connectionless')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/connection-oriented')
def connection_oriented():
    return render_template('connection_oriented.html')

@app.route('/connectionless')
def connectionless():
    return render_template('connectionless.html')

@app.route('/start_co_server', methods=['POST'])
def start_co_server():
    global co_server_thread
    try:
        if co_server_thread and co_server_thread.is_alive():
            return jsonify({'status': 'error', 'message': 'Server already running'})
        
        co_server_thread = threading.Thread(target=start_connection_oriented_server)
        co_server_thread.daemon = True
        co_server_thread.start()
        
        time.sleep(1)  # Give server time to start
        return jsonify({'status': 'success', 'message': 'Connection-oriented server started on port 2121'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/stop_co_server', methods=['POST'])
def stop_co_server():
    global co_server
    try:
        if co_server:
            co_server.stop_server()
        return jsonify({'status': 'success', 'message': 'Connection-oriented server stopped'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/start_cl_server', methods=['POST'])
def start_cl_server():
    global cl_server_thread
    try:
        if cl_server_thread and cl_server_thread.is_alive():
            return jsonify({'status': 'error', 'message': 'Server already running'})
        
        cl_server_thread = threading.Thread(target=start_connectionless_server)
        cl_server_thread.daemon = True
        cl_server_thread.start()
        
        time.sleep(1)  # Give server time to start
        return jsonify({'status': 'success', 'message': 'Connectionless server started on port 2122'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/stop_cl_server', methods=['POST'])
def stop_cl_server():
    global cl_server
    try:
        if cl_server:
            cl_server.stop_server()
        return jsonify({'status': 'success', 'message': 'Connectionless server stopped'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/send_co_file', methods=['POST'])
def send_co_file():
    try:
        if 'file' not in request.files:
            return jsonify({'status': 'error', 'message': 'No file selected'})
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'status': 'error', 'message': 'No file selected'})
        
        # Save uploaded file temporarily
        temp_path = os.path.join('temp', file.filename)
        if not os.path.exists('temp'):
            os.makedirs('temp')
        file.save(temp_path)
        
        # Send file using connection-oriented FTP
        client = ConnectionOrientedFTPClient()
        success = client.send_file('localhost', 2121, temp_path)
        
        # Clean up temp file
        os.remove(temp_path)
        
        if success:
            return jsonify({
                'status': 'success', 
                'message': f'File {file.filename} sent successfully using connection-oriented FTP'
            })
        else:
            return jsonify({'status': 'error', 'message': 'Failed to send file'})
            
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/send_cl_file', methods=['POST'])
def send_cl_file():
    try:
        if 'file' not in request.files:
            return jsonify({'status': 'error', 'message': 'No file selected'})
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'status': 'error', 'message': 'No file selected'})
        
        # Save uploaded file temporarily
        temp_path = os.path.join('temp', file.filename)
        if not os.path.exists('temp'):
            os.makedirs('temp')
        file.save(temp_path)
        
        # Send file using connectionless FTP
        client = ConnectionlessFTPClient()
        success = client.send_file('localhost', 2122, temp_path)
        
        # Clean up temp file
        os.remove(temp_path)
        
        if success:
            return jsonify({
                'status': 'success', 
                'message': f'File {file.filename} sent successfully using connectionless FTP'
            })
        else:
            return jsonify({'status': 'error', 'message': 'Failed to send file'})
            
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/list_files')
def list_files():
    try:
        co_files = []
        cl_files = []
        
        if os.path.exists('uploads_connection_oriented'):
            co_files = os.listdir('uploads_connection_oriented')
        
        if os.path.exists('uploads_connectionless'):
            cl_files = os.listdir('uploads_connectionless')
            
        return jsonify({
            'connection_oriented': co_files,
            'connectionless': cl_files
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    # Create necessary directories
    for dir_name in ['uploads_connection_oriented', 'uploads_connectionless', 'temp']:
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
    
    app.run(debug=True, host='0.0.0.0', port=5000)