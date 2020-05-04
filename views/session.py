import hashlib
import uuid

from bottle import Bottle, request, abort

from models.user import User

session_app = Bottle()


@session_app.post('/session/sign_up/')
def sign_up():
    try:
        password = request.json['password']
        email = request.json['email']
    except TypeError:
        return abort(400, 'Password or email missing')

    password_hash = hashlib.sha256(password.encode()).hexdigest()
    if User.show.get(User.email == email):
        return abort(400, 'User already exists')

    token = uuid.uuid4().hex
    User.change.insert(email=email, password=password_hash, token=token)
    return 'User created'


@session_app.post('/session/sign_in/')
def sign_in():
    try:
        password = request.json['password']
        email = request.json['email']
    except TypeError:
        return abort(400, 'Password or email missing')

    password_hash = hashlib.sha256(password.encode()).hexdigest()

    condition = (User.email == email) & (User.password == password_hash)
    user = User.show.get(condition)

    if user:
        return {'token': user.token, 'watchlist': user.watchlist}
    else:
        return 'Bad username or password'


@session_app.post("/session/watchlist/<update:re:add|remove>")
def update_watchlist(update):
    try:
        token = request.json['token']
        movie_id = str(request.json['movie_id'])
    except TypeError:
        return abort(400, 'Token or movie id missing')

    user = User.show.get(User.token == token)
    if not user:
        return abort(400, 'User not found')

    watchlist = user.watchlist.split(',') if user.watchlist else []
    if update == 'add':
        watchlist.append(movie_id)
    else:
        watchlist.remove(movie_id)

    User.change.update(User.pk == user.id, watchlist=','.join(watchlist))
    return 'Watchlist updated'


@session_app.route('/session/sign_up/', method=['OPTIONS'])
@session_app.route("/session/watchlist/<update:re:add|remove>", method=['PUT'])
@session_app.route('/session/sign_in/', method=['OPTIONS'])
def option():
    return
