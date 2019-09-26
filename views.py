from app import app, photos, db
from models import User, Post, followers
from forms import RegisterForm, PostForm, LoginForm
from flask import render_template, redirect, url_for, request, abort
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import login_required, current_user, logout_user, login_user


@app.route('/')
def index():
    form = LoginForm()

    return render_template('index.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'GET':
        return redirect(url_for('index'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if not user:
            return render_template('index.html', form=form, message='Login Failed')

        if check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)

            return redirect(url_for('profile'))

        return render_template('index.html', form=form, message='Login Failed')

    return render_template('index.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/profile', defaults={'username' : None})
@app.route('/profile/<username>')
def profile(username):
    if username:
        user = User.query.filter_by(username=username).first()
        if not user:
            abort(404)
    else:
        user = current_user

    posts = Post.query.filter_by(user=user).order_by(Post.date_created.desc()).all()

    current_time = datetime.now()

    followed_by = user.followed_by.all()

    display_follow = True

    if current_user == user:
        display_follow = False
    elif current_user in followed_by:
        display_follow = False

    who_to_watch = User.query.filter(User.id != user.id).order_by(db.func.random()).limit(4).all()

    return render_template('profile.html', who_to_watch=who_to_watch, user=user, posts=posts, current_time=current_time, followed_by=followed_by, display_follow=display_follow)

@app.route('/timeline', defaults={'username': None})
@app.route('/timeline/<username>')
def timeline(username):
    form = PostForm()
    if username:
        user = User.query.filter_by(username=username).first()
        if not user:
            abort(404)
        
        posts = Post.query.filter_by(user=user).order_by(
        Post.date_created.desc()).all()
        total_posts = len(posts)
    else:
        user = current_user
        posts = Post.query.join(followers, (followers.c.followee_id == Post.user_id)).filter(followers.c.follower_id == current_user.id).order_by(Post.date_created.desc()).all()
        total_posts = Post.query.filter_by(user=user).order_by(
        Post.date_created.desc()).count()

    current_time = datetime.now()
    followed_by = user.followed_by.all()
    who_to_watch = User.query.filter(User.id != user.id).order_by(db.func.random()).limit(4).all()

    return render_template('timeline.html', who_to_watch=who_to_watch, followed_by=followed_by, form=form, posts=posts, current_time=current_time, user=user, total_posts=total_posts)


@app.route('/make_post', methods=['POST'])
@login_required
def make_post():
    form = PostForm()

    if form.validate():
        post = Post(user_id=current_user.id,
                    text=form.text.data, date_created=datetime.now())
        db.session.add(post)
        db.session.commit()

        return redirect(url_for('timeline'))

    return 'Something went wrong.'


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        image_filename = photos.save(form.image.data)
        image_url = photos.url(image_filename)

        new_user = User(name=form.name.data, username=form.username.data,
                        image=image_url, password=generate_password_hash(form.password.data), join_date=datetime.now())
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)

        return redirect(url_for('profile'))

    return render_template('register.html', form=form)

@app.route('/follow/<username>')
@login_required
def follow(username):
    user_to_follow = User.query.filter_by(username=username).first()

    current_user.following.append(user_to_follow)

    db.session.commit()
    return redirect(url_for('profile'))