from flask import Flask
from flask import Flask,flash
from flask import render_template,request,redirect,url_for
from PIL import Image
import requests
from io import BytesIO


# ファイル拡張子の判定
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/top', methods=['GET', 'POST'])  # type: ignore
def post():
    if request.method == 'POST':
        enc_data  = request.form['img']
        dec_data = base64.b64decode( enc_data.split(',')[1] ) # 環境依存の様(","で区切って本体をdecode)
        #dec_data = base64.b64decode(enc_data)
        dec_img  = Image.open(BytesIO(dec_data))
        dec_img.save("test.png")

        """
        blob  = request.form['blob']
        #response = requests.get(url)
        #img = Image.open(url)
        ###追加###
        with open(blob, 'br') as f:
            img = f.read()
        ###
        img.save("test.png")
        """
        return redirect('/test')
    else:
        return render_template('top.html')


@app.route("/test")
def test():
    return render_template('test.html')

@app.route("/error")
def error():
    return render_template('error.html')

@app.route("/result")
def result():
    return render_template('result.html')

###追加###
import base64
from io import BytesIO
@app.route("/img_post", methods=['POST'])
def set_data():
    enc_data  = request.form['img']
    #dec_data = base64.b64decode( enc_data )              # これではエラー  下記対応↓
    #dec_data = base64.b64decode( enc_data.split(',')[1] ) # 環境依存の様(","で区切って本体をdecode)
    #dec_img  = Image.open(BytesIO(dec_data))
    return render_template('test.html')
###追加###