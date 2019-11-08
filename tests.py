from datetime import datetime, timedelta
import unittest
from application import app, db
from application.models import Users, Sample

class UsersModelCase (unittest.TestCase) :
    def setup(self) :
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://shiro:zoom@localhost/dataproject'
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
        db.session.add_all(u1, u2, u3, u4)
      
      
 

if __name__ == '__main__':
    unittest.main(verbosity=2)
