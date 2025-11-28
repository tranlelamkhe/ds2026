import socket

if __name__ == '__main__':

    host = '127.0.0.1'
    port = 8080

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))

    while True:
        cmd = input("Command (send/get/exit): ").strip().lower()

        if cmd == "send":
            filename = input("Enter .txt filename to send: ")

            try:
                f = open(filename, "rb")  #open in binary
            except FileNotFoundError:
                print("File not found!")
                continue

            client.sendall(f"SEND {filename}".encode())

            while True:
                chunk = f.read(1024)
                if not chunk:
                    break
                client.sendall(chunk)

            client.sendall(b"__END__")

            ack = client.recv(1024)
            if ack != b"__RECEIVED__":
                print("Error: server did not acknowledge file")
                f.close()
                continue

            print("File sent successfully!")
            f.close()

        elif cmd == "get":
            filename = input("Enter filename to download: ")

            client.sendall(f"GET {filename}".encode())

            status = client.recv(1024)
            if status == b"__NOTFOUND__":
                print("Server: File not found!")
                continue

            newname = "download_" + filename
            with open(newname, "wb") as fo:  
                while True:
                    data = client.recv(1024)
                    if b"__END__" in data:
                        fo.write(data.replace(b"__END__", b""))
                        break
                    fo.write(data)

            print("Downloaded successfully!")
            print("Saved as:", newname)

        elif cmd == "exit":
            client.sendall("EXIT".encode())
            break

    client.close()
