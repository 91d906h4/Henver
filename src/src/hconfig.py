# Import modules
import configparser

# Read conf file.
main_conf = configparser.ConfigParser()
main_conf.read("./config/main.ini")

# Const settings.
# [Server]
SERVER_HOST     = str(main_conf["server"]["host"])
SERVER_PORT     = int(main_conf["server"]["port"])
PHP_CGI         = str(main_conf["server"]["php_cgi"])
DEFAULT_PAGE    = str(main_conf["server"]["default_page"])
DEFAULT_PAGE    = str(main_conf["server"]["default_page"])
E400_PAGE       = str(main_conf["server"]["e400_page"])
E403_PAGE       = str(main_conf["server"]["e403_page"])
E404_PAGE       = str(main_conf["server"]["e404_page"])
E409_PAGE       = str(main_conf["server"]["e409_page"])
E414_PAGE       = str(main_conf["server"]["e414_page"])
E500_PAGE       = str(main_conf["server"]["e500_page"])
E502_PAGE       = str(main_conf["server"]["e502_page"])
E503_PAGE       = str(main_conf["server"]["e503_page"])
APPEND_SER_NAME = str(main_conf["server"]["append_ser_name"])

# [Sys]
ENCODING        = str(main_conf["sys"]["encoding"])
LOGGING         = str(main_conf["sys"]["logging"])
LOG_PATH        = str(main_conf["sys"]["log_path"])
LOG_LEVEL       = str(main_conf["sys"]["log_level"]).upper()

# [Security]
ALLOWED_METHODS = str(main_conf["security"]["allowed_methods"]).upper()
DIR_TRAV_FILTER = str(main_conf["security"]["dir_trav_filter"])
CLEAR_URL_PENC  = str(main_conf["security"]["clear_url_penc"])
URL_ONLY_ALNUM  = str(main_conf["security"]["url_only_alnum"])
PREVENT_DDOS    = str(main_conf["security"]["prevent_ddos"])
DDOS_COUNT      = str(main_conf["security"]["ddos_count"])
DDOS_TIME       = str(main_conf["security"]["ddos_time"])
MAX_URL_LEN     = int(main_conf["security"]["max_url_len"])

# [Version]
SERVER_VERSION  = "v1.5.0"