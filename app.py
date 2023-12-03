from email.policy import default
from urllib import response
from flask import Response, request
import flask
import sys
import os
import tempfile

app = flask.Flask(__name__)

projects = {}

tmp_file = tempfile.TemporaryDirectory()
app.config['UPLOAD_FOLDER'] = "\\data"

@app.route('/index')
@app.route('/')
def index():
    return flask.render_template('index.html', projects=projects)

@app.route('/<user>/upload', methods=['GET', 'POST'])
def upload(user):
    return Response('Service Unavailable', 503)
    if "GET" == request.method:
        return flask.render_template('upload.html')
    file = flask.request.files['file']
    
    try: open(f'{app.config['UPLOAD_FOLDER']}\\{user}\\{file.filename}', 'x').close()
    except FileExistsError: pass
    file.save(f'{app.config['UPLOAD_FOLDER']}\\{user}\\{file.filename}')
    return 'OK'

@app.route('/file/<filename>')
def get_file(filename):
    user = request.args.get('user', default='default', type=str)
    if not os.path.exists(f'{app.config["UPLOAD_FOLDER"]}\\{user}\\{filename}'):
        return 'File not found', 404
    with open(f'{app.config['UPLOAD_FOLDER']}\\{user}\\{filename}', 'rb') as f:
        return f.read()

host = '0.0.0.0'
port = 80
if len(sys.argv) > 1:
    HaP = sys.argv[1].split(':')
    host = HaP[0]
    port = HaP[1]

try:
    app.run(host=host, port=port, debug=True) # type: ignore
except Exception:
    pass
finally:
    tmp_file.cleanup()