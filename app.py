from flask import Flask, json, abort, Response, request
import requests
import threading

app = Flask(__name__)
app.config["defaultExpiration"] = 0

@app.post('/on')
def on():
    print("INFO: Client requested ON state...")
    try:
        r = requests.post('http://wil-emitter-node/on')
    except Exception as e:
        print("ERROR: %s..." % e)
        abort(400)
    if app.config["defaultExpiration"] > 0:
        print("INFO: Default expiration is %i..." % app.config["defaultExpiration"])
        timer = threading.Timer(app.config["defaultExpiration"], off)
        timer.start()
    return Response(
        r.text,
        status=r.status_code,
    )

@app.post('/off')
def off():
    print("INFO: Client requested OFF state...")
    try:
        r = requests.post('http://wil-emitter-node/off')
    except Exception as e:
        print("ERROR: %s..." % e)
        abort(400)
    return Response(
        r.text,
        status=r.status_code,
    )

@app.get('/state')
def state():
    try:
        r = requests.get('http://wil-emitter-node/state')
    except Exception as e:
        print("ERROR: %s..." % e)
        abort(400)
    return Response(
        r.text,
        status=r.status_code,
    )

@app.post('/exp')
def expiration():
    if request.args is None or len(request.args) <= 0:
        abort(400)
    else:
        try:
            app.config["defaultExpiration"] = int(request.args["seconds"])
        except Exception as e:
            print("ERROR: %s..." % e)
            abort(400)    
    print("INFO: Client requested expiration in %i seconds..." % app.config["defaultExpiration"])
    return Response(
        "Turning off in %i seconds." % app.config["defaultExpiration"],
        status=200,
    )

@app.post('/reboot')
def reboot():
    if request.args is None or len(request.args) <= 0:
        abort(400)
    else:
        target = None
        try:
            target = request.args["target"]
            print("INFO: Client requested reboot of target '%s'..." % target)
            if target == "server":
                print("INFO: I would reboot the server...")
                return "Rebooting target '%s'." % target
            elif target == "nodes":
                try:
                    r = requests.post('http://wil-emitter-node/reboot')
                except Exception as e:
                    print("ERROR: %s..." % e)
                    abort(400)
                return Response(
                    r.text,
                    status=r.status_code,
                )
            else:
                raise Exception("Client requested invalid target")
        except Exception as e:
            print("ERROR: %s..." % e)
            abort(400)
    