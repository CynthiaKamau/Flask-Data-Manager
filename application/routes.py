from datetime import datetime
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from application import app, db
from application.forms import LoginForm, RegistrationForm
from application.models import Users, Sample
from application.forms import EditProfileForm, SampleForm, ResetPasswordForm


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route ('/', methods=['GET', 'POST'])
@app.route ('/index', methods=['GET', 'POST'])
@login_required
def index () :
    form = SampleForm()
    if form.validate_on_submit():
        sample = Sample( description= form.sample.data, species= form.sample.data, location_collected= form.sample.data, project= form.sample.data, owner= form.sample.data, retension_period= form.sample.data, barcode= form.sample.data, analysis= form.sample.data, amount=form.sample.data, researcher=current_user)
        db.session.add(sample)
        db.session.commit()
        flash('Your post is now live!')

    page = request.args.get('page', 1, type=int)
    samples = current_user.followed_samples(). paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('index', page=samples.next_num) \
        if samples.has_next else None
    prev_url = url_for('index', page=samples.prev_num) \
        if samples.has_prev else None
    return render_template("index.html", title ="Home Page", form=form, samples=samples.items, next_url=next_url, prev_url=prev_url)


@app.route ('/login', methods= ['GET', 'POST'])
def login ():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data) :
            flash ('Invalid username or password')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    
    return render_template ('login.html', title='Register as a new user', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return (url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = Users(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Sucessfully registered as a new user')
        return redirect(url_for('login'))
    return render_template('register.html', title='Registration', form=form)

@app.route('/user/<username>')
@login_required
def user(username) :
    user = Users.query.filter_by(username =username).first_or_404()
    page = request.args.get('page', 1, type=int)
    samples = user.samples.order_by(Sample.timestamp.desc()).paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('user', username= user.username,page=samples.next_num) \
        if samples.has_next else None
    prev_url = url_for('user', username=user.username, page=samples.prev_num) \
        if samples.has_prev else None
    
    return render_template('user.html', user=user, samples=samples.items, next_url=next_url, prev_url=prev_url)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved')
        return redirect(url_for('edit_profile'))
    elif request.method =='GET' :
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',form=form)

@app.route('/follow/<username>')
@login_required
def follow(username):
    user = Users.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('indes'))

    if user == current_user:
        flash('You cannot follow yourself')
        return redirect(url_for('index'))
    current_user.follow(user)
    db.session.commit()
    flash('You are noe following {}!'.format(username))
    return redirect(url_for('user', username=username))


@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = Users.query.filter_by(username=username).first()
    if user is None:
        flash ('User {} not found .'.format(username))
        return redirect(url_for('index'))

    if user == current_user:
        flash('You cannot unfollow yourself!')
        return redirect(url_for('user', username=username))

    current_user.follow(user)
    db.session.commit()
    flash ('You have stopped following {}.'.format(username))
    return redirect(url_for('user', username=username))

@app.route('/search')
@login_required
def search():
    page = request.args.get('page', 1, type=int)
    samples = Sample.query.order_by(Sample.timestamp.desc()).paginate(
        page, app.config['POSTS_PER_PAGE'], False)

    next_url = url_for('search', page=samples.next_num) \
        if samples.has_next else None
    prev_url = url_for('explore', page=samples.prev_num) \
        if samples.has_prev else None

    return render_template('index.html', title='Search Samples', samples=samples.items, next_url=next_url, prev_url =prev_url)

@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequest()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
            flash('Check your email for a password reset link')
            return redirect(url_for('login'))
            return render_template('reset_password_request.html', title='Reset Password', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    user= Users.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)
