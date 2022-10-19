from flask import Flask,flash,make_response
from flask import render_template,request,redirect,url_for
from PIL import Image
import sys
from io import BytesIO
import requests
from chardet import detect
import base64
import cv2
import numpy as np
import matplotlib.pyplot as plt
import io
from werkzeug.utils import secure_filename
import json

def save_img(img_base64):
    #binary <- string base64
    img_binary = base64.b64decode(img_base64)
    #jpg <- binary
    img_jpg=np.frombuffer(img_binary, dtype=np.uint8)
    #raw image <- jpg
    img = cv2.imdecode(img_jpg, cv2.IMREAD_COLOR)
    #デコードされた画像の保存先パス
    image_file="/home/capture_img/images/img0000.jpg"
    #画像を保存
    cv2.imwrite(image_file, img)
    return "SUCCESS"

#AIのモデル関数
def model(img):
    return 50

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
def top():
    if request.method == 'POST':
        enc_data  = request.form
        for mykey in enc_data.values():
            enc_data_kai = mykey
        dec_data = base64.b64decode( enc_data_kai.split(',')[1] )
        dec_img  = Image.open(BytesIO(dec_data))
        dec_img.save("test222.png","PNG")
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
def result(result):
    return render_template('result.html',result=result)

@app.route("/dist",methods=['GET', 'POST'])
def dist():
    if request.method == 'POST':

        # ファイル部分があるかの確認
        if 'img' not in request.files:
            return redirect('/error')
        file = request.files['img']

        # ファイルが選択されていない場合
        if file.filename == '':
            flash('ファイルが選択されていません')
            return redirect('/')
        
        # ファイルの拡張子が適切な場合に保存
        if file and allowed_file(file.filename):
            img = Image.open(file)
            #img.save('./img/crop-img.png')
            result = model(img)
            return render_template('result.html',result=result) # back to mypage
    else:
        return render_template('dist.html')