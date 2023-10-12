import datetime
import sqlite3
from flask import Flask,render_template,url_for,request,flash,message_flashed,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = 'mysecretkey12345'



class Article(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(100),nullable=False)
    email = db.Column(db.String(100),nullable=False)
    text = db.Column(db.Text,nullable=False)
    time = db.Column(db.DateTime,default=datetime.utcnow)
    def __repr__(self):
        return f'<Article {self.id}>'

@app.route("/")
def base():
    return render_template("base.html")
@app.route("/index")
def index():
    return render_template("index.html")
@app.route("/about")
def about():
    return render_template("about.html")
@app.route('/posts')
def posts():
    articles = Article.query.order_by(Article.time.desc()).all()
    return render_template("posts.html",articles=articles)
@app.route('/posts/<int:id>')
def posts_detail(id):
    article = Article.query.get(id)
    return render_template("posts_detail.html",article=article)
@app.route('/posts/<int:id>/delete')
def posts_delete(id):
    article = Article.query.get_or_404(id)

    try:
        db.session.delete(article)
        db.session.commit()
        return redirect(url_for('posts'))
    except:
        return "Error when using delete"


@app.route("/posts/<int:id>/update",methods=["POST","GET"])
def post_update(id):
    article = Article.query.get_or_404(id)

    if request.method == 'POST':
        article.title = request.form['title']
        article.email = request.form['email']
        article.text = request.form['text']


        try:
            db.session.commit()
            return redirect(url_for('posts'))
        except:
            return "Error when using update"
    else:
        return render_template("posts_update.html",article=article)

@app.route("/create_article",methods=["POST","GET"])
def create_article():
    if request.method == 'POST':
        title = request.form['title']
        email = request.form['email']
        text = request.form['text']

        if len(request.form['title']) > 4 and len(request.form['email']) > 4:
            res = Article(title=title,email=email,text=text)

            try:
                db.session.add(res)
                db.session.commit()
                flash("You are successfully registrated", category="success")
                return redirect(url_for('posts'))
            except Exception as e:
                flash(f"Error when adding to the database: {e}", category="error")
        else:
            flash("The fields are filled in incorrectly", category="error")
    return render_template("create_article.html")
if __name__ == '__main__':
    app.run(debug=True)