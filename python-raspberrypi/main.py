#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

# PORTO 20 sempre que recebe um impulso a 1 vindo do arduino (ou do sensor), incrementa o numero de golos da equipa A e manda notificação
# PORTO 21 sempre que recebe um impulso a 1 vindo do arduino (ou do sensor), incrementa o numero de golos da equipa B e manda notificação

from bottle import route, run, template
import json
import requests
import RPi.GPIO as GPIO
__author__ = 'Rui Martins'

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
GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # or PUD_UP ?
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # or PUD_UP ?

info = {
    "team_a": {
        "name": "TEAM A",
        "goals": 0,
        "players": [
            {
                "name": "Rui Martins"
            },
            {
                "name": "Fábio Ferreira"
            }
        ]
    },
    "team_b": {
        "name": "TEAM B",
        "goals": 0,
        "players": [
            {
                "name": "Francisco Mendes"
            },
            {
                "name": "Miguel Almeida"
            }
        ]
    }
}


def _send_score():
    # Devia de se enviar o INFO derectamente
    data = {
        "team_a": info["team_a"]["goals"],
        "team_b": info["team_b"]["goals"]
    }
    r = requests.put(url=url, data=json.dumps(data))
    # print r.status_code
    # print r.content


def _goal_team_a(pin_number):
    # TODO: Usar Gevent-socketio para notificações em realtime
    print "GOAL A!"
    info["team_a"]["goals"] += 1
    _send_score()


def _goal_team_b(pin_number):
    # TODO: Usar Gevent-socketio para notificações em realtime
    print "GOAL B!"
    info["team_b"]["goals"] += 1
    _send_score()


GPIO.add_event_detect(20, GPIO.FALLING, callback=_goal_team_a, bouncetime=300)
GPIO.add_event_detect(21, GPIO.FALLING, callback=_goal_team_b, bouncetime=300)
_send_score()

# TODO: ...

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

run(host='0.0.0.0', port=80)

# TODO: ...

GPIO.cleanup()  # clean up GPIO
