from flask import Flask, jsonify, request, render_template
import sqlite3
import pickle


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['GET','POST'])
def predict():
    if request.method == 'POST':
        pregnancies = int(request.form['pregnancies'])
        glucose = int(request.form['glucose'])
        blood_pressure = int(request.form['blood-pressure'])
        skin_thickness = int(request.form['skin-thickness'])
        insulin = int(request.form['insulin'])
        bmi = float(request.form['bmi'])
        diabetes_pedigree = float(request.form['diabetes-pedigree'])
        age = int(request.form['age'])
        data = [pregnancies,glucose,blood_pressure,skin_thickness,insulin,bmi,diabetes_pedigree,age]
        print(data)
        with open('model.pickle','rb') as file:
            model = pickle.load(file)
        result = model.predict([data])
        print(result)
        if result[0] == 0:
            outcome = 'No Diabetic'
        else:
            outcome = 'Diabetic Patient'
        print('Data has been Inserted')
        return jsonify({'message':outcome})
    else:
        return render_template('predict.html')

@app.route('/show-patient', methods = ['GET','POST'])
def showpatient():
    conn = sqlite3.connect('patient.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM PATIENT_DETAILS")
    data = []
    for i in cur.fetchall():
        patient = {}
        patient['name'] = i[0]
        patient['age'] = i[1]
        patient['gender'] = i[2]
        patient['result'] = i[3]
        data.append(patient)
    return render_template('showpatient.html',data = data)

@app.route("/insert-patient", methods=['GET','POST'])
def addpatient():
    if request.method=='POST':
        conn = sqlite3.connect('patient.db')
        cur = conn.cursor()
        Patient_Name=request.form.get('Patient_Name')
        Patient_Age=request.form.get('Patient_Age')
        gender=request.form.get('gender')
        Result_diabetic=request.form.get('Result_diabetic')
        cur.execute(f"insert into PATIENT_DETAILS(PATIENT_NAME,PATIENT_AGE,GENDER,DIABETIC) values('{Patient_Name}',{Patient_Age},'{gender}','{Result_diabetic}')")
        conn.commit()
        print('Data as been Inserted')
        return jsonify({'message':'sucessfull'})
    else:
        return render_template('insertpatient.html')
    
if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=False,port=5000)