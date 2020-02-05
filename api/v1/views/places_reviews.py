#!/usr/bin/python3
"""
    ~~~~city~~ place~~ review endpoint
"""
from flask import request, jsonify
from api.v1.views import app_views
from models.review import Review
from api.v1.views.general import do
from models import storage


@app_views.route("/places/<id>/reviews", methods=["GET", "POST"])
def places_id_reviews(id):
    """ list or create """
    review = [c for c in storage.all("Place").values() if c.id == id]
    if not review:
        return {"error": "Not found"}, 404

    if request.method == "GET":
        return (jsonify([
            s.to_dict() for s
            in storage.all("Review").values()
            if s.place_id == id
        ]), 200)
    elif request.method == "POST":
        # make sure place id is valid
        found = False
        for place in storage.all("Place").values():
            if place.id == id:
                found = True
                break
        if not found:
            return {"error": "Not found"}, 404
        # check JSON
        try:
            data = request.get_json()
        except:
            return "Not a JSON", 400
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
        # check text
        if "text" not in data:
            return "Missing text", 400
        # create object
        new = Review()
        for key in data:
            setattr(new, key, data[key])
        setattr(new, "place_id", id)
        new.save()
        return new.to_dict(), 201
    return {"error": "Not found"}, 404


@app_views.route("/reviews/<id>", methods=["GET", "PUT", "DELETE"])
def reviews_id(id):
    """ modift """
    return do(Review, id, ("user_id", "place_id"))
