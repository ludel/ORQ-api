import os

import requests
from bottle import Bottle

from api import DEBUG
from api.movie import movie_app
from api.people import people_app

main_app = Bottle()


def check_data():
    if not os.path.exists('data/movie.csv'):
        url = os.environ['DATA_URL']

        with open('data/movie.csv', 'wb') as f:
            f.write(requests.get(url).content)


if __name__ == '__main__':
    check_data()
    main_app.merge(people_app)
    main_app.merge(movie_app)
    main_app.run(host='localhost', port=8080, debug=DEBUG)
