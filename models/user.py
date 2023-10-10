# models/user.py
from db import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    first_name = db.Column(db.String(120))
    last_name = db.Column(db.String(120))
    state = db.Column(db.String(120))
    county = db.Column(db.String(120))
    display_name = db.Column(db.String(240))  # firstname + lastname

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @staticmethod
    def hash_password(password):
        return generate_password_hash(password)
    
    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()
        
    google_id = db.Column(db.String, unique=True, nullable=True)

    @classmethod
    def find_or_create_by_google(cls, google_id, email, first_name, last_name):
        user = cls.query.filter_by(google_id=google_id).first()
        if not user:
            user = cls(email=email, google_id=google_id, first_name=first_name, last_name=last_name)
            db.session.add(user)
            db.session.commit()
        return user
