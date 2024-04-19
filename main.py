import os
import jwt
import pydub
from flask import (
        Flask, request, jsonify, redirect,
        render_template, make_response)
from db import Database
from functools import wraps
from pydub import AudioSegment
from werkzeug.utils import secure_filename


app = Flask(__name__)
# an web application's configuration
app.config['SECRET_KEY'] = 'secret_key'
app.add_url_rule('/uploads/<path:filename>', endpoint='uploads',
                 view_func=app.send_static_file)
UPLOAD_DIR = 'uploads'
db = Database('users.db')
with app.app_context():
    db.create_tables()


def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.cookies.get('token') or \
                request.headers.get('Authorization')

        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'],
                              algorithms=['HS256'])
            username = data['username']
        except Exception:
            return jsonify({'message': 'Invalid token'}), 401
        return f(username, *args, **kwargs)
    return decorated_function


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.errorhandler(404)
def page_not_found(error):
    '''
    Display error page for 404 error
    '''
    return render_template('error.html'), 404


@app.route('/tracks', methods=['GET'])
@token_required
def get_library(username):
    tracks = db.get_tracks(username)
    tracks_list = [dict(track) for track in tracks]
    print(tracks_list)
    return render_template('tracks.html', tracks=tracks_list)


@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    user = db.get_user(username)
    if not user:
        return jsonify({'message': 'Invalid username or password'}), 401

    if not user[2] == password:
        return jsonify('Invalid username or password')
    token = jwt.encode({'username': username}, app.config['SECRET_KEY'],
                       algorithm='HS256')

    # Save token in a db for an user
    db.update_user_token(username, token)
    response = make_response(redirect('/index'))
    response.set_cookie('token', token)
    return response


@app.route('/create_account', methods=['POST'])
def create_account():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')

    if len(password) < 6:
        return jsonify({"message": "A password weak"})

    if username == password:
        return jsonify({"message": "A password equals username. Forbidden"})
    db.insert_user(username, password, email)
    return jsonify({"message": "Account created successfully"})


@app.route('/audio_edit', methods=['POST'])
def audio_edit():
    track_name = request.form.get('track_name')
    begin = request.form.get('begin')
    end = request.form.get('end')
    print(track_name)

    track_extension = os.path.splitext(track_name)[1]

    begin, end = begin * 1000, end * 1000
    if track_extension == '.wav':
        audio = pydub.AudioSegment.from_wav(track_name)
    elif track_extension == '.mp3':
        audio = pydub.AudioSegment.from_mp3(track_name)
    else:
        return jsonify({'message': 'A format file doesn\'t support'})

    cropped_audio = audio[begin:end]
    cropped_audio.export(f'edited_{track_name}', format='mp3')


@app.route('/upload_audio', methods=['POST'])
@token_required
def upload_audio(username):
    if 'file' not in request.files:
        return 'No file part'

    file = request.files['file']

    if file.filename == '':
        return 'No selected file'

    file_extension = file.filename.rsplit('.', 1)[1].lower()
    if file_extension in ['mp3', 'wav']:
        filename = secure_filename(file.filename)
        path = os.path.join(UPLOAD_DIR, filename)
        file.save(path)
        db.add_track(username, 'Unknown', path)
        return jsonify({"message": "Audio uploaded successfully"})
    else:
        return 'Invalid file format. Please upload an image file.'


if __name__ == "__main__":
    app.run(debug=True)
