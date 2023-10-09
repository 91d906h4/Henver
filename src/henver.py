# Import modules.
import socket
import threading
import webbrowser

from src.hcli import hcli
from src.logger import logger
from src.hrequest import hrequest
from src.hresponse import hresponse
from src.hsecurity import hsecurity

# Call CLI tool.
SERVER_HOST, SERVER_PORT, quiet_start = hcli()

# Create socket.
try:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(1)

    # Server starting message.
    print(f"Thank you for using Henver HTTP Server.")
    print(f"Host {SERVER_HOST} listening on port {SERVER_PORT}.")
    print(f"Press CTRL-C to stop server...")

    # If server started up successfully, then open website in browser.
    if not quiet_start: webbrowser.open(f"http://{SERVER_HOST}:{SERVER_PORT}")

    logger("INFO", f"Server start.", SERVER_HOST)

except Exception as e:
    # Quit if server start failed.
    print(f"Server start failed. Here's the error messages:")
    print(str(e))

    logger("FITAL", "Server start failed. Error message: " + str(e), SERVER_HOST)

    exit(-1)

# Server index.
def index(client_connection: socket.socket, request: str, client_address: str) -> None:
    # Parse request.
    request = hrequest(request)

    # Run security check.
    request = hsecurity(request, client_address)

    # Generate and return response.
    hresponse(request, client_address, client_connection)

    # Close connection.
    client_connection.close()

# Run server.
while True:
    try:
        # Accept client connections.
        client_connection, client_address = server_socket.accept()

        # Get request.
        request = client_connection.recv(1024).decode()

        # Start new thread.
        threading.Thread(target=index, args=(client_connection, request, client_address[0], )).start()

    except KeyboardInterrupt: break
    except: continue

# Close socket and exit.
server_socket.close()

print("Server shutdown successfully.")

logger("INFO", f"Server shutdown.", SERVER_HOST)

exit(0)