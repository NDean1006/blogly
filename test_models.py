from unittest import TestCase
from app import app
from models import db, Users

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///Blogly_db_test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.drop_all()
db.create_all()

class ModelsTests(TestCase):

    def setUp(self):
        """Stuff to do before every test."""
        Users.query.delete()

    def tearDown(self):
        db.session.rollback()
       
    def test_homepage(self):
        """Make sure INDEX HTML is displayed"""

        with self.client:
            response = self.client.get('/')
            self.assertIn(b'<h1>Users</h1>\n', response.data)
            