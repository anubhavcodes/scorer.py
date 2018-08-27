import logging

import pynotify

from scorer.system import exitApp

logger = logging.getLogger('scorer.notification')


def popUpMessage(title, message):
    logger.info("Initializing pynotify")
    try:
        pynotify.init("Scorer")
        pynotify.Notification(title, message, "dialog-information").show()
    except Exception as e:
        logger.error("Error initializing pynotify")
        logger.debug(e)
        logger.info("Unable to initialize pynotify: Connection Refused")
        logger.info("Quitting the app")
        exitApp()
