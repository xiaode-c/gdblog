# coding:utf-8

import markdown
from . import admin
from flask import render_template, url_for, request, flash, redirect
from .. import db, login_manager
from ..models import User, Post, Tag, Category, Comment, post_tags
from flask.ext.login import login_required, login_user, logout_user, current_user
from .forms import LoginForm, AddPostForm

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@admin.route("/")
@login_required
def index():
    return render_template("admin/index.html")

@admin.route("/posts")
@admin.route('/posts/<int:page>', methods=['GET', 'POST'])
@login_required
def posts(page=1):
    pagination = Post.query.order_by('-pub_date').paginate(page, 10, False)
    posts = pagination.items
    return render_template("admin/posts.html", posts=posts, pagination=pagination)

@admin.route('/comments')
@admin.route('/comments/<int:page>', methods=['GET', 'POST'])
@login_required
def comments(page=1):
    pagination = Comment.query.order_by('-created_time').paginate(page, 10, False)
    comments = pagination.items
    return render_template("admin/comments.html", pagination=pagination, comments=comments)

@admin.route("/categorys")
@admin.route('/categorys/<int:page>', methods=['GET', 'POST'])
@login_required
def categorys(page=1):
    pagination = Category.query.order_by('name').paginate(page, 10, False)
    categorys = pagination.items
    return render_template("admin/categorys.html", categorys=categorys, pagination=pagination)

@admin.route("/tags")
@admin.route('/tags/<int:page>', methods=['GET', 'POST'])
@login_required
def tags(page=1):
    pagination = Tag.query.order_by('name').paginate(page, 10, False)
    tags = pagination.items
    return render_template("admin/tags.html", tags=tags, pagination=pagination)

@admin.route("/users")
@admin.route('/users/<int:page>', methods=['GET', 'POST'])
@login_required
def users(page=1):
    pagination = Category.query.order_by('name').paginate(page, 10, False)
    users = pagination.items
    return render_template("admin/users.html", users=users, pagination=pagination)

@admin.route("/add-post", methods=['GET', 'POST'])
@login_required
def add_post():
    form = AddPostForm()
    categories = Category.query.all()
    form.category.choices = [(c.id, c.name) for c in categories]
    if request.method == "POST":
        title = form.title.data
        md_text = form.content.data
        category_id = int(form.category.data)
        content = markdown.markdown(md_text, extensions=[ \
                                'markdown.extensions.fenced_code', \
                                'markdown.extensions.codehilite', \
                                'markdown.extensions.tables'])
        print content
        author_id = current_user.id
        tag_name = form.tags.data
        tag_list = form.tags.data.split(',')
        tags = []

        for i in range(0,len(tag_list)):
            tag_list[i] = tag_list[i].strip()
        tags = []
        for tag in tag_list:
            tag_obj = Tag.query.filter_by(name=tag).first()
            if tag_obj is None:
                tag_obj = Tag(name=tag)
            tags.append(tag_obj)

        Post.add_article(title=title, md_text=md_text, content=content, \
                    author_id=author_id, tags=tags, category_id=category_id, \
                    tags_name=tag_name)
    return render_template("admin/add-post.html", categories=categories, form=form)

@admin.route("/edit-post/<int:post_id>", methods=['GET', 'POST'])
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    if request.method == "GET":
        return render_template("admin/edit-post.html", post=post)
    else:
        post.title = request.form["title"]
        content = request.form["body"]
        post.md_text = md_text
        post.body = markdown.markdown(post.md_text, extensions=[ \
                                'markdown.extensions.fenced_code', \
                                'markdown.extensions.codehilite'])
        db.session.add(post)
        db.session.commit()
        return redirect(url_for("admin.posts"))

@admin.route('/posts/<int:post_id>/delete', methods=['GET'])
@login_required
def delete_post(post_id):
    post = Post.query.filter(Post.id==post_id).first()
    if post:
        db.session.delete(post)
        db.session.commit()
    return redirect(url_for("admin.posts"))

@admin.route("/add-tag", methods=['GET', 'POST'])
@login_required
def add_tag():
    if request.method == 'GET':
        return render_template(url_for("admin.tags"))
    else:
        name = request.form["name"]
        tag = Tag(name=name)
        db.session.add(tag)
        db.session.commit()
        return redirect(url_for('admin.tags'))

@admin.route('/tags/<int:tag_id>/delete', methods=['GET'])
@login_required
def delete_tag(tag_id):
    tag = Tag.query.filter(Tag.id==tag_id).first()
    if tag:
        db.session.delete(tag)
        db.session.commit()
    return redirect(url_for("admin.tags"))

@admin.route("/add-category", methods=['GET', 'POST'])
@login_required
def add_category():
    if request.method == 'GET':
        return render_template(url_for("admin.categorys"))
    else:
        name = request.form["name"]
        category = Category(name=name)
        db.session.add(category)
        db.session.commit()
        return redirect(url_for("admin.categorys"))

@admin.route('/categorys/<int:category_id>/delete', methods=['GET'])
@login_required
def delete_category(category_id):
    category = Category.query.filter(Category.id==category_id).first()
    if category:
        db.session.delete(category)
        db.session.commit()
    return redirect(url_for("admin.categorys"))

@admin.route("/add-user", methods=['GET', 'POST'])
@login_required
def add_user():
    if request.method == 'GET':
        return render_template(url_for("admin.users"))
    else:
        user_name = request.form["name"]
        password = request.form["password"]
        email = request.form["email"]
        user = User(name=user_name, password=password, email=email)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("admin.users"))

@admin.route('/users/<int:user_id>/delete', methods=['GET'])
@login_required
def delete_user(user_id):
    user = User.query.filter(User.id==user_id).first()
    if user:
        db.session.delete(user)
        db.session.commit()
    return redirect(url_for("admin.users"))


@admin.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == "POST":
        username = form.username.data
        password = form.password.data
        remember_me = form.remember_me.data
        user = User.query.filter_by(name=username).first()
        if user is not None:
            login_user(user, remember_me)
            return redirect(request.args.get('next') or url_for("admin.index"))
        flash('Invalid username or password')
    return render_template("login.html", form=form)

@admin.route("/logout")
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))
