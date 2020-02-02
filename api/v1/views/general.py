from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
"""
    general stuff
"""


def get_obj(obj):
    """ get """
    if obj:
        return (jsonify(obj.to_dict()), 200)
        return {}
    return abort(404)


def put_obj(obj):
    """ put """
    if not obj:
        abort(404)
    try:
        data = request.get_json()
    except:
        return "Not a JSON", 400
    for key in data:
        if key not in ("id", "created_at", "updated_at"):
            if not(type(obj).__name__ == "User" and key in "email"):
                setattr(obj, key, data[key])
    storage.save()
    return (jsonify(obj.to_dict()), 200)


def delete_obj(obj):
    """ delete """
    if not obj:
        abort(404)
    storage.delete(obj)
    storage.save()
    return (jsonify(dict()), 200)


methods = {
    "GET": get_obj,
    "PUT": put_obj,
    "DELETE": delete_obj,
}


def do(cls, id=None):
    """ general """
    if id:
        for obj in storage.all(cls).values():
            if obj.id == id and request.method in methods:
                return methods[request.method](obj)
    elif request.method == "GET":
        return (jsonify([
            s.to_dict() for s
            in storage.all(cls).values()
        ]), 200)
    elif request.method == "POST":
        try:
            data = request.get_json()
        except:
            return "Not a JSON", 400
        if not data or "name" not in data:
            return "Missing name", 400
        new = cls()
        for key in data:
            setattr(new, key, data[key])
        new.save()
        return (jsonify(new.to_dict()), 201)
    return {"error": "Not found"}, 404
