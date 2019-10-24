import neomodel as neo
from neomodel.cardinality import ZeroOrOne, ZeroOrMore


class Movie(neo.StructuredNode):
    uid = neo.IntegerProperty()
    title = neo.StringProperty()
    vote = neo.StringProperty()
    overview = neo.StringProperty()
    poster = neo.StringProperty()
    date = neo.StringProperty()
    language = neo.StringProperty()

    producer = neo.RelationshipTo('Producer', 'PRODUCE_BY', cardinality=ZeroOrOne)
    compositor = neo.RelationshipTo('Compositor', 'COMPOSED_BY', cardinality=ZeroOrOne)
    director = neo.RelationshipTo('Director', 'LEAD_BY', cardinality=ZeroOrOne)
    actors = neo.RelationshipTo('Actor', 'PLAYED_BY', cardinality=ZeroOrMore)
    genres = neo.RelationshipTo('Genre', 'OWN', cardinality=ZeroOrMore)
    keywords = neo.RelationshipTo('Keyword', 'IS', cardinality=ZeroOrMore)

    @property
    def serialize(self):
        return {
            'id': self.uid,
            'title': self.title,
            'vote_average': self.vote,
            'overview': self.overview,
            'poster_path': self.poster,
            'release_date': self.date,
            'original_language': self.language
        }

    @classmethod
    def related_base(cls, name, selection):
        return neo.db.cypher_query(
            f"""MATCH (Base {{name:"{name}"}})--(m:Movie)--(b:Base)
                WHERE NOT m.uid IN {selection}
                RETURN m, collect(b) LIMIT 50"""
        )[0]

    @classmethod
    def matrix(cls, selection_ids):
        return neo.db.cypher_query(
            f"""MATCH (p)-[r]-(m:Movie)
                WHERE m.uid in {selection_ids}
                WITH p, Count(r) AS CountRelation
                RETURN p, CountRelation 
                ORDER BY CountRelation DESC LIMIT 30"""
        )


class Base(neo.StructuredNode):
    name = neo.StringProperty()


class Producer(Base):
    movie = neo.RelationshipFrom(Movie, 'PRODUCED', cardinality=ZeroOrOne)


class Actor(Base):
    movie = neo.RelationshipFrom(Movie, 'PLAY_IN', cardinality=ZeroOrMore)


class Compositor(Base):
    movie = neo.RelationshipFrom(Movie, 'COMPOSED', cardinality=ZeroOrOne)


class Director(Base):
    movie = neo.RelationshipFrom(Movie, 'LED', cardinality=ZeroOrOne)


class Genre(Base):
    movie = neo.RelationshipFrom(Movie, 'OWN', cardinality=ZeroOrMore)


class Keyword(Base):
    movie = neo.RelationshipFrom(Movie, 'IS', cardinality=ZeroOrMore)
