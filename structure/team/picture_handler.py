import os
# pip install pillow
from PIL import Image

from flask import url_for, current_app

def team_picture(pic_upload):

    filename = pic_upload.filename
    # Grab extension type .jpg or .png
    ext_type = filename.split('.')[-1]
    filen= filename.split('.')[0]
    storage_filename = filen + '.' +ext_type
    filepath = os.path.join(current_app.root_path, 'static/profile_pics', storage_filename)

    # Play Around with this size.
    output_size = (200, 200)

    # Open the picture and save it
    pic = Image.open(pic_upload)
    pic.thumbnail(output_size)
    pic.save(filepath)

    return storage_filename
