import pyttsx

def voice(message,_rate=-50,_volume=0):
    engine = pyttsx.init()
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate+_rate)
    volume = engine.getProperty('volume')
    engine.setProperty('volume', volume+_volume)
    engine.say(message)
    engine.runAndWait()
