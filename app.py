import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle

app = Flask(__name__)
model = pickle.load(open('model1.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/y_predict',methods=['POST'])
def y_predict():
    '''
    For rendering results on HTML GUI
    '''
    x_test = [[x for x in request.form.values()]]
    
    prediction = model.predict(x_test)
    print(prediction)
    output=prediction[0]
    if (output == 1):
        output = "diabetic patient"
    else:
        output = "not sick with diabetes"

    return render_template('index.html', 
  prediction_text=
  'the person who has this data is {}'.format(output))

if __name__ == "__main__":
    app.run(debug=True)
