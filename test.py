import re

from config import app_dir
import os
from PIL import Image


def resize_image():

    original_image = Image.open(r'D:\Py_projects\flask_prj\shop_app\app\static\img\default.png')
    resized_image = original_image.resize((200,200))
    resized_image.save('default.png')

file = 'poco'
print(os.path.join(app_dir,file))