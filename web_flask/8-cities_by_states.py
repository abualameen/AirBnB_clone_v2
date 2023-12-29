# Import necessary modules
from flask import Flask, render_template
from models import storage
from models.state import State
from models.city import City

# Initialize Flask application
app = Flask(__name__)


@app.teardown_appcontext
def teardown_db(exception):
    """Close the current SQLAlchemy session."""
    storage.close()


@app.route('/cities_by_states', strict_slashes=False)
def cities_by_states():
    """Display states and cities."""
    states = storage.all(State).values()
    cities = storage.all(City).values()
    states = [state for state in states if isinstance(state, State)]
    cities = [city for city in cities if isinstance(city, City)]
    return render_template(
                            '8-cities_by_states.html',
                            states=states,
                            cities=cities)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
