from flask import Flask, redirect, render_template, flash, session, request
from models import db, connect_db, User
""" Blogly application """

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///Blogly_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "gettimjiggywithit9999999"
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG'] = True

connect_db(app)
db.create_all()

@app.route('/')
def show_home():
    return redirect("/users")

@app.route('/users')
def home_page():
    """ show home page """
    u = User.query.all()
    return render_template('index.html', u=u)

@app.route('/users/new')
def add_new_user():
    """ show create new user page"""
    return render_template('add_new.html')

@app.route('/users/new', methods=["POST"])
def create_new_user():
    """ show create new user page"""
    new_user = User(
        first_name=request.form['first_name'],
        last_name=request.form['last_name'],
        image_url=request.form['image_url'] or None)

    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")

@app.route('/users/<int:user_id>')
def show_user(user_id):
    """ Show details single pet"""
    user = User.query.get_or_404(user_id)
    return render_template("user.html", user=user)


@app.route('/users/<int:user_id>/edit')
def show_user_edit(user_id):
    """" Show user edit page """
    user = User.query.get_or_404(user_id)
    return render_template('edit.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def users_update(user_id):
    """Handle submission for updating a user"""

    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect("/users")

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def users_destroy(user_id):
    """Handle submission for deleting a user"""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")