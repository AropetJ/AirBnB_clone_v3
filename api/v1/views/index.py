#!/usr/bin/python3
"""
A script that returns a json response
"""

from api.v1.views import app_views
from flask import jsonify, request
from models import storage


@app_views.route('/status', methods=['GET'])
def status():
    """A function that returns a JSON status: OK
    """
    if request.method == 'GET':
        response = {"status": "OK"}
        return jsonify(response)


@app_views.route('/api/v1/stats', methods=['GET'])
def stats():
    """A function that retrieves the number of each objects bu type"""
    if request.method == 'GET':
        response = {}
        OBJECTS = {
            "Amenity": "amenities",
            "City": "cities",
            "Place": "places",
            "Review": "reviews",
            "State": "states",
            "User": "users"
        }
        for k, v in OBJECTS.items():
            response[v] = storage.count(k)
        return jsonify(response)
