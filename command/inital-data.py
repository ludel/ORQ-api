import pandas as pd
from neomodel import db, DoesNotExist, remove_all_labels
from tqdm import tqdm

from views.models import Movie, Actor, Compositor, Director, Keyword, Producer, Genre


def get_or_create(model, **field):
    try:
        payload = model.nodes.get(**field)
    except DoesNotExist:
        payload = model(**field).save()

    return payload


df = pd.read_csv('data/movie.csv')

remove_all_labels(db)

with db.transaction:
    for index, row in tqdm(df.iterrows(), total=df.shape[0]):
        try:
            Movie.nodes.get(uid=row['uid'])
        except DoesNotExist:
            movie = Movie(
                uid=row['id'],
                title=row['title'],
            ).save()
        else:
            continue

        director = get_or_create(Director, name=row['director'])
        compositor = get_or_create(Compositor, name=row['compositor'])
        producer = get_or_create(Producer, name=row['producer'])

        movie.producer.connect(producer)
        movie.director.connect(director)
        movie.compositor.connect(compositor)

        actor_1 = get_or_create(Actor, name=row['actor_1'])
        actor_2 = get_or_create(Actor, name=row['actor_2'])
        actor_3 = get_or_create(Actor, name=row['actor_3'])
        movie.actors.connect(actor_1)
        movie.actors.connect(actor_2)
        movie.actors.connect(actor_3)

        for name in row['genres'].split(' '):
            genre = get_or_create(Genre, name=name)
            movie.genres.connect(genre)

        for name in row['keywords'].split(' '):
            keyword = get_or_create(Keyword, name=name)
            movie.keywords.connect(keyword)

print('Done !')
