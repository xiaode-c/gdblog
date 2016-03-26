# coding:utf-8

from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, PasswordField, SelectField, BooleanField, DateTimeField
from wtforms.validators import Required
from flask_pagedown.fields import PageDownField


class LoginForm(Form):
    username = StringField(u'用户名:', validators=[Required()])
    password = PasswordField(u'密码:', validators=[Required()])
    remember_me = BooleanField(u'记住')
    submit = SubmitField(u'登录')

class AddPostForm(Form):
    title = StringField(u"标题", validators=[Required()])
    content = PageDownField(u"正文")
    category = SelectField(u"分类", validators=[Required()])
    tags = StringField(u"标签", validators=[Required()])
    submit = SubmitField(u"发布")

class EditPostForm(Form):
    title = StringField(u"标题", validators=[Required()])
    content = PageDownField(u"正文")
    submit = SubmitField(u"发布")
