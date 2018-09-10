import json
import scorer.logger as logger
from scorer.system import exitApp

logger = logger.get_logger("config-reader")


def read_json(file_path):
    try:
        with open(file_path.lower()) as json_data:
            data = json.load(json_data)
        return data
    except FileNotFoundError as e:
        logger.error("config file not found!!")
        exitApp()


config_data = read_json("config.json")
NO_LIVE_MATCHES = config_data["NO_LIVE_MATCHES"]
SLEEP_INTERVAL = config_data["SLEEP_INTERVAL"]
WON_STATUS = config_data["WON_STATUS"]
