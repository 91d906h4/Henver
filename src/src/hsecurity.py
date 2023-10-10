# hsecurity
# 
#   This module will analysis and filter out illegal requests.

# Import modules.
import json

from src.logger import logger
from urllib.parse import unquote
from src.hconfig import ALLOWED_METHODS, DIR_TRAV_FILTER, CLEAR_URL_PENC, URL_ONLY_ALNUM, \
                        PREVENT_DDOS, MAX_URL_LEN, DDOS_COUNT, DDOS_TIME

# Get banned IP address list.
f = open("./config/ban.json")
ban = json.load(f)
f.close()

def hsecurity(request: list, clinet_ip: str="") -> dict:
    method          = request["method"]
    file            = request["file"]
    file_type       = request["file_type"]
    file_extension  = request["file_extension"]
    query_string    = request["query_string"]
    host            = request["host"]
    user_agent      = request["user_agent"]
    server_errors   = request["server_errors"]

    # Detect the requests that is too long.
    if MAX_URL_LEN == -1: pass
    elif len(file) > MAX_URL_LEN: server_errors = 414

    # Clear URL percent-encoding characters.
    # 
    # This section will remove all space and decode percent-encoded characters.
    # Some URL Encoded Attacks will use something like "%2520" to avoid detection ("%2520" is 
    # the percent-encoding of "%20", and "%20" is the encoding of space), so we keep decoding
    # the URL untill there is no more encoded characters in it.
    if CLEAR_URL_PENC == "enable":
        while "%" in file:
            file = unquote(file)
            file = file.replace(" ", "")

    # Filter out banned IP address.
    # All requests from banned IP will be dropped.
    if clinet_ip in ban["ban_ip"]:
        logger("WARN", f"Access from banned IP address {clinet_ip}.", clinet_ip)
        exit(-1)

    # Filter out illegal HTTP methods.
    # All requests with illegal methods will be dropped.
    if ALLOWED_METHODS == "all": pass
    elif method not in ALLOWED_METHODS:
        logger("WARN", f"Get illegal HTTP method {method}.", clinet_ip)
        exit(-1)

    # Remove all illegal characters in URL.
    if URL_ONLY_ALNUM == "enable":
        clear_file = ""

        for char in file:
            # Using "set" to make sure the search time compelixty is O(1).
            if char in {
                # 0-9.
                "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", \

                # a-z.
                "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", \
                "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", \
                "u", "v", "w", "x", "y", "z", \

                # A-Z.
                "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", \
                "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", \
                "U", "V", "W", "X", "Y", "Z", \

                # Special characters.
                "_", "?", "&", "#", "/", "=", "-", ":", ".", "+", \
                "(", ")"
            }: clear_file += char

        file = clear_file

    # Detect DOS/DDOS attack.
    # if PREVENT_DDOS == "enable": ...

    # Redirect (fix) the queries that tend to do directory traversal.
    if DIR_TRAV_FILTER == "enable":
        while ".." in file: file = file.replace("..", "")
        while "//" in file: file = file.replace("//", "")

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