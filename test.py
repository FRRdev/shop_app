image = open(r'D:\Py_projects\flask_prj\shop_app\app\static\img\mountains.jpg','rb').read()



from PIL import Image


def resize_image():

    original_image = Image.open(r'D:\Py_projects\flask_prj\shop_app\app\static\img\default.png')
    resized_image = original_image.resize((200,200))
    resized_image.save('default.png')


resize_image()
