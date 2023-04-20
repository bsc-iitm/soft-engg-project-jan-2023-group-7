from models import db
from flask_restful import Resource
from flask import request
from models.users import User, Role, user_datastore


def GetUser(id):
    d = User.query.filter_by(id=id).first()
    return d


def GetAllUsers():
    d = User.query.all()
    return d

# def GetCardsbyUser(id):
#     d=Cards.query.filter_by(client_id=id).all()
#     return d

# def GetScoresbyUser(id):
#     d=Scores.query.filter_by(client_id=id).all()
#     return d


class User_Others(Resource):
    def get(self, client_id):
        g = GetUser(client_id)
        return g.GetDict(), 200

    def delete(self, client_id):
        g = GetUser(client_id)
        if g == None:
            return {"Error": "Not Found"}, 404
        db.session.delete(g)
        db.session.commit()
        return g.GetDict(), 200

    def put(self, client_id):
        g = GetUser(client_id)
        if request.content_type == 'application/json':
            email = request.json['email']
            password = request.json['password']
            role = request.json['role']
        else:
            email = request.form['email']
            password = request.form['password']
            role = request.form['role']
        if email == None:
            return {"Error": "Incorrect Parameter"}, 400
        if g == None:
            return {"Error": "NotFound"}, 404
        g.email = email
        g.password = password
        g.role = role
        g = GetUser(client_id)
        return g.GetDict(), 200


def createUser(e, p, r):
    user_datastore.create_user(
        email=e, password=p, active=True)
    user_datastore.add_role_to_user(User.query.filter_by(
        email=e).first(), Role.query.filter_by(name=r).first())
    db.session.commit()
    return User.query.filter_by(
        email=e).first()


class User_Create(Resource):
    def post(self):
        if request.content_type == 'application/json':
            email = request.json['email']
            password = request.json['password']
            role = request.json['role']
        else:
            email = request.form['email']
            password = request.form['password']
            role = request.form['role']
        if email == None:
            return {"Error": "Incorrect Parameter"}, 400
        d = createUser(email, password, role)
        return d.GetDict(), 201

    def get(self):
        g = GetAllUsers()
        a = []
        for x in g:
            a.append(x.GetDict())
        return a
