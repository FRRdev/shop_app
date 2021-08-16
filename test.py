import app
from PIL import Image


def resize_image():

    original_image = Image.open(r'D:\Py_projects\flask_prj\shop_app\app\static\img\default.png')
    resized_image = original_image.resize((200,200))
    resized_image.save('default.png')

from flask_mail import Message
from app import mail
msg = Message('test subject', sender='mixail.critsyn@mail.ru',recipients=['mkritsyn@fromtech.ru'])
msg.body = 'test body'
msg.html = '<h1>HTML body</h1>'
mail.send(msg)