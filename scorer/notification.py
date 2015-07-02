from sys import version_info
from scorer.system import exitApp
import logging
import subprocess as sp

logger = logging.getLogger('scorer.notification')

def popUpMessage(title, message):
    try:
        command = ['notify-send', title, message]
        pipe = sp.call(command)
    except Exception as e:
        logger.debug(e)
        exitApp()
