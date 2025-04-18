from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import  SQLAlchemy
from datetime import datetime

from werkzeug.utils import redirect

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///danjo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
db = SQLAlchemy(app)


class Achive(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Achive %r>' % self.id

@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/posts')
def posts():
    articles = Achive.query.order_by(Achive.date.desc()).all()
    return render_template("posts.html", articles=articles)

@app.route('/posts/<int:id>')
def posts_det(id):
    article = Achive.query.get(id)
    return render_template("posts_det.html", article=article)


@app.route('/posts/<int:id>/del')
def posts_delete(id):
    article = Achive.query.get_or_404(id)
    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/posts')
    except:
        return "При удалении произошла ошибка"

@app.route('/posts/<int:id>/update', methods = ['POST', 'GET'])
def post_update(id):
    article = Achive.query.get(id)
    if request.method == "POST":
        article.title = request.form['title']
        article.intro = request.form['intro']
        article.text = request.form['text']

        try:
            db.session.commit()
            return redirect('/posts')
        except:
            return "При редактировании статьи произошла ошибка"

    else:
        return render_template("post_update.html", article=article)


@app.route('/create-achive', methods = ['POST', 'GET'])
def create_achive():
    if request.method == "POST":
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        article = Achive(title=title, intro = intro, text= text)

        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/posts')
        except:
            return "При добавлении статьи произошла ошибка"

    else:
        return render_template("create-achive.html")

if __name__ == "__main__":
    app.run()