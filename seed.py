"""Seed file to make sample data for pets db."""

from models import User, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()

# Add User
Bob = User(first_name='Bob', last_name="Bobertson")
Bobly = User(first_name='Bobly', last_name="bobbington",image_url="https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcQtEXLb6Fe08VLoo-niT9j6J8D1RebmoDDVKw&usqp=CAU")
goddammit = User(first_name='Goddammit', last_name="Bobby")

# Add new objects to session, so they'll persist
db.session.add(Bob)
db.session.add(Bobly)
db.session.add(goddammit)

# Commit--otherwise, this never gets saved!
db.session.commit()
