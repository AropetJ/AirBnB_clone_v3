#!/usr/bin/python3
"""Creates an endpoint that retrieves the number of
each objects by type
"""

from api.v1.views import app_views
from flask import jsonify
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models import storage
from models.user import User


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """Creates a route /status on the object app_views"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
    """ Retrieves the number of each objects by type """
    class_names = ["amenities", "cities", "places", "reviews",
                   "states", "users"]
    classes = [Amenity, City, Place, Review, State, User]

    num_objts = {}
    for i in range(len(classes)):
        num_objts[class_names[i]] = storage.count(classes[i])

    return jsonify(num_objts)
