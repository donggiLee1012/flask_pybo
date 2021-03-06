from pybo import db

question_voter = db.Table(
    'question_voter',
    db.Column('user_id',db.Integer,db.ForeignKey('user.id',ondelete='CASCADE'),primary_key=True),
    db.Column('question_id',db.Integer,db.ForeignKey('question.id',ondelete='CASCADE'),primary_key=True)
)
answer_voter = db.Table(
    'answer_voter',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True),
    db.Column('answer_id', db.Integer, db.ForeignKey('answer.id', ondelete='CASCADE'), primary_key=True)
)



class Question(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    subject = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text(),nullable=False)
    create_date = db.Column(db.DateTime(),nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id',ondelete='CASCADE'), nullable=False)
    user = db.relationship('User',backref=db.backref('question_set'))
    modify_date = db.Column(db.DateTime(),nullable=True)
    voter = db.relationship('User', secondary=question_voter, backref=db.backref('question_voter_set'))


class Answer(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'))
    question = db.relationship('Question',backref=db.backref('answer_set',cascade='delete'))
    content = db.Column(db.Text(),nullable=False)
    create_date = db.Column(db.DateTime(),nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('answer_set'))
    modify_date = db.Column(db.DateTime(),nullable=True)
    voter = db.relationship('User', secondary=answer_voter, backref=db.backref('answer_voter_set'))

class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(150),unique=True,nullable=False)
    password = db.Column(db.String(200),nullable=False)
    email = db.Column(db.String(120),unique=True,nullable=False)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('comment_set'))
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    modify_date = db.Column(db.DateTime())
    question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'), nullable=True)
    question = db.relationship('Question', backref=db.backref('comment_set'))
    answer_id = db.Column(db.Integer, db.ForeignKey('answer.id', ondelete='CASCADE'), nullable=True)
    answer = db.relationship('Answer', backref=db.backref('comment_set'))

class Shoesmodel(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(50),unique=True)
    subname = db.Column(db.String(50), unique=True)
    code = db.Column(db.String(30),unique=True)
    img = db.Column(db.Text())
    brand = db.Column(db.String(30),nullable=False)
    retail_price = db.Column(db.Integer,default=0)
    release_date = db.Column(db.DateTime())
    colorway = db.Column(db.Text())

class Structureprice(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    code = db.Column(db.String(30), db.ForeignKey('shoesmodel.code',onupdate='CASCADE'))
    saleday = db.Column(db.DateTime(), nullable=False)
    price = db.Column(db.Integer,default=0)
    size = db.Column(db.Integer,default=200)




class Shoes(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(200),nullable=False)
    condition = db.Column(db.String(20),default='새상품')
    size = db.Column(db.String(30))
    price = db.Column(db.Integer,default=0)
    seller = db.Column(db.String(30))
    upload_date = db.Column(db.DateTime())
    uri = db.Column(db.Text())
    img = db.Column(db.Text())
    search_query = db.Column(db.String(30))

    shoesmodel_id = db.Column(db.String(30), db.ForeignKey('shoesmodel.id',onupdate='CASCADE'))
    shoesmodel = db.relationship('Shoesmodel', backref=db.backref('sales_set'))


