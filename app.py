import os
from flask import Flask, request, redirect, url_for, send_file
from werkzeug.utils import secure_filename
import subprocess

import torch

from modules.analyze_video import convert_mp4_to_pkl
from modules.fbx_output import convert_pkl_to_fbx

def makedirs(path): 
   try: 
        os.makedirs(path) 
   except OSError: 
       if not os.path.isdir(path): 
           raise

# 영상 분석시 영상 선택 및 경로, 옵션 지정
argv_mp4 = ['--vid_file', 'sample_video.mp4', '--output_folder', 'output/', '--no_render']
argv_pkl = ['python', 'modules/fbx_output.py','--input','output/sample_video/vibe_output.pkl', '--output',
            'output/sample_video/fbx_output.glb', '--fps_source', '30',
            '--fps_target', '30', '--gender', 'female', '--person_id', '1']

person_id = 1

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
            filepath_mp4 = 'videos' + '/' + filename

            # videos 폴더 유무 확인 후, 없으면 폴더 생성
            makedirs('videos')

            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # .mp4 to .pkl 변환 
            argv_mp4[1] = filepath_mp4
            convert_mp4_to_pkl(argv_mp4)

            # .pkl to .fbx 변환
            file_path_pkl = 'output' + '/' + filename.rsplit('.',1)[0] + '/' + 'vibe_output.pkl'
            file_path_fbx = 'output' + '/' + filename.rsplit('.',1)[0] + '/' + 'fbx_output.glb'

            argv_pkl[3] = file_path_pkl
            argv_pkl[5] = file_path_fbx
            global person_id
            argv_pkl[13] = str(person_id)
            person_id += 1

            p = subprocess.run(args=argv_pkl)
            torch.cuda.empty_cache()
            return send_file(file_path_fbx , mimetype = 'glb')
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4500)
