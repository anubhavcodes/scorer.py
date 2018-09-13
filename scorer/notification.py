import logging

import notify2

from scorer.system import exitApp

logger = logging.getLogger('scorer.notification')


def popUpMessage(title, message):
    logger.info("Initializing notify2")
    try:
        notify2.init("Scorer")
        notify2.Notification(title, message, "dialog-information").show()
    except Exception as e:
        logger.error("Error initializing notify2")
        logger.debug(e)
        logger.info("Unable to initialize notify2: Connection Refused")
        logger.info("Quitting the app")
        exitApp()
