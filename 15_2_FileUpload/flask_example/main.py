import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from flask import send_from_directory

UPLOAD_FOLDER = 'C:\\temp\\flask_example\\uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config key값에 대하여 값을 넣을 수 있음
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024     # 16 MB, byte 단위
app.secret_key = 'super secret key'

# Ref.: https://flask.readthedocs.io/en/latest/patterns/fileuploads/


# image.JPG --> JPG --> jpg 
def allowed_file(filename): # 업로드 할 때 확장자 제한 체크 함수
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':                
        if 'file' not in request.files:
            # input type file이 있는 지 물어봄
            app.logger.debug('No file part')
            return redirect(request.url) # 전 단계의 url 이 뭔지 알려줌
            # return redirect(url_for('upload_file')) // 루트로 들어가는것
        file = request.files['file']

        if file.filename == '': # 파일명이 없다는거는 보낸것이 없다는것, 파일안보냈을 때 에러처리
            app.logger.debug('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename): 
            filename = secure_filename(file.filename) # 여기서 한글이 깨짐
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename)) # form tag에서 받아온 binary Data를 임시로 저장함
            return redirect(url_for('uploaded_file', filename=filename))
    return '''
    <!doctype html>
    <meta charset="UTF-8">
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method="post" enctype="multipart/form-data">
      <input type="file" name="file">
      <input type="submit" value="Upload">
    </form>
    '''

    # enctype multipart/form-data 파일업로드 할 때 사용

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    # 파일디렉토리 위치, 실제 파일명 결합해서 제공

if __name__ == '__main__':    
    app.run(host='0.0.0.0', port=5000, debug=True)

