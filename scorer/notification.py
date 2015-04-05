from sys import version_info
import logging
import pynotify 

def popUpMessage(title, message):
    logging.debug("Initializing pynotify")
    pynotify.init("Scorer")
    pynotify.Notification(title, message, "dialog-information").show()
