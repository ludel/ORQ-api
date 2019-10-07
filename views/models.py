import neomodel as neo
from neomodel.cardinality import ZeroOrOne, ZeroOrMore


class Movie(neo.StructuredNode):
    uid = neo.IntegerProperty()
    title = neo.StringProperty()

    producer = neo.RelationshipTo('Producer', 'PRODUCE_BY', cardinality=ZeroOrOne)  # todo OneToOne relationship
    compositor = neo.RelationshipTo('Compositor', 'COMPOSED_BY', cardinality=ZeroOrOne)  # todo OneToOne relationship
    director = neo.RelationshipTo('Director', 'LEAD_BY', cardinality=ZeroOrOne)  # todo OneToOne relationship
    actors = neo.RelationshipTo('Actor', 'PLAYED_BY', cardinality=ZeroOrMore)
    genres = neo.RelationshipTo('Genre', 'OWN', cardinality=ZeroOrMore)
    keywords = neo.RelationshipTo('Keyword', 'IS', cardinality=ZeroOrMore)

    @classmethod
    def recommendation(cls, selection_ids, movies_in_cluster):
        return neo.db.cypher_query(
            f"""MATCH (p)-[:LEAD_BY|:COMPOSED_BY|:PRODUCE_BY|:PLAYED_BY|:IS]-(Movie) WHERE Movie.uid in {selection_ids} 
            WITH p MATCH (m:Movie) WHERE m.uid in {movies_in_cluster}  
            AND (p)-[:LEAD_BY|:COMPOSED_BY|:PRODUCE_BY|:PLAYED_BY|:IS]-(m) 
            WITH m, count(p) AS NumberPerson RETURN m ORDER BY NumberPerson DESC LIMIT 10 """
        )


class Base(neo.StructuredNode):
    name = neo.StringProperty(unique_index=True, )


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
