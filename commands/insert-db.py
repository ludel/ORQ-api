import os

import pandas as pd
from neomodel import db, DoesNotExist, config, install_all_labels
from tqdm import tqdm

from models.movie import Movie, Actor, Compositor, Director, Keyword, Producer, Genre

config.DATABASE_URL = os.environ['BOLT']

df = pd.read_csv('../data/movie.csv')
df.drop_duplicates(subset='id', inplace=True)
df.fillna('', inplace=True)

install_all_labels()


def get_or_create(model, **field):
    try:
        payload = model.nodes.get(**field)
    except DoesNotExist:
        payload = model(**field).save()

    return payload


@db.transaction
def main():
    for index, row in tqdm(df.iterrows(), total=df.shape[0]):
        try:
            Movie.nodes.get(uid=row['id'])
        except DoesNotExist:
            movie = Movie(
                uid=row['id'],
                title=row['title'],
                poster=row['poster'],
                overview=row['overview'],
                vote=row['vote'],
                date=row['date'],
                language=row['language'],
            ).save()
        else:
            continue

        director = get_or_create(Director, name=row['director'])
        compositor = get_or_create(Compositor, name=row['compositor'])
        producer = get_or_create(Producer, name=row['producer'])
        movie.producer.connect(producer)
        movie.director.connect(director)
        movie.compositor.connect(compositor)

        for name in row['genres'].split('|'):
            genre = get_or_create(Genre, name=name)
            movie.genres.connect(genre)

        for name in row['keywords'].split('|'):
            keyword = get_or_create(Keyword, name=name)
            movie.keywords.connect(keyword)

        for name in row['actors'].split('|'):
            actor = get_or_create(Actor, name=name)
            movie.actors.connect(actor)


if __name__ == '__main__':
    main()
    print('Done !')
