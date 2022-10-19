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
        #enc_data = request.form.get('blob')
        print("ここまで実行されました2")
        #msg = save_img(request.form["img"])
        #return make_response(msg)
        #print(request.form.getlist('blob'))
        #print(request.form["blob"][0])

        #tmp = dict(request.form)
        enc_data  = request.form
        for mykey in enc_data.values():
            #print(mykey)
            enc_data_kai = mykey
        #print(enc_data_kai)
        dec_data = base64.b64decode( enc_data_kai.split(',')[1] )
        dec_img  = Image.open(BytesIO(dec_data))
        #print(enc_data[1])
        #dec_data = base64.b64decode( enc_data.split(',')[1] ) # 環境依存の様(","で区切って本体をdecode)
        #dec_img  = Image.open(BytesIO(dec_data))
        #print(tmp)
        #json_load = json.load(tmp)
        #print(type(json_load))
        #for mykey in tmp.keys():
            #print(mykey)
        #    enc_data=bytes(mykey, 'utf-8')
        #img_np = np.array(enc_data)
        #img_np = img_np.astype(np.uint8)
        #print(img_np.dtype)
        #dec_data = img_np.tobytes()
        #print(dec_data[:10])
        #plt.imshow(np.frombuffer(dec_data, dtype = np.uint8).reshape(img_np.shape))
        #plt.title("バイナリ->numpy array")
        #plt.show()
        #print(dec_data)
        #dataBytesIO = io.BytesIO(dec_data)
        #print(dataBytesIO.getvalue())
        #dec_img  = Image.open(dataBytesIO)
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