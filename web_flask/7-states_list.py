#!/usr/bin/python3
"""Flask web application to display a list of states."""
from flask import Flask, render_template
from models import storage
from models.state import State
from os import getenv

app = Flask(__name__)


@app.route('/states_list', strict_slashes=False)
def states_list():
    """Display a HTML page with a list of states."""
    states = storage.all(State).values()
    states = [state for state in states if isinstance(state, State)]
    sorted_states = sorted(states, key=lambda state: state.name)
    return render_template('7-states_list.html', states=sorted_states)


@app.teardown_appcontext
def teardown_db(exception):
    """Remove the current SQLAlchemy Session."""
    storage.close()


if __name__ == "__main__":
    host = '0.0.0.0'
    port = 5000
    app.run(host=host, port=port)