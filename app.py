from __future__ import division, print_function
# coding=utf-8
import sys
import os
import glob
import re
import numpy as np

# Import the necessary packages
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input, decode_predictions

# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer

# Define a flask app
app = Flask(__name__)

# Model saved with Keras model.save()
MODEL_PATH = 'models/oxford_flowers_102_final_model.h5'

# Load your trained model
model = load_model(MODEL_PATH)
#model._make_predict_function()          # Necessary
#print('Model loaded. Start serving...')

print('Model loaded. Check http://127.0.0.1:5000/')

class_mappings = {'alpine sea holly': 0, 'anthurium': 1, 'artichoke': 2, 'azalea': 3, 'ball moss': 4, 'balloon flower': 5, 'barbeton daisy': 6, 'bearded iris': 7, 'bee balm': 8, 'bird of paradise': 9, 'bishop of llandaff': 10, 'black-eyed susan': 11, 'blackberry lily': 12, 'blanket flower': 13, 'bolero deep blue': 14, 'bougainvillea': 15, 'bromelia': 16, 'buttercup': 17, 'californian poppy': 18, 'camellia': 19, 'canna lily': 20, 'canterbury bells': 21, 'cape flower': 22, 'carnation': 23, 'cautleya spicata': 24, 'clematis': 25, 'colts foot': 26, 'columbine': 27, 'common dandelion': 28, 'corn poppy': 29, 'cyclamen': 30, 'daffodil': 31, 'desert-rose': 32, 'english marigold': 33, 'fire lily': 34, 'foxglove': 35, 'frangipani': 36, 'fritillary': 37, 'garden phlox': 38, 'gaura': 39, 'gazania': 40, 'geranium': 41, 'giant white arum lily': 42, 'globe thistle': 43, 'globe-flower': 44, 'grape hyacinth': 45, 'great masterwort': 46, 'hard-leaved pocket orchid': 47, 'hibiscus': 48, 'hippeastrum': 49, 'japanese anemone': 50, 'king protea': 51, 'lenten rose': 52, 'lotus': 53, 'love in the mist': 54, 'magnolia': 55, 'mallow': 56, 'marigold': 57, 'mexican aster': 58, 'mexican petunia': 59, 'monkshood': 60, 'moon orchid': 61, 'morning glory': 62, 'orange dahlia': 63, 'osteospermum': 64, 'oxeye daisy': 65, 'passion flower': 66, 'pelargonium': 67, 'peruvian lily': 68, 'petunia': 69, 'pincushion flower': 70, 'pink primrose': 71, 'pink-yellow dahlia?': 72, 'poinsettia': 73, 'primula': 74, 'prince of wales feathers': 75, 'purple coneflower': 76, 'red ginger': 77, 'rose': 78, 'ruby-lipped cattleya': 79, 'siam tulip': 80, 'silverbush': 81, 'snapdragon': 82, 'spear thistle': 83, 'spring crocus': 84, 'stemless gentian': 85, 'sunflower': 86, 'sweet pea': 87, 'sweet william': 88, 'sword lily': 89, 'thorn apple': 90, 'tiger lily': 91, 'toad lily': 92, 'tree mallow': 93, 'tree poppy': 94, 'trumpet creeper': 95, 'wallflower': 96, 'water lily': 97, 'watercress': 98, 'wild pansy': 99, 'windflower': 100, 'yellow iris': 101}
#print(class_mappings)

def model_predict(img_path, model) :
    # Load the image into Python
    test_image = image.load_img(img_path, target_size=(224, 224))

    # Convert the image to a matrix of numbers
    test_image = image.img_to_array(test_image)
    test_image = np.expand_dims(test_image, axis=0)
    test_image = preprocess_input(test_image)

    # Make predictions
    result = model.predict(test_image)

    return result

@app.route('/', methods=['GET'])
def index() :
    # Main page
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def upload() :
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)

        # Make prediction
        preds = model_predict(file_path, model)
        predicted_class_num = np.argmax(preds)
        predicted_class = list(class_mappings.keys())[list(class_mappings.values()).index(predicted_class_num)]
    
        return str(predicted_class)
    return None


if __name__ == '__main__':
    app.run(debug=True)