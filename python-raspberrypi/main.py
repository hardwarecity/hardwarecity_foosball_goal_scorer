#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

# PORTO 17 sempre que recebe um impulso a 1 vindo do arduino (ou do sensor), incrementa o numero de golos da equipa A e manda notificação
# PORTO 27 sempre que recebe um impulso a 1 vindo do arduino (ou do sensor), incrementa o numero de golos da equipa B e manda notificação

from bottle import route, run, template
import json
import requests
import RPi.GPIO as GPIO
from subprocess import call
import time
from neopixel import *

__author__ = 'Hardware City'

# LED strip configuration:
LED_COUNT      = 8      # Number of LED pixels.
LED_PIN_A      = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_PIN_B      = 15      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)

strip_A = None
strip_B = None
try:
    strip_A = Adafruit_NeoPixel(LED_COUNT, LED_PIN_A, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
except Exception as e:
    pass
try:
    strip_B = Adafruit_NeoPixel(LED_COUNT, LED_PIN_B, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
except Exception as e:
    pass
if strip_A is not None:
    try:
        strip_A.begin()
        strip_A.show()
    except Exception as e:
        strip_A = None
if strip_B is not None:
    try:
        strip_B.begin()
        strip_B.show()
    except Exception as e:
        strip_B = None

MAX_GOAL = 5

try:
    GPIO.cleanup()  # clean up GPIO
except:
    pass

url = "https://sweltering-torch-9311.firebaseio.com/results.json"

banner = """
██╗  ██╗ █████╗ ██████╗ ██████╗ ██╗    ██╗ █████╗ ██████╗ ███████╗     ██████╗██╗████████╗██╗   ██╗
██║  ██║██╔══██╗██╔══██╗██╔══██╗██║    ██║██╔══██╗██╔══██╗██╔════╝    ██╔════╝██║╚══██╔══╝╚██╗ ██╔╝
███████║███████║██████╔╝██║  ██║██║ █╗ ██║███████║██████╔╝█████╗      ██║     ██║   ██║    ╚████╔╝
██╔══██║██╔══██║██╔══██╗██║  ██║██║███╗██║██╔══██║██╔══██╗██╔══╝      ██║     ██║   ██║     ╚██╔╝
██║  ██║██║  ██║██║  ██║██████╔╝╚███╔███╔╝██║  ██║██║  ██║███████╗    ╚██████╗██║   ██║      ██║
╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝  ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝     ╚═════╝╚═╝   ╚═╝      ╚═╝

"""  # http://patorjk.com/software/taag/#p=display&f=ANSI%20Shadow&t=HARDWARE%20CITY

print banner

print "GPIO VERSION:", GPIO.VERSION
print "URL:", url

# TODO: Usar Gevent-socketio para notificações em realtime
GPIO.setmode(GPIO.BCM)
#GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # PUD_DOWN enable with 3.3v or 5v | PUD_UP if enable with 0v
#GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # PUD_DOWN enable with 3.3v or 5v | PUD_UP if enable with 0v
GPIO.setup(17, GPIO.IN)  # PUD_DOWN enable with 3.3v or 5v | PUD_UP if enable with 0v
GPIO.setup(27, GPIO.IN)  # PUD_DOWN enable with 3.3v or 5v | PUD_UP if enable with 0v

info = {
    "team_a": {
        "name": "TEAM A",
        "goals": 0,
        "players": [
            {
                "name": "Rui Martins",
                "avatar": "https://www.gravatar.com/avatar/040f98fba4259ac18a53d9a1f6addbe6"
            },
            {
                "name": "Fábio Ferreira",
                "avatar": "https://scontent-mad1-1.xx.fbcdn.net/v/t1.0-9/10411025_906767319351448_6274486805898773858_n.jpg?oh=a1298d61dcd1ac11c21302a3b2109442&oe=57C80780"
            }
        ]
    },
    "team_b": {
        "name": "TEAM B",
        "goals": 0,
        "players": [
            {
                "name": "Francisco Mendes",
                "avatar": "https://scontent.xx.fbcdn.net/v/t1.0-1/s100x100/10001368_694448010598388_898270615_n.jpg?oh=bddb4f1de1c40cf2b4528e971fed0b52&oe=57E2973B"
            },
            {
                "name": "Miguel Almeida",
                "avatar": "https://scontent.xx.fbcdn.net/v/t1.0-1/p100x100/483802_10151544048463659_1974167195_n.jpg?oh=7755df1af27d9254e5900a156afc0446&oe=57C47E20"
            }
        ]
    }
}


def _send_score():
    # Devia de se enviar o INFO directamente?
    data = {
        "team_a": info["team_a"]["goals"],
        "team_b": info["team_b"]["goals"]
    }
    try:
        r = requests.put(url=url, data=json.dumps(data))
    except:
        print "ERROR: Score Connection Fail!"
    # print r.status_code
    # print r.content


def _goal_team_a(pin_number=None):
    # TODO: Usar Gevent-socketio para notificações em realtime
    print "GOAL A!"
    info["team_a"]["goals"] += 1
    _send_score()
    # Mesmo que o IF seguinte seja executado, tem que enviar o score com o MAX_GOAL antes de reiniciar (por casua do codigo do miguel)
    if info["team_a"]["goals"] >= MAX_GOAL:
        info["team_a"]["goals"] = 0
        info["team_b"]["goals"] = 0
        _send_score()
    # call(["python", "blink_A.py"])
    if strip_A is not None:
        a = 1
        while a < 5:
            # Color wipe animations.
            colorWipe(strip_A, Color(255, 0, 0))  # Red wipe
            colorWipe(strip_A, Color(0, 255, 0))  # Blue wipe
            colorWipe(strip_A, Color(0, 0, 255))  # Green wipe
            # Theater chase animations.
            # theaterChase(strip, Color(127, 127, 127))  # White theater chase
            # theaterChase(strip, Color(127,   0,   0))  # Red theater chase
            # theaterChase(strip, Color(  0,   0, 127))  # Blue theater chase
            # Rainbow animations.
            # rainbow(strip)
            # rainbowCycle(strip)
            # theaterChaseRainbow(strip)
            a += 1
        for i in range(LED_COUNT):
            colorWipe(strip_A, Color(0, 0, 0))
        strip_A.show()

def _goal_team_b(pin_number=None):
    # TODO: Usar Gevent-socketio para notificações em realtime
    print "GOAL B!"
    info["team_b"]["goals"] += 1
    _send_score() # Mesmo que o IF seguinte seja executado, tem que enviar o score com o MAX_GOAL antes de reiniciar (por casua do codigo do miguel)
    if info["team_b"]["goals"] >= MAX_GOAL:
        info["team_a"]["goals"] = 0
        info["team_b"]["goals"] = 0
        _send_score()
    # call(["python", "blink_B.py"])
    if strip_B is not None:
        a = 1
        while a < 5:
            # Color wipe animations.
            colorWipe(strip_B, Color(255, 0, 0))  # Red wipe
            colorWipe(strip_B, Color(0, 255, 0))  # Blue wipe
            colorWipe(strip_B, Color(0, 0, 255))  # Green wipe
            # Theater chase animations.
            # theaterChase(strip, Color(127, 127, 127))  # White theater chase
            # theaterChase(strip, Color(127,   0,   0))  # Red theater chase
            # theaterChase(strip, Color(  0,   0, 127))  # Blue theater chase
            # Rainbow animations.
            # rainbow(strip)
            # rainbowCycle(strip)
            # theaterChaseRainbow(strip)
            a += 1
        for i in range(LED_COUNT):
            colorWipe(strip_B, Color(0, 0, 0))
        strip_B.show()

GPIO.add_event_detect(17, GPIO.FALLING, callback=_goal_team_a, bouncetime=3000)
GPIO.add_event_detect(27, GPIO.FALLING, callback=_goal_team_b, bouncetime=3000)
_send_score()


@route('/')
@route('/index.html')
def index():
    return template('<b>{{name_a}}: {{goals_a}}</b><br/><b>{{name_b}}: {{goals_b}}</b>',
                    name_a=info["team_a"]["name"], goals_a=info["team_a"]["goals"],
                    name_b=info["team_b"]["name"], goals_b=info["team_b"]["goals"])

@route('/reset')
def reset():
    info["team_a"]["goals"] = 0
    info["team_b"]["goals"] = 0
    _send_score()


@route('/menu')
def menu():
    return "to do..."


### FUNÇÕES DOS LEDS:


# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)

def theaterChase(strip, color, wait_ms=50, iterations=10):
    """Movie theater light style chaser animation."""
    for j in range(iterations):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, color)
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)

def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)

def rainbow(strip, wait_ms=20, iterations=1):
    """Draw rainbow that fades across all pixels at once."""
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((i+j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)

def rainbowCycle(strip, wait_ms=20, iterations=5):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel(((i * 256 / strip.numPixels()) + j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)

def theaterChaseRainbow(strip, wait_ms=50):
    """Rainbow movie theater light style chaser animation."""
    for j in range(256):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, wheel((i+j) % 255))
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)

######

_goal_team_a()
_goal_team_b()
reset()

run(host='0.0.0.0', port=80)

GPIO.cleanup()  # clean up GPIO
