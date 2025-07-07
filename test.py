from bottle import Bottle, run
from controllers import init_controllers

app = Bottle()
init_controllers(app)

if __name__ == "__main__":
    run(app, host="0.0.0.0", port=8080, debug=True, reloader=True)
