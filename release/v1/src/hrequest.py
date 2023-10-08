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

        extensions = {
            # PHP.
            "php":  ["PHP", "PHP"],

            # Text.
            "js":   ["TEXT", "JS"],
            "txt":  ["TEXT", "TXT"],
            "css":  ["TEXT", "CSS"],
            "csv":  ["TEXT", "CSV"],
            "htm":  ["TEXT", "HTML"],
            "html": ["TEXT", "HTML"],

            # Application.
            "rar":  ["APP", "RAR"],
            "bin":  ["APP", "BIN"],
            "pdf":  ["APP", "PDF"],
            "xml":  ["APP", "XML"],
            "json": ["APP", "JSON"],

            # Image.
            "png":  ["IMAGE", "PNG"],
            "gif":  ["IMAGE", "GIF"],
            "svg":  ["IMAGE", "SVG"],
            "bmp":  ["IMAGE", "BMP"],
            "ico":  ["IMAGE", "ICO"],
            "jpg":  ["IMAGE", "JPEG"],
            "jpeg": ["IMAGE", "JPEG"],
            "webp": ["IMAGE", "WEBP"],

            # Video.
            "mp4":  ["VIDEO", "MP4"],
            "avi":  ["VIDEO", "AVI"],
            "webm": ["VIDEO", "WEBM"],

            # Audio.
            "mp3":  ["AUDIO", "MP3"],
            "wav":  ["AUDIO", "WAV"],
            "aac":  ["AUDIO", "AAC"],
            "abw":  ["AUDIO", "ABW"],
            "weba": ["AUDIO", "WEBA"],
        }

        if extension in extensions:
            file_type, file_extension = extensions[extension]

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