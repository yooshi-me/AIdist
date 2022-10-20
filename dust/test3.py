from PIL import Image
import random
import boto3
import base64
from io import BytesIO

s3 = boto3.client(
    's3',
    aws_access_key_id=app.config['AWS_ACCESS_KEY_ID'],
    aws_secret_access_key=app.config['AWS_SECRET_ACCESS_KEY']
    )

@users.route('/image',methods=['POST'])
@login_required
def image():
    if request.method == 'POST': 
        enc_data = request.form['image']
        dec_data = base64.b64decode(enc_data.split(',')[1]) # 環境依存の様(","で区切って本体をdecode)
        dec_img  = Image.open(BytesIO(dec_data))
        image = add_profile_pic(dec_img)
        image = "{}png".format(image)
        s3_resource = boto3.resource('s3')
        my_bucket = s3_resource.Bucket(app.config['AWS_BUCKET'])
        my_bucket.Object(image).put(Body=BytesIO(dec_data))
        image_url = 'https://'+str(app.config['AWS_BUCKET'])+'.s3-ap-northeast-1.amazonaws.com/{}'
        image_url = image_url.format(image)
        current_user.profile_image = image_url
        db.session.commit()
        return jsonify({'image': image_url})

def add_profile_pic(pic_upload):
    filename = pic_upload.filename
    ext_type = filename.split('.')[-1]
    suffix = datetime.now().strftime("%y%m%d_%H%M%S")
    s = 'abcdefghijklmnopqrstuvwxyz'
    result = "".join([random.choice(s) for x in range(10)])
    storage_filename = str(suffix)+str(result)+'.'+ext_type
    return storage_filename