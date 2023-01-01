import joblib
import pandas
import statsmodels.formula.api as smf
import subprocess
from graphing import *
import csv
from flask import Flask,jsonify, render_template, request
# from flask import Flask, 
from flask_cors import CORS, cross_origin


def load_model_and_predict(harness_size):   
    model_filename = './avalanche_dog_boot_model.pkl'
    
    loaded_model = joblib.load(model_filename)
    print("We've loaded a model with the following parameters:")
    print(loaded_model.params)
    inputs = {"harness_size": [harness_size]}
    predicted_boot_size = loaded_model.predict(inputs)[0]
    return predicted_boot_size


def check_size_of_boots(selected_harness_size, selected_boot_size):

    estimated_boot_size = load_model_and_predict(selected_harness_size)
    estimated_boot_size = int(round(estimated_boot_size))

    if selected_boot_size == estimated_boot_size:
        return {'flag': 0, 'message': f"Great choice! We think these boots and harness pair will fit your avalanche dog well."}

    if selected_boot_size < estimated_boot_size:
        return {'flag': -1,'message': "The boots and harness pair you have selected might be TOO SMALL for a dog as "\
               f"big as yours. We recommend a doggy boots size of {estimated_boot_size}."}

    if selected_boot_size > estimated_boot_size:
        return {'flag': 1,'message': "The boots and harness pair you have selected might be TOO BIG for a dog as "\
               f"small as yours. We recommend a doggy boots size of {estimated_boot_size}."}

app = Flask(__name__)
CORS(app, support_credentials=True)


@app.route("/predict",methods=['GET'])
@cross_origin(supports_credentials=True)
def predict():
    boot = int(request.args.get('b'))
    harness = int(request.args.get('h'))
    print('Input: ',boot,' | ',harness)
    x = check_size_of_boots(
        selected_harness_size=harness, selected_boot_size=boot)
    print(x,'\n')
    return x


if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=5000)
