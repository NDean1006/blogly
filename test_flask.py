from unittest import TestCase
from app import app
from models import db, Users

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///Blogly_db_test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['TESTING']= True

app.config['DEBUF_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class FlaskTests(TestCase):
    """ tests for views for users"""

    def setUp(self):
        """Stuff to do before every test."""
        Users.query.delete()

        user = Users(First_name="TestUser", last_name="Ham'N'Cheese")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

    def tearDown(self):
        db.session.rollback()
       
    def test_homepage(self):
        """Make sure INDEX HTML is displayed"""

        with app.test_client() as client:
            resp = self.client.get('/')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("TestUser", html)

            self.assertIn(b'<h1>Users</h1>\n', html)