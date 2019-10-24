import json

from bottle import Bottle, request, abort

from models.movie import Movie, Base

recommendation_app = Bottle()


@recommendation_app.post('/recommendation')
def recommendation():
    current_interest = request.forms.get("currentInterest")
    all_interests = json.loads(request.forms.get("allInterest", {}))
    results = Movie.related_base(current_interest)

    scoring = {}
    for row in results:
        movie = Movie.inflate(row[0])
        bases = [Base.inflate(b).name for b in row[1]]

        scoring[movie.title] = {'score': 0, 'relations': [], 'data': movie.serialize}

        for key, value in all_interests.items():
            if key in bases:
                scoring[movie.title]['score'] += value
                scoring[movie.title]['relations'].append(key)

    return scoring


@recommendation_app.post('/recommendation/matrix')
def recommendation_matrix():
    selection = request.forms.get("selection")

    if not selection:
        return abort(400, "Selection not privided")

    keys = json.loads(selection).keys()
    selection_ids = [int(uid) for uid in keys]

    interests = {}
    for row in Movie.matrix(selection_ids)[0]:
        name = Base.inflate(row[0]).name
        existing_count = interests.get(name, 0)

        interests[name] = row[1] + existing_count

    return interests
