from flask import Flask
from flask import Flask,flash
from flask import render_template,request,redirect,url_for

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
        return redirect(url_for('test'))
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
from PIL import Image
from io import BytesIO
@app.route("/img_post", methods=['POST'])
def set_data():
    enc_data  = request.form['img']
    #dec_data = base64.b64decode( enc_data )              # これではエラー  下記対応↓
    #dec_data = base64.b64decode( enc_data.split(',')[1] ) # 環境依存の様(","で区切って本体をdecode)
    #dec_img  = Image.open(BytesIO(dec_data))
    return render_template('test.html')
###追加###