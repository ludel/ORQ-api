import hashlib

from bottle import Bottle, request

session_app = Bottle()


@session_app.post('/session/sign_up/')
def sign_up(db):
    password = request.json.get('password')
    password_hash = hashlib.sha256(password.encode()).hexdigest()

    user = {'email': request.json.get('email'), 'password': password_hash, 'watchlist': ''}

    if db.execute('SELECT * FROM user WHERE email == :email', user).fetchone():
        return 'User already exists'

    db.execute('INSERT INTO "user" ("email", "password", "watchlist") VALUES (:email, :password, :watchlist)',
               user)

    return 'User created'


@session_app.post('/session/sign_in/')
def sign_in(db):
    password = request.json.get('password', '')
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    user = {'email': request.json.get('email'), 'password': password_hash}

    query = 'SELECT * FROM user WHERE email == :email AND password == :password'
    res = db.execute(query, user).fetchone()

    if res:
        return {'id': res[0], 'email': res[1], 'watchlist': res[3]}
    else:
        return 'Bad username or password'


@session_app.route('/session/sign_up/', method=['OPTIONS'])
@session_app.route('/session/sign_in/', method=['OPTIONS'])
def option():
    return
