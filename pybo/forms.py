from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField,PasswordField,SelectField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired,Length,EqualTo,Email


class QuestionForm(FlaskForm):
    # DataRequired 필수값표시 , Email 이메일인지 체크
    subject = StringField('제목',validators=[DataRequired('제목은 필수입력 항목입니다.')])
    content = TextAreaField('내용',validators=[DataRequired('내용은 필수입력 항목입니다.')])

class AnswerForm(FlaskForm):
    content = TextAreaField('내용',validators=[DataRequired('내용은 필수입력 항목입니다.')])

class UserCreateForm(FlaskForm):
    username = StringField('사용자이름', validators=[DataRequired(), Length(min=3, max=25)])
    password1 = PasswordField('비밀번호', validators=[DataRequired(), EqualTo('password2', '비밀번호가 일치하지 않습니다')])
    password2 = PasswordField('비밀번호확인', validators=[DataRequired()])
    email = EmailField('이메일', [DataRequired('이메일은 필수입력 항목입니다.'), Email()])

class UserLoginForm(FlaskForm):
    username = StringField('사용자이름',validators=[DataRequired(), Length(min=3,max=25)])
    password = PasswordField('비밀번호',validators=[DataRequired()])

class CommentForm(FlaskForm):
    content = TextAreaField('내용',validators=[DataRequired()])

cho =[('','선택안함')]
for i in range(220,315,5):
    cho.append((str(i),str(i)+'mm'))

class SearchShoes(FlaskForm):

    size = SelectField('사이즈',choices=cho,coerce=str)
    content = StringField('내용',validators=[DataRequired('검색하실 신발명을 입력하세요.')])
