from flask import Flask, render_template, url_for, request, redirect
from werkzeug.utils import secure_filename
from flask_mongoengine import MongoEngine
from datetime import datetime
from models import ToDo
from PIL import Image
from itertools import cycle
import os


app = Flask(__name__)
app.debug = True
app.config["MONGO_URI"] = "mongodb://localhost:27017/ToDo"

app.config['APP_ROOT'] = os.path.dirname(os.path.abspath(__file__))
app.config['IMAGE_UPLOADS'] = '/static/uploads'

db = MongoEngine(app)


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
def allowed_image(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        color = request.form['color']
        
        if request.files:

            image = request.files["image"]
            if not image.filename:
                return "No filename"

            if allowed_image(image.filename):
                filename = os.path.join(app.config['IMAGE_UPLOADS'], "{}.jpg".format(datetime.now().strftime('%m%s')))
                
                image.save(''.join([app.config['APP_ROOT'],filename]))

                # color = cycle(['primary', 'secondary', 'success', 'danger', 'warning', 'info', 'dark'])
                
                new_task = ToDo(title=title, content=content, img=filename, color=color)

                try:
                    new_task.save()
                    return redirect(request.url)
                except:
                    return "Error, cloud not connect db"
            else:
                return "That file extension is not allowed"  
    else:

        tasks = ToDo.objects()
        
        return render_template("index.html", tasks=tasks)


@app.route('/delete/<id>')
def delete(id):
    
    if ToDo.objects(id=id):
        filename = ToDo.objects(id=id)[0].img
        os.remove(''.join([app.config['APP_ROOT'],filename]))


        ToDo.objects(id=id).delete()
        return redirect('/')
    return 'There was a problem deleting that task'


@app.route('/update/<id>', methods=['POST', 'GET'])
def update(id):

    if request.method == 'POST':
        if ToDo.objects(id=id):
            title = request.form['title']
            content = request.form['content']
            filename = ToDo.objects(id=id)[0].img
            if request.files and request.files["image"].filename:
                image = request.files["image"]

                if allowed_image(image.filename):
                    os.remove(''.join([app.config['APP_ROOT'],filename]))
                    filename = os.path.join(app.config['IMAGE_UPLOADS'], "{}.jpg".format(datetime.now().strftime('%m%s')))
                    image.save(''.join([app.config['APP_ROOT'],filename]))
            
            ToDo.objects(id=id).update(title=title, content=content, img=filename)
            
            return redirect('/')
                        
        return 'Task not found'
    else:
        task = ToDo.objects(id=id)[0]
        return render_template("update.html", task=task)

