import app
from PIL import Image


def resize_image():

    original_image = Image.open(r'D:\Py_projects\flask_prj\shop_app\app\static\img\default.png')
    resized_image = original_image.resize((200,200))
    resized_image.save('default.png')


a = [(1,'er'),(2,'poco')]
for b,c in a:
    print(b,c)