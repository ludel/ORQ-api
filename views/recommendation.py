from bottle import Bottle, request, abort

from models.movie import Movie, Base

recommendation_app = Bottle()


@recommendation_app.post('/recommendation')
def recommendation():
    cursor_about = request.json.get("cursorAbout")
    user_matrix = request.json.get("userMatrix", {})
    selection = request.json.get('selection', [])

    clean_selection = [int(uid) for uid in selection]

    results = Movie.related_base(cursor_about, clean_selection)

    scoring = {}
    for index, row in enumerate(results):
        movie = Movie.inflate(row[0])
        bases = [Base.inflate(b).name for b in row[1]]

        content = {'title': movie.title, 'score': 0, 'relations': [], 'data': movie.serialize}

        for key, value in user_matrix.items():
            if key in bases:
                content['score'] += value
                content['relations'].append(key)

        scoring[index] = content

    return scoring


@recommendation_app.post('/recommendation/matrix')
def recommendation_matrix():
    selection = request.json.get('selection')

    if not selection:
        return abort(400, 'Selection not privided')

    keys = selection.keys()
    selection_ids = [int(uid) for uid in keys]

    interests = {}
    for row in Movie.matrix(selection_ids)[0]:
        name = Base.inflate(row[0]).name
        existing_count = interests.get(name, 0)

        interests[name] = row[1] + existing_count

    return interests


@recommendation_app.route('/recommendation/matrix', method=['OPTIONS'])
def recommendation_matrix_option():
    return


@recommendation_app.route('/recommendation', method=['OPTIONS'])
def recommendation_option():
    return
