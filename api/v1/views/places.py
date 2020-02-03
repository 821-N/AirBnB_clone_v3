#!/usr/bin/python3
"""
    ~~city~~ place endpoint
"""
from flask import request, jsonify
from api.v1.views import app_views
from models.place import Place
from api.v1.views.general import do
from models import storage


@app_views.route("/cities/<id>/places", methods=["GET", "POST"])
def cities_id_places(id):
    """ list or create """
    place = [c for c in storage.all("City").values() if c.id == id]
    if not place:
        return {"error": "Not found"}, 404

    if request.method == "GET":
        return (jsonify([
            s.to_dict() for s
            in storage.all("Place").values()
            if s.city_id == id
        ]), 200)
    elif request.method == "POST":
        try:
            data = request.get_json()
        except:
            return {"error": "Not found"}, 404
        # make sure city id is valid
        found = False
        for city in storage.all("City").values():
            if city.id == id:
                found = True
                break
        if not found:
            return {"error": "Not found"}, 404
        # make sure user id is valid
        if "user_id" not in data:
            return "Missing user_id", 400
        found = False
        user_id = data["user_id"]
        for user in storage.all("User").values():
            if user.id == user_id:
                found = True
                break
        if not found:
            return {"error": "Not found"}, 404

        if "name" not in data:
            return {"error": "Not found"}, 404
        new = Place()
        for key in data:
            setattr(new, key, data[key])
        setattr(new, "city_id", id)
        new.save()
        return new.to_dict(), 201
    return {"error": "Not found"}, 404


@app_views.route("/places/<id>", methods=["GET", "PUT", "DELETE"])
def places_id(id):
    """ modift """
    return do(Place, id)
