import os
import sys
import json
from flask import Flask, render_template, request
import pickle
import numpy as np
from werkzeug.wsgi import wrap_file

# Get root directory
BASEDIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

# Initialize Flask app
app = Flask(__name__, 
            template_folder=os.path.join(BASEDIR, 'templates'),
            static_folder=os.path.join(BASEDIR, 'static'),
            static_url_path='/static')

# Load model
model = None
try:
    model_path = os.path.join(BASEDIR, 'thyroid.pkl')
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
except Exception as e:
    print(f"Warning: Could not load model: {e}")

def predict_thyroid(age=34, gender='F', smoking='No', hx_smoking='No', hx_radiotherapy='No', 
                    thyroid_function='Euthyroid', physical_examination='Single nodular goiter-righ', 
                    Adenopathy='No', Pathology='Micropapillary', Focality='Uni-Focal', risk='Low', 
                    T='T1a', N='N0', M='M0', Stage='1', Response='Indeterminate'):
    temp = []
    
    if gender == 'F':
        temp += [1, 0]
    else:
        temp += [0, 1]
    
    if smoking == 'No':
        temp += [1, 0]
    else:
        temp += [0, 1]
    
    if hx_smoking == 'No':
        temp += [1, 0]
    else:
        temp += [0, 1]
    
    if hx_radiotherapy == 'No':
        temp += [1, 0]
    else:
        temp += [0, 1]
    
    if thyroid_function == 'Clinical Hypothyroidism':
        temp += [1, 0, 0, 0]
    elif thyroid_function == 'Euthyroid':
        temp += [0, 1, 0, 0]
    elif thyroid_function == 'Subclinical Hyperthyroidism':
        temp += [0, 0, 1, 0]
    else:
        temp += [0, 0, 0, 1]
    
    if physical_examination == 'Diffuse goiter':
        temp += [1, 0, 0, 0, 0]
    elif physical_examination == 'Multinodular goiter':
        temp += [0, 1, 0, 0, 0]
    elif physical_examination == 'Normal':
        temp += [0, 0, 1, 0, 0]
    elif physical_examination == 'Single nodular goiter-left':
        temp += [0, 0, 0, 1, 0]
    else:
        temp += [0, 0, 0, 0, 1]
    
    if Pathology == 'Follicular':
        temp += [1, 0, 0, 0]
    elif Pathology == 'Hurthel cell':
        temp += [0, 1, 0, 0]
    elif Pathology == 'Micropapillary':
        temp += [0, 0, 1, 0]
    else:
        temp += [0, 0, 0, 1]

    if risk == 'High':
        temp += [1, 0, 0]
    elif risk == 'Intermediate':
        temp += [0, 1, 0]
    else:
        temp += [0, 0, 1]
    
    if Stage == '1':
        temp += [1, 0, 0, 0]
    elif Stage == '2':
        temp += [0, 1, 0, 0]
    elif Stage == '3':
        temp += [0, 0, 1, 0]
    elif Stage == '4a':
        temp += [0, 0, 0, 1]
    else:
        temp += [0, 0, 0, 1]
    
    if Response == 'Biochemical Incomplete':
        temp += [1, 0, 0, 0]
    elif Response == 'Excellent':
        temp += [0, 1, 0, 0]
    elif Response == 'Subclinical Indeterminate':
        temp += [0, 0, 1, 0]
    else:
        temp += [0, 0, 0, 1]
    
    if Adenopathy == 'No':
        temp += [3]
    elif Adenopathy == 'Right':
        temp += [5]
    elif Adenopathy == 'Extensive':
        temp += [1]
    elif Adenopathy == 'Left':
        temp += [2]
    elif Adenopathy == 'Bilateral':
        temp += [0]
    else:
        temp += [4]
    
    if Focality == 'Uni-Focal':
        temp += [1]
    else:
        temp += [0]
    
    if T == 'T1a':
        temp += [0]
    elif T == 'T1b':
        temp += [1]
    elif T == 'T2':
        temp += [2]
    elif T == 'T3a':
        temp += [3]
    elif T == 'T3b':
        temp += [4]
    elif T == 'T4a':
        temp += [5]
    else:
        temp += [6]
    
    if N == 'N0':
        temp += [0]
    elif N == 'N1b':
        temp += [2]
    else:
        temp += [1]
    
    if M == 'M0':
        temp += [0]
    else:
        temp += [1]

    temp += [age]
    temp = np.array([temp])
    
    if model is not None:
        pred = model.predict(temp)
        return "Yes" if pred[0] == 1 else "No"
    return "Error"

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def catch_all(path):
    """Catch all routes and handle them appropriately"""
    if path == "" or path == "/":
        return render_template('index.html')
    elif path == "predict":
        if request.method == 'POST':
            try:
                age = int(request.form.get('age', 34))
                gender = request.form.get('gender', 'F')
                smoking = request.form.get('smoking', 'No')
                hx_smoking = request.form.get('hx_smoking', 'No')
                hx_radiotherapy = request.form.get('hx_radiothreapy', 'No')
                thyroid_function = request.form.get('thyroid_function', 'Euthyroid')
                physical_examination = request.form.get('physical_examination', 'Single nodular goiter-righ')
                Adenopathy = request.form.get('Adenopathy', 'No')
                Pathology = request.form.get('Pathology', 'Micropapillary')
                Focality = request.form.get('Focality', 'Uni-Focal')
                risk = request.form.get('risk', 'Low')
                T = request.form.get('T', 'T1a')
                N = request.form.get('N', 'N0')
                M = request.form.get('M', 'M0')
                Stage = request.form.get('Stage', '1')
                Response = request.form.get('Response', 'Indeterminate')
                
                pred = predict_thyroid(age=age, gender=gender, smoking=smoking, 
                                       hx_smoking=hx_smoking, hx_radiotherapy=hx_radiotherapy,
                                       thyroid_function=thyroid_function, 
                                       physical_examination=physical_examination,
                                       Adenopathy=Adenopathy, Pathology=Pathology, 
                                       Focality=Focality,
                                       risk=risk, T=T, N=N, M=M, Stage=Stage, 
                                       Response=Response)
                return render_template('result.html', Prediction=pred)
            except Exception as e:
                return f"Error: {str(e)}", 500
        return render_template('prediction.html')
    elif path.startswith('static/'):
        # Serve static files
        return app.send_static_file(path[7:])
    else:
        return "Not Found", 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
