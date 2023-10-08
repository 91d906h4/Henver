# hresponse
# 
#   This module is used to generate the HTTP response and send them to client.

# Import modules.
import subprocess

from src.logger import logger
from src.hexception import URITooLongError
from src.hconfig import DEFAULT_PAGE, ENCODING, APPEND_SER_NAME, PHP_CGI, \
                        E400_PAGE, E403_PAGE, E404_PAGE, E409_PAGE, E414_PAGE, \
                        E500_PAGE, E502_PAGE, E503_PAGE

def hresponse(request: dict, clinet_ip: str, client_connection: object) -> None:
    file            = request["file"]
    file_type       = request["file_type"]
    file_extension  = request["file_extension"]
    query_string    = request["query_string"]
    server_errors   = request["server_errors"]

    # Set the default response code and content.
    code = 200
    content = ""

    # Response headers.
    r_code = {
        # 2XX
        200: "200 OK",

        # 4XX
        400: "400 Bad Request",
        403: "403 Forbidden",
        404: "404 Not Found",
        409: "409 Too Many Requests",
        414: "414 URI Too Long",

        # 5XX
        500: "500 Internal Server Error",
        502: "502 Bad Gateway",
        503: "503 Service Unavailable",
    }
    r_content_type = {
        # PHP.
        "PHP": "text/html",

        # Text.
        "JS": "text/javascript",
        "TXT": "text/plain",
        "CSS": "text/css",
        "CSV": "text/csv",
        "HTML": "text/html",

        # Application.
        "RAR": "application/vnd.rar",
        "BIN": "application/octet-stream",
        "PDF": "application/pdf",
        "XML": "application/xml",
        "JSON": "application/json",

        # Image.
        "PNG": "image/png",
        "GIF": "image/gif",
        "SVG": "image/svg+xml",
        "BMP": "image/bmp",
        "ICO": "image/vnd.microsoft.icon",
        "WEBP": "image/webp",
        "JPEG": "image/jpeg",

        # Video.
        "MP4": "video/mp4",
        "AVI": "video/x-msvideo",
        "WEBM": "video/webm",

        # Audio.
        "MP3": "audio/mpeg",
        "WAV": "audio/wav",
        "AAC": "audio/aac",
        "ABW": "audio/x-abiword",
        "WEBA": "audio/weba",
    }

    try:
        # Raise server errors.
        if server_errors == 414: raise URITooLongError("Get request longer than max_url_len.")

        # Request for index file.
        if file == "/":
            content = open(f"./public/{DEFAULT_PAGE}", encoding=ENCODING).read()

        # Request fot PHP files.
        elif file_type == "PHP":
            # Try to open file to check if file exists.
            open("./public/" + file, encoding=ENCODING).close()

            # The other (batter) solution is to use socket and FastCGI to implement
            # the connections between client and PHP-CGI.
            # If we use subprocess to run the PHP files, many features such as $_SERVER,
            # $_SESSION, etc. will no longer be useful.
            # 
            # https://github.com/Terr/pyfcgiclient/tree/master

            command = [PHP_CGI, "./public" + file] + query_string

            # Execute PHP-CGI and get the result from CGI.
            content = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=False)
            content = content.stdout.decode(encoding=ENCODING)

        # Request fot media files.
        elif file_type in ["IMAGE", "VIDEO", "AUDIO"]:
            content = open("./public/" + file, mode="rb").read()
            logger("INFO", f"Request for file '{file}'.", clinet_ip)

        # Request for other files.
        else:
            content = open("./public/" + file, encoding=ENCODING).read()
            logger("INFO", f"Request for file '{file}'.", clinet_ip)

    # Exceptions.
    except FileNotFoundError as e: code = 404; logger("INFO", str(e), clinet_ip)
    except PermissionError as e: code = 403; logger("WARN", str(e), clinet_ip)
    except URITooLongError as e: code = 414; logger("WARN", str(e), clinet_ip)
    except Exception as e: code = 500; logger("ERROR", str(e), clinet_ip)

    # Error page content.
    if code != 200:
        error_page = {
            # 4XX
            400: E400_PAGE,
            403: E403_PAGE,
            404: E404_PAGE,
            409: E409_PAGE,
            414: E414_PAGE,

            # 5XX
            500: E500_PAGE,
            502: E502_PAGE,
            503: E503_PAGE,
        }

        content = open("./public/" + error_page[code], encoding=ENCODING).read()

    # Encode the content if it is not a media file.
    if file_type not in ["IMAGE", "VIDEO", "AUDIO"]:
        content = content.encode()

    # Sned HTTP response.

    # Status Code.
    client_connection.send(f"HTTP/1.1 {r_code[code]}\r\n".encode())

    # Server name.
    if APPEND_SER_NAME == "enable":
        client_connection.send(f"Server: Henver\r\n".encode())

    # PHP file.
    # PHP-CGI will generate the header, so we just return everything.
    if file_type == "PHP" and code == 200:
        client_connection.send(content)
        return

    # Content type.
    if code != 200:
        # If HTTP status code is not 200, then return static error pages.
        client_connection.send(f"Content-Type: text/html\r\n".encode())
    elif file_extension in r_content_type:
        client_connection.send(f"Content-Type: {r_content_type[file_extension]}\r\n".encode())

    # Append a newline between header and contents.
    client_connection.send(f"\r\n".encode())

    # Contents.
    client_connection.send(content)