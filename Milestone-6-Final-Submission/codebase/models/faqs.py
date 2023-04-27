from models import db


class FAQ(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    issue = db.Column(db.String(20), unique=True)
    solution = db.Column(db.String(20))
    upvotes = db.Column(db.Integer())
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(
        db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def GetDict(self):
        return {
            'id': self.id,
            'issue': self.issue,
            'solution': self.solution,
            'upvotes': self.upvotes,
            'created_on': str(self.created_on),
            'updated_on': str(self.updated_on)
        }
