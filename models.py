
import datetime
from flask_sqlalchemy import SQLAlchemy
"""Models for Blogly."""


db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

DEFAULT_IMAGE_URL = "https://www.freeiconspng.com/uploads/icon-user-blue-symbol-people-person-generic--public-domain--21.png"
# define models 

class User(db.Model):
    """ User """

    __tablename__ = "users"

    def __repr__(self):
       u = self
       return f"<User id={u.id} first_name={u.first_name} last_name={u.last_name} image_url={u.image_url}>"

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)

    first_name = db.Column(db.Text, nullable=False,)
    
    last_name = db.Column(db.Text,nullable=False,)

    image_url = db.Column(db.Text,
                     nullable=False,
                     unique=False,
                     default=DEFAULT_IMAGE_URL)

    posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")

    @property
    def full_name(self):
        """Return full name of user."""

        return f"{self.first_name} {self.last_name}"



class Post(db.Model):
    """ Post """

    __tablename__ = "posts"

    def __repr__(self):
       p = self
       return f"<Post id={p.id} title={p.title} content={p.content} created_at={p.created_at} >"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    @property
    def friendly_date(self):
        """Return nicely-formatted date."""

        return self.created_at.strftime(" %a %X %x")

class PostTag(db.Model):
    """ Joins Posts and tags """

    __tablename__ = "post_tags"

    def __repr__(self):
       pt = self
       return f"<PostTag  post_id={pt.post_id} tag_id={pt.tag_id} >"

    post_id =  db.Column(db.Integer,
                    db.ForeignKey("posts.id"),
                    primary_key=True)
    tag_id = db.Column(db.Integer,
                    db.ForeignKey("tags.id"),
                    primary_key=True )

class Tag(db.Model):
    """ Tag Model """

    __tablename__ = "tags"

    def __repr__(self):
       t = self
       return f"<Tag  id={t.id} name={t.name} >"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False, unique=True)

    posts = db.relationship(
        'Post',
        secondary="post_tags",
        cascade="all,delete",
        backref="tags",
    )


