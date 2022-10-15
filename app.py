from flask import Flask
from flask import Flask,flash
from flask import render_template,request,redirect

# ファイル拡張子の判定
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

def model(img):
    return 1

app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/top', methods=['GET', 'POST'])  # type: ignore
def post():
    if request.method == 'POST':
        # ファイル部分があるかの確認
        if 'photo' not in request.files:
            return redirect('/error')
        img = request.files['photo']

        # ファイルの拡張子が適切な場合にモデルに渡す
        if img and allowed_file(img.filename):
            result = model(img)
            return redirect('/result',result)
        else:
            flash('png、jpg、jpeg形式のファイルを選択してください')
            return redirect(request.url)
    else:
        return render_template('top.html')

@app.route("/error")
def error():
    return render_template('error.html')

@app.route("/result")
def result():
    return render_template('result.html')

