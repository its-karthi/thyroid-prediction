from flask import Flask, render_template, request
import pickle 
import numpy as np

app=Flask(__name__)

with open("thyroid.pkl","rb")as f:
    model=pickle.load(f)

def predict_thyroid(age=34,gender='F',smoking='No',hx_smoking='No',hx_radiotherapy='No',thyroid_function='Euthyroid',physical_examination='Single nodular goiter-righ',Adenopathy='No',Pathology='Micropapillary',Focality='Uni-Focal',risk='Low',T='T1a',N='N0',M='M0',Stage='1',Response='Indeterminate'):
   temp=list()
   if gender=='F':
      temp=temp+[1,0]
   else:
      temp=temp+[0,1]
   
   if smoking=='No':
      temp=temp+[1,0]
   else:
      temp=temp+[0,1]
   
   if hx_smoking=='No':
      temp=temp+[1,0]
   else:
      temp=temp+[0,1]
   
   if hx_radiotherapy=='No':
      temp=temp+[1,0]
   else:
      temp=temp+[0,1]
   
   if thyroid_function=='Clinical Hypothyroidism':
      temp=temp+[1,0,0,0]
   elif thyroid_function=='Euthyroid':
      temp=temp+[0,1,0,0]
   elif thyroid_function=='Subclinical Hyperthyroidism':
      temp=temp+[0,0,1,0]
   else:
      temp=temp+[0,0,0,1]
   
   if physical_examination=='Diffuse goiter':
      temp=temp+[1,0,0,0,0]
   elif physical_examination=='Multinodular goiter':
      temp=temp+[0,1,0,0,0]
   elif physical_examination=='Normal':
      temp=temp+[0,0,1,0,0]
   elif physical_examination=='Single nodular goiter-left':
      temp=temp+[0,0,0,1,0]
   else:
      temp=temp+[0,0,0,0,1]
   
   if Pathology=='Follicular':
      temp=temp+[1,0,0,0]
   elif Pathology=='Hurthel cell':
      temp=temp+[0,1,0,0]
   elif Pathology=='Micropapillary':
      temp=temp+[0,0,1,0]
   else:
      temp=temp+[0,0,0,1]

   if risk=='High':
      temp=temp+[1,0,0]
   elif risk=='Intermediate':
      temp=temp+[0,1,0]
   else:
      temp=temp+[0,0,1]
   
   if Stage=='1':
      temp=temp+[1,0,0,0]
   elif Stage=='2':
      temp=temp+[0,1,0,0]
   elif Stage=='3':
      temp=temp+[0,0,1,0]
   elif Stage=='4a':
      temp=temp+[0,0,0,1]
   else:
      temp=temp+[0,0,0,1]
   
   if Response=='Biochemical Incomplete':
      temp=temp+[1,0,0,0]
   elif Response=='Excellent':
      temp=temp+[0,1,0,0]
   elif Response=='Subclinical Indeterminate':
      temp=temp+[0,0,1,0]
   else:
      temp=temp+[0,0,0,1]
   

   if Adenopathy=='No':
      temp=temp+[3]
   elif Adenopathy=='Right':
      temp=temp+[5]
   elif Adenopathy=='Extensive':
      temp=temp+[1]
   elif Adenopathy=='Left':
      temp=temp+[2]
   elif Adenopathy=='Bilateral':
      temp=temp+[0]
   else:
      temp=temp+[4]
   
   if Focality=='Uni-Focal':
      temp=temp+[1]
   else:
      temp=temp+[0]
   
   if T=='T1a':
      temp=temp+[0]
   elif T=='T1b':
      temp=temp+[1]
   elif T=='T2':
      temp=temp+[2]
   elif T=='T3a':
      temp=temp+[3]
   elif T=='T3b':
      temp=temp+[4]
   elif T=='T4a':
      temp=temp+[5]
   else:
      temp=temp+[6]
               
   if N=='N0':
      temp=temp+[0]
   elif N=='N1b':
      temp=temp+[2]
   else:
      temp=temp+[1]
               
   if M=='M0':
      temp=temp+[0]
   else:
      temp=temp+[1]

#age 
   temp=temp+[age]


   temp=np.array([temp])
   print(temp)
   pred=model.predict(temp)
   print(pred)
   if pred[0]==0:
      result="No"
      return result
   else:
      result="Yes"
      return result
   




@app.route("/")
def index():
    return render_template('index.html')

@app.route("/predict",methods=['GET','POST'])
def predict():
    if request.method=='POST':
        age = int(request.form.get('age'))
        gender = request.form.get('gender')
        smoking = request.form.get('smoking')
        hx_smoking = request.form.get('hx_smoking')
        hx_radiotherapy = request.form.get('hx_radiothreapy')
        thyroid_function = request.form.get('thyroid_function')
        physical_examination = request.form.get('physical_examination')
        Adenopathy = request.form.get('Adenopathy')
        Pathology = request.form.get('Pathology')
        Focality = request.form.get('Focality')
        risk = request.form.get('risk')
        T = request.form.get('T')
        N = request.form.get('N')
        M = request.form.get('M')
        Stage = request.form.get('Stage')
        Response = request.form.get('Response')
        
        pred=predict_thyroid(age=age,gender=gender,smoking=smoking,hx_smoking=hx_smoking,hx_radiotherapy=hx_radiotherapy,thyroid_function=thyroid_function,physical_examination=physical_examination,Adenopathy=Adenopathy,Pathology=Pathology,Focality=Focality,risk=risk,T=T,N=N,M=M,Stage=Stage,Response=Response)
        print(pred)
        return render_template('result.html',
                               Prediction=pred)
    return render_template('prediction.html')

if __name__=='__main__':
    app.run(debug=True,port=4500, host="0.0.0.0")
