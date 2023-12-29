#!/usr/bin/python3
"""
Script that starts a Flask web application
"""
from flask import Flask, render_template
from models import storage
from models.state import State
from models.city import City

app = Flask(__name__)


@app.teardown_appcontext
def teardown_db(exception):
    """Remove the current SQLAlchemy Session"""
    storage.close()


@app.route('/states', strict_slashes=False)
def states_list():
    """Display a HTML page with a list of states."""
    states = storage.all(State).values()
    states = [state for state in states if isinstance(state, State)]
    sorted_states = sorted(states, key=lambda state: state.name)
    return render_template('7-states_list.html', states=sorted_states)


@app.route('/states/<id>', strict_slashes=False)
def states_cities_list(id):
    """Display a HTML page with the list of cities of a State"""
    states = storage.all(State).values()
    for state in states:
        if id == state.id:
            cities = state.cities
            return render_template('9-states.html', state=state, cities=cities)
    return render_template('9-states.html', state=None)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
