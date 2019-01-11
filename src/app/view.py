from app import app, db
from flask import render_template, redirect, url_for, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, EqualTo, Length
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Post
from werkzeug.urls import url_parse


class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password2 = PasswordField(
        'Повторите пароль', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Регистрация')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Введите другое имя!')


class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')


class PostForm(FlaskForm):
    head_post = StringField('Задание', validators=[DataRequired()])
    body_post = TextAreaField('Описание задания', validators=[Length(min=0, max=500)])
    submit = SubmitField('Добавить задание')


class EditForm(FlaskForm):
    head_post = StringField('Задание', validators=[DataRequired()])
    body_post = TextAreaField('Описание задания', validators=[Length(min=0, max=500)])
    submit = SubmitField('Изменить')


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(head=form.head_post.data, body=form.body_post.data, user_id=current_user.id, timestamp=datetime.now())
        post.store_to_db()
        return redirect(url_for('index'))
    posts = Post.query.filter_by(user_id=current_user.id).all()
    posts.reverse()
    posts = posts[0:3]
    return render_template('index.html', form=form, posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            return redirect(url_for('login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/<int:id>/del')
@login_required
def del_task(id):
    Post.query.filter_by(id=id).first().delete_post()
    return redirect(url_for('index'))


@app.route('/all_post', methods=['GET', 'POST'])
@login_required
def all_post():
    posts = Post.query.filter_by(user_id=current_user.id).all()
    posts.reverse()
    return render_template('all_post.html', posts=posts)


@app.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_task(id):
    post = Post.query.filter_by(id=id).first()
    form = EditForm(head_post=post.head, body_post=post.body)
    posts = Post.query.filter_by(user_id=current_user.id).all()[:3]
    print(id)
    if form.validate_on_submit():
        Post.query.filter_by(id=id).update({Post.head: form.head_post.data})
        Post.query.filter_by(id=id).update({Post.body: form.body_post.data})
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('index.html', posts=posts, form=form)
