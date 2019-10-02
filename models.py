from mongoengine import Document, StringField, IntField, DateField, ImageField
from datetime import datetime
from flask_pymongo import PyMongo


class ToDo(Document):
    id = IntField(primary_key=True)
    title = StringField(max_length=60, required=True)
    content = StringField(max_length=200)
    image = ImageField(size=2000)
    created = DateField(default=datetime.utcnow)

    def __repr__(self):
        return self.id
