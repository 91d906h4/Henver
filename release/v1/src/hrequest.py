# hrequest
# 
#   This module is used to parse the HTTP requests.

# HTTP header parser.
def hrequest(request: str) -> dict:
    # Split header.
    headers = request.split("\n")

    # Set the default values to prevent if they are not in the header.
    method          = "GET"
    file            = "/"
    file_type       = None
    file_extension  = None
    query_string    = []
    host            = None
    user_agent      = None
    server_errors   = None

    # Parse header.
    for header in headers:
        try:
            if header.startswith(("GET", "POST", "POST", "OPTIONS", "PUT", "DELETE", "TRACE", "PATCH", "LINK", "UNLINK")):
                method, file, _ = header.split()

                if "?" in file:
                    file, query_string = file.split("?", 1)

                    if "&" in query_string:
                        query_string = query_string.split("&")
                    else:
                        query_string = [query_string]

                continue

            # Ignore the fields without colon (:) in header.
            # Every legal fields in HTTP header is expected to be in the following format:
            #   TITLE: VALEU
            elif ":" not in header: continue

            title, content = header.split(":", 1)

            # Clear and format headers.
            title = title.lower()
            content = content.strip()

            if title == "host": host = content
            elif title == "user-agent": user_agent = content

        # Ignore exceptions.
        except: continue

    # Recogenize filetypes.
    if "." in file:
        extension = file.split(".")[-1]
        extension = extension.lower()

        if extension == "php": file_type = "PHP"; file_extension = "PHP"

        # Text.
        elif extension == "js": file_type = "TEXT"; file_extension = "JS"
        elif extension == "txt": file_type = "TEXT"; file_extension = "TXT"
        elif extension == "css": file_type = "TEXT"; file_extension = "CSS"
        elif extension == "csv": file_type = "TEXT"; file_extension = "CSV"
        elif extension in ["html", "htm"]: file_type = "TEXT"; file_extension = "HTML"

        # Application.
        elif extension == "rar": file_type = "APP"; file_extension = "RAR"
        elif extension == "bin": file_type = "APP"; file_extension = "BIN"
        elif extension == "pdf": file_type = "APP"; file_extension = "PDF"
        elif extension == "xml": file_type = "APP"; file_extension = "XML"
        elif extension == "json": file_type = "APP"; file_extension = "JSON"

        # Image.
        elif extension == "png": file_type = "IMAGE"; file_extension = "PNG"
        elif extension == "gif": file_type = "IMAGE"; file_extension = "GIF"
        elif extension == "svg": file_type = "IMAGE"; file_extension = "SVG"
        elif extension == "bmp": file_type = "IMAGE"; file_extension = "BMP"
        elif extension == "ico": file_type = "IMAGE"; file_extension = "ICO"
        elif extension == "webp": file_type = "IMAGE"; file_extension = "WEBP"
        elif extension in ["jpg", "jpeg"]: file_type = "IMAGE"; file_extension = "JPEG"

        # Video.
        elif extension == "mp4": file_type = "VIDEO"; file_extension = "MP4"
        elif extension == "avi": file_type = "VIDEO"; file_extension = "AVI"
        elif extension == "webm": file_type = "VIDEO"; file_extension = "WEBM"

        # Audio.
        elif extension == "MP3": file_type = "AUDIO"; file_extension = "MP3"
        elif extension == "wav": file_type = "AUDIO"; file_extension = "WAV"
        elif extension == "aac": file_type = "AUDIO"; file_extension = "ACC"
        elif extension == "abw": file_type = "AUDIO"; file_extension = "ABW"
        elif extension == "weba": file_type = "AUDIO"; file_extension = "WEBA"

    return {
        "method":           method,
        "file":             file,
        "file_type":        file_type,
        "file_extension":   file_extension,
        "query_string":     query_string,
        "host":             host,
        "user_agent":       user_agent,
        "server_errors":    server_errors,
    }