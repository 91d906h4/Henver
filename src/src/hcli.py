# hcli
# 
#   This module is the CLI tool for Henver.

# Import Modules.
import sys

from src.hconfig import SERVER_HOST, SERVER_PORT, SERVER_VERSION

def hcli() -> list:
    global SERVER_HOST, SERVER_PORT, SERVER_VERSION

    # Set the default value.
    quiet_start = False

    # Read server settings from command line.
    for param in sys.argv:
        # Server host.
        if param.startswith("--host="): SERVER_HOST = str(param[7:])

        # Server port.
        elif param.startswith("--port="): SERVER_PORT = int(param[7:])

        # Quiet start.
        elif param in {"--quiet-start", "-ss"}: quiet_start = True

        # Show version.
        elif param in {"--version", "-v"}:
            print(f"The current version is Henver {SERVER_VERSION}.")
            print(f"")

            exit(0)

        # Help message.
        elif param in {"--help", "-h"}:
            print(f"Thank you for using Henver HTTP Server {SERVER_VERSION}.")
            print(f"")
            print(f"Options:")
            print(f"")
            print(f"\t--help (-h)\n\t    Show this help message.")
            print(f"\t--host\n\t    Useing comman '--host=XXX.XXX.XXX.XXX' to specify the server host. (Default: '127.0.0.1')")
            print(f"\t--port\n\t    Useing comman '--port=XXX' to specify the port for server. (Defualt: '80')")
            print(f"\t--quiet-start (-ss)\n\t    Start the server without open website in browser. (Defualt: 'False')")
            print(f"\t--version (-v)\n\t    Show the version of server.")
            print(f"")

            exit(0)

    return [
        SERVER_HOST,
        SERVER_PORT,
        quiet_start,
    ]