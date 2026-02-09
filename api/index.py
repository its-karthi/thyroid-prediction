import os
import sys
from flask import Flask, render_template, request
import pickle
import numpy as np

# Get root directory (parent of api/)
BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASEDIR)

# Create Flask application
app = Flask(
    __name__,
    template_folder=os.path.join(BASEDIR, 'templates'),
    static_folder=os.path.join(BASEDIR, 'static'),
    static_url_path='/static'
)

# Load the model
model = None
try:
    with open(os.path.join(BASEDIR, 'thyroid.pkl'), 'rb') as f:
        model = pickle.load(f)
except Exception as e:
    print(f"Error loading model: {e}", file=sys.stderr)

def predict_thyroid(age=34, gender='F', smoking='No', hx_smoking='No', hx_radiotherapy='No',
                    thyroid_function='Euthyroid', physical_examination='Single nodular goiter-righ',
                    Adenopathy='No', Pathology='Micropapillary', Focality='Uni-Focal', risk='Low',
                    T='T1a', N='N0', M='M0', Stage='1', Response='Indeterminate'):
    temp = []
    
    # Gender encoding
    temp.extend([1, 0] if gender == 'F' else [0, 1])
    # Smoking encoding
    temp.extend([1, 0] if smoking == 'No' else [0, 1])
    # History of smoking encoding
    temp.extend([1, 0] if hx_smoking == 'No' else [0, 1])
    # History of radiotherapy encoding
    temp.extend([1, 0] if hx_radiotherapy == 'No' else [0, 1])
    
    # Thyroid function encoding
    if thyroid_function == 'Clinical Hypothyroidism':
        temp.extend([1, 0, 0, 0])
    elif thyroid_function == 'Euthyroid':
        temp.extend([0, 1, 0, 0])
    elif thyroid_function == 'Subclinical Hyperthyroidism':
        temp.extend([0, 0, 1, 0])
    else:
        temp.extend([0, 0, 0, 1])
    
    # Physical examination encoding
    if physical_examination == 'Diffuse goiter':
        temp.extend([1, 0, 0, 0, 0])
    elif physical_examination == 'Multinodular goiter':
        temp.extend([0, 1, 0, 0, 0])
    elif physical_examination == 'Normal':
        temp.extend([0, 0, 1, 0, 0])
    elif physical_examination == 'Single nodular goiter-left':
        temp.extend([0, 0, 0, 1, 0])
    else:
        temp.extend([0, 0, 0, 0, 1])
    
    # Pathology encoding
    if Pathology == 'Follicular':
        temp.extend([1, 0, 0, 0])
    elif Pathology == 'Hurthel cell':
        temp.extend([0, 1, 0, 0])
    elif Pathology == 'Micropapillary':
        temp.extend([0, 0, 1, 0])
    else:
        temp.extend([0, 0, 0, 1])
    
    # Risk encoding
    if risk == 'High':
        temp.extend([1, 0, 0])
    elif risk == 'Intermediate':
        temp.extend([0, 1, 0])
    else:
        temp.extend([0, 0, 1])
    
    # Stage encoding
    if Stage == '1':
        temp.extend([1, 0, 0, 0])
    elif Stage == '2':
        temp.extend([0, 1, 0, 0])
    elif Stage == '3':
        temp.extend([0, 0, 1, 0])
    else:
        temp.extend([0, 0, 0, 1])
    
    # Response encoding
    if Response == 'Biochemical Incomplete':
        temp.extend([1, 0, 0, 0])
    elif Response == 'Excellent':
        temp.extend([0, 1, 0, 0])
    elif Response == 'Subclinical Indeterminate':
        temp.extend([0, 0, 1, 0])
    else:
        temp.extend([0, 0, 0, 1])
    
    # Adenopathy encoding
    adenopathy_map = {'No': 3, 'Right': 5, 'Extensive': 1, 'Left': 2, 'Bilateral': 0}
    temp.append(adenopathy_map.get(Adenopathy, 4))
    
    # Focality encoding
    temp.append(1 if Focality == 'Uni-Focal' else 0)
    
    # T stage encoding
    t_map = {'T1a': 0, 'T1b': 1, 'T2': 2, 'T3a': 3, 'T3b': 4, 'T4a': 5}
    temp.append(t_map.get(T, 6))
    
    # N stage encoding
    n_map = {'N0': 0, 'N1a': 1, 'N1b': 2}
    temp.append(n_map.get(N, 1))
    
    # M stage encoding
    temp.append(0 if M == 'M0' else 1)
    
    # Age
    temp.append(age)
    
    # Make prediction
    temp_array = np.array([temp])
    if model is not None:
        try:
            pred = model.predict(temp_array)
            return "Yes" if pred[0] == 1 else "No"
        except Exception as e:
            return f"Prediction error: {str(e)}"
    return "Model not loaded"

# Routes
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
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
            
            prediction = predict_thyroid(
                age=age, gender=gender, smoking=smoking,
                hx_smoking=hx_smoking, hx_radiotherapy=hx_radiotherapy,
                thyroid_function=thyroid_function, physical_examination=physical_examination,
                Adenopathy=Adenopathy, Pathology=Pathology, Focality=Focality,
                risk=risk, T=T, N=N, M=M, Stage=Stage, Response=Response
            )
            return render_template('result.html', Prediction=prediction)
        except Exception as e:
            return f"Error processing form: {str(e)}", 500
    return render_template('prediction.html')

# For local testing
if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
