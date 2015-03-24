#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
from gi.repository import Notify
from time import sleep


def sendmessage(title, message):
  Notify.init("Scorer")
  scorer = Notify.Notification.new(title, message, "dialog-information")
  scorer.show()
  return


url = "http://static.cricinfo.com/rss/livescores.xml"
match = 0
score = ""
interrupted=False

print("Fetching matches..")
while True:
  try:
    r = requests.get(url)
    while r.status_code is not 200:
      sleep(2)
      r = requests.get(url)
    soup = BeautifulSoup(r.text)
    data = soup.find_all("description")
    if match == 0:
      print("Matches available:")
      counter = 1
      for game in data[1:]:
        print(counter, game.text)
        counter += 1
      match = int(input("Enter your choice: "))
      interrupted=False
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
      match = 0
      interrupted=True
