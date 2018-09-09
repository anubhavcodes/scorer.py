import scorer.logger as logger
import pynotify
from scorer.system import exitApp

logger = logger.get_logger('scorer.notification')


def popUpMessage(title, message):
    try:
        command = ['notify-send', title, message]
        pipe = sp.call(command)
        logger.info("pop up message sent!!")
    except Exception as e:
        logger.debug(e)
        exitApp()
