import socket
import os

#folder to store uploaded files
UPLOAD_FOLDER = "shared_files"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

if __name__ == '__main__':
    host = '127.0.0.1'
    port = 8080
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    sock.listen(1)

    print('Waiting for client...')
    conn, addr = sock.accept()
    print('Connected with:', addr)

    while True:
        command = conn.recv(1024).decode()
        if not command:
            break

        parts = command.split()

        if parts[0] == "SEND":
            filename = parts[1]
            print(f"\nReceiving file: {filename}")

            server_filename = os.path.join(UPLOAD_FOLDER, filename)

            with open(server_filename, "wb") as fo: #open in binary
                while True:
                    data = conn.recv(1024)
                    if b"__END__" in data:  
                        index = data.find(b"__END__")
                        fo.write(data[:index])  
                        break
                    fo.write(data)

            print("File received successfully!")
            print("Saved as:", server_filename)

            conn.sendall(b"__RECEIVED__")

        elif parts[0] == "GET":
            filename = parts[1]
            filepath = os.path.join(UPLOAD_FOLDER, filename)

            if not os.path.exists(filepath):
                conn.sendall(b"__NOTFOUND__")
                print("File not found:", filename)
                continue

            conn.sendall(b"__OK__")
            print(f"Client requested file: {filename}")

            with open(filepath, "rb") as f: #send in binary
                while True:
                    chunk = f.read(1024)
                    if not chunk:
                        break
                    conn.sendall(chunk)

            conn.sendall(b"__END__")
            print("File sent successfully!")

        elif parts[0] == "EXIT":
            print("Client disconnected.")
            break

    conn.close()
    sock.close()
