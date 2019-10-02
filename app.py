from flask import Flask, render_template, url_for, request, redirect
from flask_pymongo import PyMongo
# from models import ToDo

app = Flask(__name__)
app.debug = True
app.config["MONGO_URI"] = "mongodb://localhost:27017/ToDo"
mongo = PyMongo(app)

class ToDo(mongo.Model):
    id = IntField(primary_key=True)
    title = StringField(max_length=60, required=True)
    content = StringField(max_length=200)
    image = ImageField(size=2000)
    created = DateField(default=datetime.utcnow)

    def __repr__(self):
        return self.id

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        new_task = ToDo(title=title, content=content)

        try:
            mongo.
            mongo.session.commit()
            return redirect('/')
        except:
            return "Error, cloud not connect db"
    else:
        return render_template("index.html")