# coding:utf-8

import markdown
import datetime
from flask import Markup
from . import db

post_tags = db.Table('post_tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id')),
    db.Column('page_id', db.Integer, db.ForeignKey('posts.id'))
    )

class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    def __repr__(self):
        return '<tag: %r>' % self.name

    @staticmethod
    def generate_fake(count=50):
        from sqlalchemy.exc import IntegrityError
        from random import seed
        from faker import Factory
        fake = Factory.create()
        seed()
        for i in range(count):
            tag = Tag(name=fake.word())
            db.session.add(tag)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()




class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    slug = db.Column(db.String(300))
    md_text = db.Column(db.Text)
    content = db.Column(db.Text)
    pub_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    modify_date = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    category_id = db.Column(db.Integer, db.ForeignKey('categorys.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    tags = db.relationship('Tag', secondary=post_tags, backref=db.backref('posts', lazy='dynamic'))
    comments = db.relationship('Comment', backref='post', lazy='dynamic')
    tags_name = db.Column(db.Text)

    @classmethod
    def add_article(cls, title, md_text, content, author_id, category_id, tags, tags_name):
        post = cls(title=title, md_text=md_text, content=content, author_id=author_id, \
                    category_id=category_id, tags=tags, tags_name=tags_name)
        db.session.add(post)
        db.session.commit()

    def html(self):
        html = markdown.markdown(self.md_text, extensions=[ \
                                'markdown.extensions.fenced_code', \
                                'markdown.extensions.codehilite'])
        return Markup(html)

    def __repr__(self):
        return '<post: %r>' % self.title


    @staticmethod
    def generate_fake(count=50):
        from sqlalchemy.exc import IntegrityError
        from random import seed, randint
        from faker import Factory
        fake = Factory.create()
        seed()
        user_count = User.query.count()
        tag_count = Tag.query.count()
        category_count = Category.query.count()
        for i in range(count):
            u = User.query.offset(randint(0, user_count-1)).first()
            t = Tag.query.offset(randint(0, tag_count-1)).first()
            c = Category.query.offset(randint(0, category_count-1)).first()
            post = Post(title=fake.word(),
                        slug=fake.word(),
                        md_text=fake.paragraph(),
                        content=fake.paragraph(),
                        pub_date=fake.date_time(),
                        modify_date=fake.date_time(),
                        category_id=c.id,
                        author_id=u.id,
                        tags_name="python"
                        )
            db.session.add(post)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()


class Category(db.Model):
    __tablename__ = 'categorys'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True)
    posts = db.relationship('Post', backref='category', lazy='dynamic')

    def __repr__(self):
        return '<category name %r>' % self.name

    @staticmethod
    def generate_fake(count=50):
        from sqlalchemy.exc import IntegrityError
        from random import seed
        from faker import Factory
        fake = Factory.create()
        seed()
        for i in range(count):
            category = Category(name=fake.word())
            db.session.add(category)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(256))
    email = db.Column(db.String(120), unique=True)
    created_date = db.Column(db.DateTime , default=datetime.datetime.utcnow())
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    comments = db.relationship('Comment', backref='author', lazy='dynamic')


    #下面是Flask-Login需要的方法
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    #User类中自动添加的id
    def get_id(self):
        return str(self.id)

    def __unicode__(self):
        return self.name

    @staticmethod
    def generate_fake(count=50):
        from sqlalchemy.exc import IntegrityError
        from random import seed
        from faker import Factory
        fake = Factory.create()
        seed()
        for i in range(count):
            user = User(name=fake.name(),
                        password="123456",
                        email=fake.free_email(),
                        created_date=fake.date_time())
            db.session.add(user)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()



class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_time = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    content = db.Column(db.Text)
    disabled = db.Column(db.Boolean)

    def __init__(self, *args, **kwargs):
        super(Comment, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<comment %r>' % self.content



# class User(db.Model):
#     name = CharField(unique=True)
#     password = CharField()
#     email = CharField()
#     created_date = DateTimeField(default=datetime.datetime.now)
#
#     class Meta:
#         order_by = ('name',)

# class Tag(db.Model):
#     name = CharField()

# class Category(db.Model):
#     name = CharField(unique=True)

# class Post(db.Model):
#     title = CharField()
#     #这是用来自定义文章链接的
#     slug = CharField(unique=True)
#     content = TextField()
#     html = TextField()
#     pub_date = DateTimeField(default=datetime.datetime.now, index=True)
#     author = ForeignKeyField(User, related_name='posts')
#     category = ForeignKeyField(Category, related_name='posts')
#     tags = ManyToManyField(Tag, related_name='posts')
#
#     def html(self):
#         html = markdown.markdown(self.content, extensions=[ \
#                                 'markdown.extensions.fenced_code', \
#                                 'markdown.extensions.codehilite'])
#         return Markup(html)
#
#     class Meta:
#         order_by = ('-pub_date',)
#
#
# PostTag = Post.tags.get_through_model()

# db.create_tables([
#     Student,
#     Course,
#     StudentCourse])


# class Comment(db.Model):
#     author = ForeignKeyField(User)
#     content = TextField()
#     post = ForeignKeyField(Post, related_name='comments')
#     created_date = DateTimeField(default=datetime.datetime.now, index=True)
#
#     class Meta:
#         order_by = ('-created_date',)
