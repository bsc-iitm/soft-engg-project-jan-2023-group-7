from flask import Flask
from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy
from models.queries import Query
from models.faqs import FAQ

# Create app
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'super-secret'
app.config['SECURITY_PASSWORD_SALT'] = 'HelloWorld'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'

# sqlite
db = SQLAlchemy(app, metadata=MetaData())

# Query and FaQ Intializer
for i in range(1, 11):
    d = Query(issue='issue'+str(i*100+i),
              solution='solution'+str(i*100+i),
              created_by='created_by'+str(i*100+i),
              answered_by='answered_by'+str(i*100+i),
              upvotes='upvotes'+str(i*100+i))
    db.session.add(d)
    db.session.commit()

    d = FAQ(issue='issue'+str(i*100+i),
              solution='solution'+str(i*100+i),
            #   created_by='created_by'+(i*100+i),
            #   answered_by='answered_by'+(i*100+i),
              upvotes='upvotes'+str(i*100+i))
    db.session.add(d)
    db.session.commit()



