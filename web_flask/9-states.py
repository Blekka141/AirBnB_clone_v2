#!/usr/bin/python3
from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)

@app.route('/states', strict_slashes=False)
@app.route('/states/<id>', strict_slashes=False)
def states(id=None):
    states = storage.all(State)
    if id:
        state = states.get(f"State.{id}")
        return render_template('9-states.html', state=state)
    else:
        return render_template('9-states.html', states=sorted(states.values(), key=lambda state: state.name))

@app.teardown_appcontext
def teardown(exception):
    storage.close()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
