from flask_security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required
from models import db


# Define models
roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(),
                                 db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime(timezone=True),
                             server_default=db.func.now())
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(
        db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    def GetDict(self):
        # print(self.roles[0].name)
        r=self.roles[0]
        return {
            'id': self.id,
            'email': self.email,
            'password': self.password,
            'role_details': {
                'role_id':r.id,
                'role_name':r.name,
                'role_description':r.description
            },
            'active':self.active,
            'confirmed_at':str(self.confirmed_at),
            'created_on': str(self.created_on),
            'updated_on': str(self.updated_on)
        }


# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
