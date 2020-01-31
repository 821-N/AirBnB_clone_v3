#!/usr/bin/python3
"""
    ~~state~~ user endpoint
"""
from api.v1.views import app_views
from models.user import User
from api.v1.views.general import do


@app_views.route("/users", methods=["GET", "POST"])
def users():
    """ list or create """
    if request.method == "GET":
        # This outputs passwords wwwwww
        return (jsonify([
            s.to_dict() for s
            in storage.all(cls).values()
        ]), 200)
    elif request.method == "POST":
        try:
            data = request.get_json()
        except:
            abort(400, "Not a JSON")
        if not data or "email" not in data:
            abort(400, "Missing email")
        if not data or "password" not in data:
            abort(400, "Missing password")
        new = cls()
        for key in data:
            setattr(new, key, data[key])
        new.save()
        return (jsonify(new.to_dict()), 201)
    return {"error": "Not found"}, 404State
    return do(User)


@app_views.route("/states/<id>", methods=["GET", "PUT", "DELETE"])
def users_id(id):
    """ modify """
    return do(User, id)
