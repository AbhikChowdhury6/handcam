from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from handcam.extensions import db, login_manager
from flask_login import UserMixin
from datetime import datetime
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from sqlalchemy.dialects.postgresql import JSON

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///alukaraju'

# db = SQLAlchemy(app)
# migrate = Migrate(app, db,compare_type=True)

# manager = Manager(app)
# manager.add_command('db', MigrateCommand)



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    rigName = db.Column(db.String(120), unique=True, nullable=False)
    rigdevicedatas = db.relationship('rigDeviceData', backref='user', lazy=True)
    isAnnotator = db.Column(db.Integer, default=0)
    
    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

'''
1 to Many relationship with user Table.
'''
class rigDeviceData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(256), nullable=False)
    filePath = db.Column(db.Text)
    fileContent = db.Column(JSON)
    contextualTag = db.Column(JSON)
    annotatorTag = db.Column(JSON)
    uploaded_at = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)
    status = db.Column(db.Integer,default=0)
    annotator_status = db.Column(db.Integer,default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)

    def __repr__(self):
        return '<rigDeviceData %r>' % self.filename


