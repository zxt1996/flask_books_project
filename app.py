from flask import Flask,render_template,flash,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired

import sys
import importlib
importlib.reload(sys)


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@127.0.0.1/flask_books'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'zxt'

db = SQLAlchemy(app)

class Author(db.Model):
    __tablename__ = 'authors'

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(16),unique=True)

    books = db.relationship('Book',backref='author')

    def __repr__(self):
        return 'Author:%s' %self.name

class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(16),unique=True)
    author_id = db.Column(db.Integer,db.ForeignKey('authors.id'))

    def __repr__(self):
        return 'Book: %s %s'%(self.name,self.author_id)

class AuthorForm(FlaskForm):
    author = StringField('author',validators=[DataRequired()])
    book = StringField('book',validators=[DataRequired()])
    submit = SubmitField('submit')


@app.route('/delete_author/<author_id>')
def delete_author(author_id):
    author = Author.query.get(author_id)

    if author:
        try:
            Book.query.filter_by(author_id=author.id).delete()

            db.session.delete(author)
            db.session.commit()
        except Exception as e:
            flash('delete author have error')
            db.session.rollback()

    else:
        flash('not find author')

    return redirect(url_for('index'))

@app.route('/delete_book/<book_id>')
def delete_book(book_id):
    book = Book.query.get(book_id)

    if book:
        try:
            db.session.delete(book)
            db.session.commit()
        except Exception as e:
            print('e')
            flash('chucuo')
            db.session.rollback()
    else:
        flash('book not find')

    print(url_for('index'))
    return redirect(url_for('index'))

@app.route('/',methods=['GET','POST'])
def index():
    author_form = AuthorForm()

    authors = Author.query.all()

    if author_form.validate_on_submit():
        author_name = author_form.author.data
        book_name = author_form.book.data

        author = Author.query.filter_by(name=author_name).first()

        if author:
            book = Book.query.filter_by(name=book_name).first

            if book:
                flash('yicunzaitongmignshuji')
            else:
                try:
                    new_book = Book(name=book_name, author_id=author.id)
                    db.session.add(new_book)
                    db.session.commit()
                except Exception as e:
                    print('e')
                    flash('tianjiashibai')
                    db.session.rollback()
        else:
            try:
                new_author = Author(name=author_name)
                db.session.add(new_author)
                db.session.commit()

                new_book = Book(name=book_name,author_id=new_author.id)
                db.session.add(new_book)
                db.session.commit()
            except Exception as e:
                print('e')
                flash('tianjiazuozeheshujishibai')
                db.session.rollback()
    else:
        if request.method == 'POST':
            flash('cangshubuquan')

    return render_template('books.html',authors=authors,form=author_form)


if __name__ == '__main__':

    db.drop_all()
    db.create_all()

    au1 = Author(name='laowang')
    au2 = Author(name='laohui')
    au3 = Author(name='laoliu')

    db.session.add_all([au1,au2,au3])

    db.session.commit()

    bk1 = Book(name='z',author_id=au1.id)
    bk2 = Book(name='x',author_id=au1.id)
    bk3 = Book(name='t',author_id=au2.id)
    bk4 = Book(name='zz',author_id=au3.id)
    bk5 = Book(name='zzz',author_id=au3.id)

    db.session.add_all([bk1,bk2,bk3,bk4,bk5])

    db.session.commit()

    app.run(debug=True)
