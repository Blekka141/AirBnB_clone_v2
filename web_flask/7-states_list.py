#!/usr/bin/python3
"""
starts a Flask web application
"""

from flask import Flask, render_template
from models import *
from models import storage

app = Flask(__name__)

@app.route('/states_list', strict_slashes=False)
def states_list():
    """
    Display an HTML page with the states listed in alphabetical order.
    """
    try:
        states = storage.all("State").values()
        sorted_states = sorted(states, key=lambda state: state.name)
        return render_template('7-states_list.html', states=sorted_states)
    except Exception as e:
        # Log the error
        app.logger.error(f"Error fetching states: {e}")
        return render_template('7-states_list.html', states=[])

@app.teardown_appcontext
def teardown_db(exception):
    """
    Close the storage on teardown.
    """
    storage.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
