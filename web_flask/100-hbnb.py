from flask import Flask, render_template
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place

app = Flask(__name__)

@app.teardown_appcontext
def teardown_db(exception):
    storage.close()

@app.route('/hbnb', strict_slashes=False)
def hbnb():
    states = storage.all(State).values()
    cities = storage.all(City).values()
    amenities = storage.all(Amenity).values()
    places = storage.all("Place").values()
    states = [state for state in states if isinstance(state, State)]
    cities = [city for city in cities if isinstance(city, City)]
    amenities = [amenity for amenity in amenities if isinstance(amenity, Amenity)]
    places = [place for place in places if isinstance(place, Place)]

    # Sort the objects by name
    states = sorted(states, key=lambda x: x.name)
    cities = sorted(cities, key=lambda x: x.name)
    amenities = sorted(amenities, key=lambda x: x.name)
    places = sorted(places, key=lambda x: x.name)

    return render_template('100-hbnb.html',
                           states=states,
                           cities=cities,
                           amenities=amenities,
                           places=places)
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
