from models import db
from flask_restful import Resource
from flask import request
from models.queries import Query


def GetQuery(id):
    d = Query.query.filter_by(id=id).first()
    return d


def GetAllQuerys():
    d = Query.query.all()
    return d


def GetSimilarQuerys(text):
    d = Query.query.all(Query.issue.like('%'+text+'%'))
    return d

# def GetCardsbyQuery(id):
#     d=Cards.query.filter_by(query_id=id).all()
#     return d

# def GetScoresbyQuery(id):
#     d=Scores.query.filter_by(query_id=id).all()
#     return d


class Query_Search(Resource):
    def get(self, text):
        g = GetSimilarQuerys(text)
        a = []
        for x in g:
            a.append(x.GetDict())
        return a


class Query_Others(Resource):
    def get(self, query_id):
        g = GetQuery(query_id)
        return g.GetDict(), 200

    def delete(self, query_id):
        g = GetQuery(query_id)
        if g == None:
            return {"Error": "Not Found"}, 404
        db.session.delete(g)
        db.session.commit()
        return g.GetDict(), 200

    def put(self, query_id):
        g = GetQuery(query_id)
        if request.content_type == 'application/json':
            issue = request.json['issue']
            solution = request.json['solution']
            created_by = request.json['created_by']
            answered_by = request.json['answered_by']
            upvotes = 0
        else:
            issue = request.form['issue']
            solution = request.form['solution']
            created_by = request.form['created_by']
            answered_by = request.form['answered_by']
            upvotes = 0
        if g == None:
            return {"Error": "NotFound"}, 404
        if issue == None:
            return {"Error": "Incorecct Parameter"}, 400
        g.issue = issue
        g.solution = solution
        g.created_by = created_by
        g.answered_by = answered_by
        g.upvotes = upvotes
        db.session.commit()
        g = GetQuery(query_id)
        return g.GetDict(), 200


def creteQuery(issue, solution, created_by, answered_by, upvotes):
    d = Query(
        issue=issue,
        solution=solution,
        created_by=created_by,
        answered_by=answered_by,
        upvotes=upvotes,
    )
    db.session.add(d)
    db.session.commit()
    return d


class Query_Create(Resource):
    def post(self):
        if request.content_type == 'application/json':
            issue = request.json['issue']
            solution = request.json['solution']
            created_by = request.json['created_by']
            answered_by = request.json['answered_by']
            upvotes = 0
        else:
            issue = request.form['issue']
            solution = request.form['solution']
            created_by = request.form['created_by']
            answered_by = request.form['answered_by']
            upvotes = 0
        if issue == None:
            return {"Error": "Incorecct Parameter"}, 400
        d = creteQuery(issue, solution, created_by, answered_by, upvotes)
        return d.GetDict(), 201

    def get(self):
        g = GetAllQuerys()
        a = []
        for x in g:
            a.append(x.GetDict())
        return a
