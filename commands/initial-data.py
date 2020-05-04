import os

import pandas as pd
import tmdbsimple
from dotenv import load_dotenv
import time
from movie_request import MovieRequest

load_dotenv('.env')

LANGUAGE = os.environ['LANGUAGE']

tmdbsimple.API_KEY = os.environ['API_TOKEN']
header = ['id', 'title', 'actors', 'compositor', 'date', 'director', 'genres', 'keywords', 'language', 'overview',
          'poster', 'producer', 'vote']


def get_detail(movie):
    actors = [movie.get_cast('cast', i) for i in range(1, 10)]
    return {
        'id': movie['id'],
        'title': movie['title'].replace(',', ''),
        'keywords': '|'.join(str(k['name']) for k in movie['keywords']['keywords']),
        'genres': '|'.join(str(g['name']) for g in movie['genres']),
        'director': movie.get_crew('crew', 'Director'),
        'producer': movie.get_crew('crew', 'Producer'),
        'compositor': movie.get_crew('crew', 'Original Music Composer'),
        'actors': '|'.join(actors),
        'vote': movie['vote_average'],
        'overview': movie['overview'],
        'poster': movie['poster_path'],
        'date': movie['release_date'],
        'language': movie['original_language'],
    }


def main(file_path, limit, sleep):
    df = pd.DataFrame(columns=header)

    for page in range(1, limit):
        print(f'=> Page {page}')
        movies_overview = tmdbsimple.Movies().top_rated(page=page)

        for movie in movies_overview['results']:
            time.sleep(sleep)
            print(f"    -> {movie['title']}")
            detail = tmdbsimple.Movies(movie['id']).info(
                language=LANGUAGE,
                append_to_response='credits,keywords,videos,reviews,images'
            )

            item = MovieRequest(**detail)
            df = df.append(get_detail(item), ignore_index=True)

        df.to_csv(file_path, index=False)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-o",
        "--output",
        type=str
    )
    parser.add_argument(
        "-s",
        "--sleep",
        type=float,
        default=1.0
    )
    parser.add_argument(
        "-n",
        "--limit",
        type=int,
    )

    args = parser.parse_args()
    main(args.output, args.limit, args.sleep)
