from sys import version_info
import logging
import pynotify 

def popUpMessage(title, message):
    logging.debug("Initializing pynotify")
    try:
        pynotify.init("Scorer")
        pynotify.Notification(title, message, "dialog-information").show()
    except Exception as e:
        logging.debug("Error initializing pynotify")
        logging.debug(e)
        logging.info("Unable to initialize pynotify: Connection Refused")
        logging.info("Quitting the app")
        exit()
