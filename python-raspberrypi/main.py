from bottle import route, run, template
import RPi.GPIO as GPIO
__author__ = 'Rui Martins'

# TODO: Usar Gevent-socketio para notificações em realtime
GPIO.setmode(GPIO.BCM)
GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # or PUD_DOWN ?
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # or PUD_DOWN ?

info = {
    "team_a": {
        "name": "TEAM A",
        "goals": 0
    },
    "team_a": {
        "name": "TEAM B",
        "goals": 0
    }
}


def _goal_team_a():
    # TODO: Usar Gevent-socketio para notificações em realtime
    print "GOAL A!"
    info["team_a"]["goals"] += 1


def _goal_team_b():
    # TODO: Usar Gevent-socketio para notificações em realtime
    print "GOAL B!"
    info["team_b"]["goals"] += 1


GPIO.add_event_detect(20, GPIO.FALLING, callback=_goal_team_a, bouncetime=300)
GPIO.add_event_detect(21, GPIO.FALLING, callback=_goal_team_b, bouncetime=300)

# TODO: ...

@route('/')
@route('/index.html')
def index():
    return template('<b>{{name_a}}: {{goals_a}}</b><br/><b>{{name_b}}: {{goals_b}}</b>',
                    name_a=info["team_a"]["name"], goals_a=info["team_a"]["goals"],
                    name_b=info["team_b"]["name"], goals_b=info["team_b"]["goals"])

run(host='localhost', port=8080)

# TODO: ...

GPIO.cleanup()  # clean up GPIO
