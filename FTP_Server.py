import socket
import os

def receive_file(client_socket, filename):
    with open(filename, 'wb') as file:
        data = client_socket.recv(1024)
        while data:
            file.write(data)
            data = client_socket.recv(1024)

def send_file(client_socket, filename):
    with open(filename, 'rb') as file:
        data = file.read(1024)
        while data:
            client_socket.send(data)
            data = file.read(1024)

def list_files(client_socket):
    files = os.listdir()  # List files in the server's working directory
    file_list = '\n'.join(files)
    client_socket.send(file_list.encode())

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 8000))
    server_socket.listen(1)

    print("FTP server ready")

    while True:
        client_socket, address = server_socket.accept()
        print(f"Connection from {address}")

        data = client_socket.recv(1024)
        filename = data.decode()

        if filename.startswith('get '):
            filename = filename[4:]
            print(f"Sending file {filename}")
            send_file(client_socket, filename)
        elif filename.startswith('put '):
            filename = filename[4:]
            print(f"Receiving file {filename}")
            receive_file(client_socket, filename)
        elif filename == 'list':
            print("Sending list of files")
            list_files(client_socket)

        client_socket.close()

if __name__ == '__main__':
    main()
