# coding:utf-8

import datetime
import random
from flask import Flask, render_template, url_for
from ..models import  User, Post, Tag, Category, Comment, post_tags
# from .. import app
from . import main



@main.route("/", methods=['GET', 'POST'])
@main.route('/index', methods=['GET', 'POST'])
@main.route('/index/<int:page>', methods=['GET', 'POST'])
def index(page=1):
    title = "Index"
    pagination = Post.query.order_by('-pub_date').paginate(page, 10, False)
    posts = pagination.items
    return render_template("index.html", posts=posts, pagination=pagination)

@main.route("/posts/<title>", methods=['GET', 'POST'])
def posts(title):
    post = Post.query.filter(Post.title==title).first()
    return render_template('post.html', post=post)


@main.route("/categorys")
def categorys():
    categorys = Category.query.all()
    return render_template('categorys.html', categorys=categorys)

@main.route("/categorys/<name>")
@main.route('/categorys/<name>/<int:page>', methods=['GET', 'POST'])
def category(name, page=1):
    category = Category.query.filter(name==name).first()
    pagination = category.posts.order_by('-pub_date').paginate(page,10,False)
    posts = pagination.items
    return render_template('category.html', posts=posts, pagination=pagination)

@main.route("/tags/")
def tags():
    tags = Tag.query.all()
    return render_template('tags.html', tags=tags)

@main.route("/tags/<name>")
def tag(name, page=1):
    tag = Tag.query.filter(Tag.name==name).first()
    pagination = tag.posts.order_by('-pub_date').paginate(page,10,False)
    posts = pagination.items
    return render_template('tag.html', posts=posts, tag=tag, pagination=pagination)

@main.route("/about")
def about():
    return render_template('about.html')
