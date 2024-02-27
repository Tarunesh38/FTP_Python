import socket

def send_file(server_socket, filename):
    with open(filename, 'rb') as file:
        server_socket.send(file.read())

def receive_file(server_socket, filename):
    with open(filename, 'wb') as file:
        data = server_socket.recv(1024)
        while data:
            file.write(data)
            data = server_socket.recv(1024)

def list_files(server_socket):
    server_socket.send(b'list')
    files_list = server_socket.recv(4096).decode()
    print("List of files on the server:")
    print(files_list)

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.connect(('localhost', 8000))

    while True:
        print("OPTIONS:")
        print("1. Upload a file")
        print("2. Download a file")
        print("3. List files on the server")
        print("4. Exit")
        option = input("Enter the option: ")

        if option == '1':
            filename = input("Enter filename to send: ")
            server_socket.send(f"put {filename}".encode())
            send_file(server_socket, filename)
            print("File sent successfully")

        elif option == '2':
            filename = input("Enter filename to receive: ")
            server_socket.send(f"get {filename}".encode())
            receive_file(server_socket, filename)
            print("File received successfully")

        elif option == '3':
            list_files(server_socket)

        elif option == '4':
            server_socket.send(b'exit')
            server_socket.close()
            break

if __name__ == '__main__':
    main()
