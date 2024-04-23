import os
import jwt
import pydub
from flask import (
        Flask, request, jsonify, redirect,
        render_template, make_response,
        send_from_directory)
from functools import wraps
from pydub import AudioSegment
from werkzeug.utils import secure_filename

from db import Database
from logic import prng, now_time


app = Flask(__name__)
# an web application's configuration
app.config['SECRET_KEY'] = 'secret_key'
app.config['UPLOAD_DIR'] = 'uploads'

db = Database('users.db')
with app.app_context():
    db.create_tables()


def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.cookies.get('token') or \
                request.headers.get('Authorization')

        # BUG: if dd an any token, all be correct
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'],
                              algorithms=['HS256'])
            username = data['username']
            user_token = db.get_token(username)
            if user_token != token or user_token is None:
                return jsonify({'message': 'Token is missing'}), 401
        except Exception:
            return jsonify({'message': 'Invalid token'}), 401
        return f(username, *args, **kwargs)
    return decorated_function


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/uploads/<path:filename>')
def download_file(filename):
    upload_dir = app.config['UPLOAD_DIR']
    return send_from_directory(upload_dir, filename)

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
    return render_template('tracks.html', tracks=tracks_list)


@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    user = db.get_user(username)
    if not user:
        return jsonify({'message': 'Invalid username or password'}), 401

    if not user[2] == password:
        return jsonify({'message': 'Invalid username or password'})
    token = jwt.encode({'username': username}, app.config['SECRET_KEY'],
                       algorithm='HS256')

    # Save token in a db for an user
    db.update_user_token(username, token)
    response = make_response(redirect('/'))
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
@token_required
def audio_edit(username):
    data = request.get_json()
    track_name = data.get('track_name')
    begin = int(data.get('begin'))
    end = int(data.get('end'))

    track_extension = os.path.splitext(track_name)[1]

    begin, end = begin * 1000, end * 1000
    if track_extension == '.wav':
        audio = pydub.AudioSegment.from_wav(track_name)
    elif track_extension == '.mp3':
        audio = pydub.AudioSegment.from_mp3(track_name)
    else:
        return jsonify({'message': 'A format file doesn\'t support'})

    cropped_audio = audio[begin:end]

    user_dir = db.get_user_dir(username)
    upload_dir = app.config['UPLOAD_DIR']
    save_dir = os.path.join(upload_dir, user_dir)
    os.chdir(save_dir)

    track_name = f'edited{now_time()}{track_extension}'

    cropped_audio.export(track_name, format='mp3')
    return jsonify({'succes': 'The file was edited'})

    
@app.route('/upload_audio', methods=['POST'])
@token_required
def upload_audio(username):
    """Upload a file to the disk.
    1. If an user has a directory -  it will be used.
    2. If the directory does't exist, it will be created and added to the DB.
    For each file, a random fake name will be generated; the real name
    will be added to the database, but only for view on a page."""

    upload_dir = app.config['UPLOAD_DIR']
    if not os.path.isdir(upload_dir):
        os.mkdir(upload_dir)

    file = request.files['file']
    if file.filename == '':
        return json({'error': 'No selected file'})

    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file_extension = file.filename.rsplit('.', 1)[1].lower()

    if not file_extension in ('mp3', 'wav'):
        return jsonify({'error': 'Invalid file format. Only mp3, wav'})
    filename = secure_filename(file.filename)
    # Get user's directory; create it if it doesn't exist.
    user_dir = db.get_user_dir(username)
    if user_dir is None:
        user_dir = prng(16)
        upload_dir = os.path.join(upload_dir, user_dir)
        os.mkdir(upload_dir)
        db.set_user_dir(username, user_dir)
    else:
        upload_dir = os.path.join(upload_dir, user_dir)

    # Create a random file name for the track
    fake_name = f'{prng(10)}.{file_extension}'
    if os.path.isfile(filename):
        fake_name = prng(10)
    path = os.path.join(upload_dir, fake_name)
    db.add_track(username, filename, fake_name, path)
    file.save(path)
    return jsonify({"success": "Audio uploaded successfully"})



if __name__ == "__main__":
    app.run(debug=True)
