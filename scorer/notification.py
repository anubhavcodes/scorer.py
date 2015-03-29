from sys import version_info
import logging
if version_info.major is 2:
    import pynotify 
    notifyModule = "pynotify"
if version_info.major is 3:
    try:
        from gi.repository import Notify
        notifyModule = "Notify"
    except ImportError:
        import notify2
        notifyModule = "notify2"

def popUpMessage(title, message):
    if notifyModule is "pynotify":
        logging.debug("Initializing pynotify")
        pynotify.init("Scorer")
        pynotify.Notification(title, message, "dialog-information").show()
    elif notifyModule is "Notify":
        Notify.init("Scorer")
        Notify.Notification.new(title, message, "dialog-information").show()
    else:
        notify2.init("Scorer")
        notify2.Notification(title, message, "dialog-information").show()
