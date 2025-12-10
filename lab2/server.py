import os
from xmlrpc.server import SimpleXMLRPCServer, SimpleXMLRPCRequestHandler
from xmlrpc.client import Binary

UPLOAD_FOLDER = "shared_files"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ("/RPC2",)

def list_files():
    return os.listdir(UPLOAD_FOLDER)

def exists(filename):
    return os.path.exists(os.path.join(UPLOAD_FOLDER, filename))

def upload_chunk(filename, data, is_last):
    """
    filename: string
    data: xmlrpc.client.Binary
    is_last: bool
    """
    path = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.exists(path):
        open(path, "wb").close()
    with open(path, "ab") as f:
        f.write(data.data)
    return True

def download_chunk(filename, offset, size):
    path = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.exists(path):
        return None

    with open(path, "rb") as f:
        f.seek(offset)
        chunk = f.read(size)
        if not chunk:
            return None   # báo hết file
        return Binary(chunk)

def main():
    server = SimpleXMLRPCServer(
        ("127.0.0.1", 8000),
        requestHandler=RequestHandler,
        allow_none=True
    )
    print("RPC File Server running on port 8000...")

    server.register_function(list_files, "list_files")
    server.register_function(exists, "exists")
    server.register_function(upload_chunk, "upload_chunk")
    server.register_function(download_chunk, "download_chunk")
    server.serve_forever()

if __name__ == "__main__":
    main()