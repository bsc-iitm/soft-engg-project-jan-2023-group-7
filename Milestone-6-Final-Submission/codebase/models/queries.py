from models import db


class Query(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    issue = db.Column(db.String(20), unique=True)
    solution = db.Column(db.String(20))
    created_by = db.Column(db.Integer())
    answered_by = db.Column(db.Integer())
    upvotes = db.Column(db.Integer())
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(
        db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def GetDict(self):
        return {
            'id': self.id,
            'issue': self.issue,
            'solution': self.solution,
            'created_by': self.created_by,
            'answered_by': self.answered_by,
            'upvotes': self.upvotes,
            'created_on': str(self.created_on),
            'updated_on': str(self.updated_on)
        }
