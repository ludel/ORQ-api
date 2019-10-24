import os

import pandas as pd
import tmdbsimple

from commands.movie_request import MovieRequest

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


def main(file_path):
    df = pd.DataFrame(columns=header)

    for page in range(1, 300):
        print(f'=> Page {page}')

        movies_overview = tmdbsimple.Movies().top_rated(page=page)

        for movie in movies_overview['results']:
            print(f"    -> {movie['title']}")
            detail = tmdbsimple.Movies(movie['id']).info(
                language=LANGUAGE,
                append_to_response='credits,keywords,videos,reviews,images'
            )

            item = MovieRequest(**detail)
            df = df.append(get_detail(item), ignore_index=True)

        df.to_csv(file_path, index=False)


if __name__ == '__main__':
    main('data/movie.csv')
