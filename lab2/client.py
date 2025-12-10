import os
from xmlrpc.client import ServerProxy, Binary

SERVER_URL = "http://127.0.0.1:8000"
proxy = ServerProxy(SERVER_URL, allow_none=True)

CHUNK_SIZE = 4096

def upload_file():
    filename = input("Enter filename to upload: ").strip()
    if not os.path.exists(filename):
        print("File not found!")
        return
    with open(filename, "rb") as f:
        while True:
            chunk = f.read(CHUNK_SIZE)
            if not chunk:
                proxy.upload_chunk(filename, Binary(b""), True)
                break
            proxy.upload_chunk(filename, Binary(chunk), False)
    print("Upload completed.")

def download_file():
    filename = input("Enter filename to download: ").strip()
    if not proxy.exists(filename):
        print("File not found on server.")
        return
    save_as = "download_" + filename
    offset = 0
    with open(save_as, "wb") as f:
        while True:
            data = proxy.download_chunk(filename, offset, CHUNK_SIZE)
            if data is None:   # FIX: server báo hết file
                break
            f.write(data.data)
            offset += len(data.data)
    print("Downloaded successfully:", save_as)


def main():
    while True:
        cmd = input("Command (send/get/list/exit): ").strip().lower()
        if cmd == "send":
            upload_file()
        elif cmd == "get":
            download_file()
        elif cmd == "list":
            print("Files:", proxy.list_files())
        elif cmd == "exit":
            break
        else:
            print("Invalid command.")
if __name__ == "__main__":
    main()