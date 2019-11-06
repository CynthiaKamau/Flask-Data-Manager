from datetime import datetime
from hashlib import md5
from application import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

#auxillary table od association
followers = db.Table ('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
    )

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    samples = db.relationship('Sample', backref='researcher', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) :
        return '<User {}>'.format(self.username)

    def set_password(self, password ) :
        self.password_hash = generate_password_hash(password)

    def check_password(self, password) :
        return check_password_hash(self.password_hash, password)

    def avatar(self, size) :
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon={}'.format(
            digest,size)

    followed = db.relationship(
    'User', secondary=followers,
    primaryjoin =(followers.c.follower_id==id),
    secondaryjoin=(followers.c.followed_id==id),
    backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')
    

@login.user_loader
def load_user(id) :
    return User.query.get(int(id))

class Sample(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(64))
    species = db.Column(db.String(165))
    location_collected = db.Column(db.String(165))
    project = db.Column(db.String(165))
    owner = db.Column(db.String(150))
    retension_period = db.Column(db.Integer)
    barcode = db.Column(db.String(165))
    analysis = db.Column(db.String(165))
    amount = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)


    def __repr__(self) :
        return '<Sample {}>'.format(self.type,self.species,self.location_collected, self.project, self.owner,self.retension_period,self.barcode,self.analysis,self.amount, self.user_id,self.timestamp)


