import imp
from flask import Flask,render_template,request
from PIL import Image
from io import BytesIO
import base64
from inference import output_result
from ml_model import Net



#AIのモデル関数
def model():
    outputs = output_result('./static/img/predict_img.png')
    #print(outputs[0][0].item(), outputs[0][1].item())
    ai_gererate_prob = outputs[0][0].item()
    return ai_gererate_prob

def model_temp():
    return 50

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/crop', methods=['GET', 'POST'])  # type: ignore
def crop():
    if request.method == 'POST':
        form  = request.form
        for value in form.values():
            data = value
        spl_data = base64.b64decode(data.split(',')[1])
        dec_img  = Image.open(BytesIO(spl_data))
        dec_img.save("./static/img/predict_img.png","PNG")
        return
    else:
        return render_template('crop.html')

@app.route("/error")
def error():
    return render_template('error.html')

@app.route("/result")
def result():
    #img = Image.open("./static/img/predict_img.png")
    #result = model(img)
    #result = model_temp()
    result = model()
    return render_template('result.html',result=result)