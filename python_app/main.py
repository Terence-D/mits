#import nfo
import jellyfinApi
import mitsCommon
import mitsData
import os
import datetime

import flask
import flask_login

class User(flask_login.UserMixin):
    pass

app = flask.Flask(__name__)

filterList = os.environ.get('TAG_WATCH')
defaultTag = os.environ.get('TAG_DEFAULT')
users = { os.environ.get('USERNAME'): {'password': os.environ.get('PASSWORD')} }
app.secret_key = os.environ.get('SESSION_SECRET')

REMEMBER_COOKIE_DURATION = datetime.timedelta(days=31)  # Example: 31 days
app.config['REMEMBER_COOKIE_DURATION'] = REMEMBER_COOKIE_DURATION

loginManager = flask_login.LoginManager()
loginManager.init_app(app)

@loginManager.user_loader
def user_loader(user):
    if user not in users:
        return
    user = User()
    user.id = user
    return user

@loginManager.request_loader
def request_loader(request):
    username = request.form.get('username')
    if username not in users:
        return
    user = User()
    user.id = username
    return user

@loginManager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized', 401

@app.route('/login', methods=['POST'])
def login():
    username = flask.request.form['username']
    if username in users and flask.request.form['password'] == users[username]['password']:
        user = User()
        user.id = username
        flask_login.login_user(user, False) #remember=remember)
        return flask.redirect(flask.url_for('dashboard'))
    return 'Bad login'

@app.route('/logout')
def logout():
    flask_login.logout_user()
    return flask.redirect(flask.url_for('root'))

@app.route('/')
def root():
    return flask.render_template('index.html') 

@app.route('/dashboard')
@flask_login.login_required
def dashboard():
    return flask.render_template('base.html', page_title='Dashboard') 

@app.route('/list')
@flask_login.login_required
def listview():
    return flask.render_template('base.html', page_title='List') 

@app.get("/api/refresh/full")
@flask_login.login_required
def api_root():
    #nfo.updateAllNfos(True)
    jellyfinApi.update(True)
    return flask.redirect(flask.url_for('dashboard'))

@app.get("/api/refresh/partial")
@flask_login.login_required
def api_partial():
    #nfo.updateAllNfos(False)
    jellyfinApi.update(False)
    return flask.redirect(flask.url_for('dashboard'))

@app.get('/api/count')
@flask_login.login_required
def api_count():
    count = 0
    for key in mitsData.scan(mitsCommon.moviePrefix):
        count += 1
    for key in mitsData.scan(mitsCommon.seriesPrefix):
        count += 1
    return flask.json.jsonify(count)

@app.get('/api/filters')
@flask_login.login_required
def api_filters():
    return filterList

@app.get('/api/movies')
@flask_login.login_required
def api_movies():
    return getMedia(mitsCommon.moviePrefix)

@app.get('/api/series')
@flask_login.login_required
def api_series():
    return getMedia(mitsCommon.seriesPrefix)

def getMedia(prefix):
    data = {}
    for key in mitsData.scan(prefix):
        rawValue = mitsData.get(key)
        rawValue = rawValue.replace('\n', '')
        data[key] = rawValue
    return data
