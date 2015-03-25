from sys import version_info
import requests
from bs4 import BeautifulSoup
if version_info.major is 2:
    import pynotify
    notifyModule = "pynotify"
if version_info.major is 3:
    try:
        from gi.Repository import Notify
        notifyModule = "Notify"
    except ImportError:
        import notify2
        notifyModule = "notify2"
from time import sleep


def sendmessage(title, message):
    if notifyModule is "pynotify":
        pynotify.init("Scorer")
        pynotify.Notification(title, message, "dialog-information").show()
    elif notifyModule is "Notify":
        Notify.init("Scorer")
        Notify.Notification.new(title, message, "dialog-information").show()
    else:
        notify2.init("Scorer")
        notify2.Notification(title, message, "dialog-information").show()


url, match, score, interrupted = "http://static.cricinfo.com/rss/livescores.xml", 0, "", False

print("Fetching matches..")
while True:
    try:
        r = requests.get(url)
        while r.status_code is not 200:
            sleep(2)
            r = requests.get(url)
        data = BeautifulSoup(r.text).find_all("description")
        if not match:
            print("Matches available:")
            for counter, game in enumerate(data[1:], 1):
                print(counter, game.text)
            match = int(input("Enter your choice: "))
            interrupted = False
        newscore = data[match].text
        if newscore != score:
            score = newscore
            sendmessage("Score", score)
        sleep(15)

    except KeyboardInterrupt:
        if interrupted:
            print("Bye bye")
            break
        else:
            print("Press Ctrl+C again to quit")
            match, interrupted = 0, True
