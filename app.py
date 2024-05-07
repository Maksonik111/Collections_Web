from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy #библиотеки для бд
from datetime import datetime

app = Flask(__name__) #создали обьект на основе класса flask(можно любое название)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Kategor.db' #бд sqlite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Article(db.Model): #модель для базы данных
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    datereliz = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return '<Article %r>' % self.id


@app.route('/') #отслеживаем url адрес
def index():
    return render_template("index.html") #вывод на экран html странички


@app.route('/collections')
def collections():
    articles = Article.query.order_by(Article.datereliz.desc()).all()
    return render_template("collections.html", articles=articles)


@app.route('/collections/<int:id>')
def collections_plus(id):
    article = Article.query.get(id)
    return render_template("collections_plus.html", article=article)

@app.route('/collections/<int:id>/del')
def collections_del(id):
    article = Article.query.get_or_404(id)
    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/collections')
    except:
        return "При удалении коллекции произошла ошибка"


@app.route('/collections/<int:id>/up', methods=['POST', 'GET'])
def collections_up(id):
    article = Article.query.get(id)
    if request.method == "POST":
        article.name = request.form['name']
        article.genre = request.form['genre']
        article.description = request.form['description']
        article.datereliz = datetime.strptime(request.form['datereliz'], '%Y-%m-%d')

        try:
            db.session.commit()
            return redirect('/collections')
        except:
            return "При редактировании коллекции произошла ошибка"
    else:

        return render_template("collections_up.html", article=article)


@app.route('/addition', methods=['POST', 'GET'])
def addition():
    if request.method == "POST":
        name = request.form['name']
        genre = request.form['genre']
        description = request.form['description']
        datereliz = datetime.strptime(request.form['datereliz'], '%Y-%m-%d')

        article = Article(name=name, genre=genre, description=description, datereliz=datereliz)

        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/addition')
        except:
            return "При добавлении коллекции произошла ошибка"
    else:
        return render_template("addition.html")


if __name__ == "__main__": #проверка запуска программы с этого файла
    # with app.app_context(): #создание бд
    #     db.create_all()
    app.run(debug=True)


