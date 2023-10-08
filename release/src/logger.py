# logger
# 
#   This module is used to log the server events.

# Server log format:
#
#   [LABEL] YYYY/MM/DD HH:MM:SS IP  LOG
# 
# LABEL:
# 
#   INFO
#       A log level for outputting application information during production operation.
#       It includes access logs and statistical logs.
#       Usually, this level of log is generated by the framework rather than individual applications because it closely relates to operational monitoring.
#       Design the output content to avoid excessive log file size.
# 
#   WARN
#       Indicates an event that does not immediately impact the application but could become a problem affecting its continued operation if left unattended.
#       It's advisable to monitor, but it's not as critical as the ERROR level.
#       Usually, this level of log is generated by the framework rather than individual applications because it closely relates to operational monitoring.
# 
#   ERROR
#       Indicates a problem that affects the continued operation of the application.
#       Monitoring is necessary, but the urgency for reporting and response is not as high as FATAL level.
#       Usually, this level of log is generated by the framework rather than individual applications because it closely relates to operational monitoring.
# 
#   FITAL
#       Indicates a critical issue that makes the continued operation of the application impossible.
#       Monitoring is essential, and immediate reporting and action are required.
#       Usually, this level of log is generated by the framework rather than individual applications because it closely relates to operational monitoring.

# Import modules.
from datetime import datetime
from src.hconfig import LOGGING, LOG_PATH, LOG_LEVEL, ENCODING

levels = {
    "INFO": 0,
    "WARN": 1,
    "ERROR": 2,
    "FITAL": 3
}

def logger(label: str, log: str, ip: str="0.0.0.0") -> None:
    # Return if logging is disabled.
    if LOGGING == "disable": return

    # Return if the event level if lower than setting.
    if levels[label] < levels[LOG_LEVEL]: return

    try:
        log = log.replace("\r\n", "").replace("\n", " ")
        now = datetime.now().strftime("%Y/%m/%d %H:%M:%S")

        f = open("." + LOG_PATH, mode="a", encoding=ENCODING)
        f.write(f"[{label}]\t{now} {ip}\t{log}\n")
        f.close()

    # Create log file while not found.
    except FileNotFoundError:
        try:
            f = open("." + LOG_PATH, mode="w")
            f.write("")
            f.close()

        except Exception as e:
            print(f"[Log] Cannot create log file. Error message: " + str(e))

    except Exception as e:
        print(f"[Log] Cannot write log file. Error message: " + str(e))