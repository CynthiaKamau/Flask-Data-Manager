from datetime import datetime, timedelta
import unittest
from flask import Flask
from application import app, db
from application.models import Users, Sample

class UserModelCase (unittest.TestCase) :
    def setup(self) :
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_password_hashing (self):
        u = Users(username='dela')
        u.set_password('54321')
        self.assertFalse(u.check_password('qwerty'))
        self.assertTrue(u.check_password('54321'))

    def test_avatar(self):
        u = Users(username ='ann', email='ann@gmail.com')
        self.assertEqual(u.avatar(128), ('https://www.gravatar.com/avatat/'
            'f04f8de53d585524e3841daec07229fb'
            '?d=identicon&s=128'))

    def test_follow(self):
        u1 = Users(username='ann', email='ann@gmail.com')
        u2 = Users(username='dela', email='dela@gmail.com')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        self.assertEqual(u1.followed.all(), [])
        self.assertEqual(u1.followers.all(), [])

        u1.follow(u2)
        db.session.commit()
        self.assertTrue(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 1)
        self.assertEqual(u1.followed.first().username, 'dela')
        self.assertEqual(u2.followers.count(), 1)
        self.assertEqual(u2.followers.first().username, 'ann')

        u1.unfollow(u2)
        db.session.commit()
        self.assertFalse(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 0)
        self.assertEqual(u2.followers.count(), 0)

    def test_follow_samples(self):
        u1 = Users(username='ann', email='ann@gmail.com')
        u2 = Users(username='dela', email='dela@gmail.com')
        u3 = Users(username='klein', email='klein@gmail.com')
        u4 = Users(username='sarah', email='sarah@gmail.com')
        db.session.add_all([u1, u2, u3, u4])


    #creating four samples
    now = datetime.utcnow()
    s1 = Sample(types="butterfly", researcher=u1, 
        timestamp=now + timedelta(seconds=1))

    s2 = Sample(types="mosquito", researcher=u2,
        timestamp=now + timedelta(seconds=3))

    s3 = Sample(types="locusts", researcher=u3,
        timestamp=now + timedelta(seconds=6))

    s4 = Sample(types="caterpillar", researcher=u4,
        timestamp=now + timedelta(seconds=9))

    db.session.add_all([s1,s2,s3,s4])
    db.session.commit()

    #setting up followers
    u1.follow(u2) #ann follows dela
    u2.follow(u3) #dela follows klein
    u3.follow(u4) #kelin follows sarah
    u4.follow(u1) #sarah follows ann

    #check followed posts for each user
    f1 = u1.followed_posts().all()
    f2 = u2.followed_posts().all()
    f3 = u3.followed_posts().all()
    f4 = u4.followed_posts().all()
    self.assertEqual(f1, [p2, p4, p1])
    self.assertEqual(f2, [p2, p3])
    self.assertEqual(f3, [p3, p4])
    self.assertEqual(f1, [p4])

if __name__ == '__main__':
    unittest.main(verbosity=2)
