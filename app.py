from flask import Flask, redirect, render_template, flash, session, request
from models import db, connect_db, User, Post, Tag
""" Blogly application """

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///Blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "gettimjiggywithit9999999"
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG'] = True

connect_db(app)
db.create_all()

@app.route('/')
def root():
    """Show recent list of posts, most-recent first."""

    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    return render_template("posts/homepage.html", posts=posts)

@app.errorhandler(404)
def page_not_found(e):
    """Show 404 NOT FOUND page."""

    return render_template('404.html'), 404

##############################################################################
# User route

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

##############################################################################
# Posts route


@app.route('/users/<int:user_id>/posts/new')
def posts_new_form(user_id):
    """Show a form to create a new post for a specific user"""

    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template('posts/new.html', user=user, tags=tags)


@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def posts_new(user_id):
    """Handle form submission for creating a new post for a specific user"""

    user = User.query.get_or_404(user_id)
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    new_post = Post(title=request.form['title'],
                    content=request.form['content'],
                    user=user, 
                    tags=tags)

    db.session.add(new_post)
    db.session.commit()
    flash(f"Post '{new_post.title}' added.")

    return redirect(f"/users/{user_id}")


@app.route('/posts/<int:post_id>')
def posts_show(post_id):
    """Show a page with info on a specific post"""

    post = Post.query.get_or_404(post_id)
    return render_template('posts/show.html', post=post)


@app.route('/posts/<int:post_id>/edit')
def posts_edit(post_id):
    """Show a form to edit an existing post"""

    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    return render_template('posts/edit.html', post=post, tags=tags)


@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def posts_update(post_id):
    """Handle form submission for updating an existing post"""

    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    tag_ids = [int(num) for num in request.form.getlist("tags")]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    db.session.add(post)
    db.session.commit()
    flash(f"Post '{post.title}' edited.")

    return redirect(f"/users/{post.user_id}")


@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def posts_destroy(post_id):
    """Handle form submission for deleting an existing post"""

    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()
    flash(f"Post '{post.title} deleted.")

    return redirect(f"/users/{post.user_id}")

##############################################################################
# Tag route

@app.route('/tags')
def tags_index():
    """Show a page with info on all tags"""

    tags = Tag.query.all()
    return render_template('tags/index.html', tags=tags)

@app.route('/tags/new')
def tags_new_form():
    """Show a form to create a new tag"""

    posts = Post.query.all()
    return render_template('tags/new.html', posts=posts)

@app.route("/tags/new", methods=["POST"])
def tags_new():
    """Handle form submission for creating a new tag"""

    post_ids = [int(num) for num in request.form.getlist("posts")]
    posts = Post.query.filter(Post.id.in_(post_ids)).all()
    new_tag = Tag(name=request.form['name'], posts=posts)

    db.session.add(new_tag)
    db.session.commit()
    flash(f"Tag '{new_tag.name}' added.")

    return redirect("/tags")

@app.route('/tags/<int:tag_id>')
def tags_show(tag_id):
    """Show a page with info on a specific tag"""

    tag = Tag.query.get_or_404(tag_id)
    return render_template('tags/show.html', tag=tag)


@app.route('/tags/<int:tag_id>/edit')
def tags_edit_form(tag_id):
    """Show a form to edit an existing tag"""

    tag = Tag.query.get_or_404(tag_id)
    posts = Post.query.all()
    return render_template('tags/edit.html', tag=tag, posts=posts)


@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def tags_edit(tag_id):
    """Handle form submission for updating an existing tag"""

    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['name']
    post_ids = [int(num) for num in request.form.getlist("posts")]
    tag.posts = Post.query.filter(Post.id.in_(post_ids)).all()

    db.session.add(tag)
    db.session.commit()
    flash(f"Tag '{tag.name}' edited.")

    return redirect("/tags")


@app.route('/tags/<int:tag_id>/delete', methods=["POST"])
def tags_destroy(tag_id):
    """Handle form submission for deleting an existing tag"""

    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    flash(f"Tag '{tag.name}' deleted.")

    return redirect("/tags")