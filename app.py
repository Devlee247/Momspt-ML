import os
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename

import argparse

from modules.analyze_video import convert_mp4_to_pkl
from modules import fbx_output

# 영상 분석시 영상 선택 및 경로, 옵션 지정
argv = ['--vid_file', 'sample_video.mp4', '--output_folder', 'output/', '--no_render']

UPLOAD_FOLDER = os.getcwd() + '/' + 'videos' # 영상 업로드 위치
ALLOWED_EXTENSIONS = {'mp4'} # 허용되는 영상 확장자

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 올바른 확장자 명을 가지고 있는지 확인
def allowd_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

'''
기본 라우트
'''
@app.route("/")
def hello_world():
    return "Hello, World!"

'''
파일을 업로드 할 수 있는 route
'''
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        
        # post request에 파일 부분이 있는지 확인
        if 'file' not in request.files:
            print('No file part')
            return redirect(request.url)
        file = request.files['file']
        
        # 파일을 선택하였는지 확인
        if file.filename == '':
            print('No selected file or uncorrect file')
            return redirect(request.url)

        # 파일 존재유무 확인 및 허가된 확장자명인지 확인
        if file and allowd_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = 'videos' + '/' + filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            # .mp4 to .pkl 변환 
            argv[1] = filepath
            convert_mp4_to_pkl(argv)
            print(request.url)
            return redirect(request.url)
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''
