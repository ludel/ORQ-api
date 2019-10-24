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
            'title': self.title,
            'vote': self.vote,
            'overview': self.overview,
            'poster': self.poster,
            'date': self.date,
            'language': self.language
        }

    @classmethod
    def recommendation(cls, selection_ids, movies_in_cluster):
        return neo.db.cypher_query(
            f"""MATCH (p)-[:LEAD_BY|:COMPOSED_BY|:PRODUCE_BY|:PLAYED_BY|:IS]-(Movie) WHERE Movie.uid in {selection_ids} 
            WITH p MATCH (m:Movie) WHERE m.uid in {movies_in_cluster}  
            AND (p)-[:LEAD_BY|:COMPOSED_BY|:PRODUCE_BY|:PLAYED_BY|:IS]-(m) 
            WITH m, count(p) AS NumberPerson RETURN m ORDER BY NumberPerson DESC LIMIT 10 """
        )

    @classmethod
    def related_base(cls, name):
        return neo.db.cypher_query(
            f"""MATCH (Base {{name:"{name}"}})--(m:Movie)--(b:Base)
                RETURN m, collect(b) LIMIT 30"""
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
