from datetime import datetime
from mongoengine import Document
from mongoengine.fields import (
    DateTimeField, StringField
)
class ToDo(Document):
    title = StringField(max_length=60, required=True)
    content = StringField(max_length=200)
    img = StringField()
    created = DateTimeField(default=datetime.now)
    color = StringField()

    # def __repr__(self):
    #     return self