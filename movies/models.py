from django_neomodel import DjangoNode
from neomodel import ArrayProperty, StringProperty, IntegerProperty, RelationshipFrom, RelationshipTo, StructuredRel


class ActedIn(StructuredRel):
    roles = ArrayProperty(StringProperty())


class Movie(DjangoNode):
    id = IntegerProperty()
    title = StringProperty()
    tagline = StringProperty()
    released = IntegerProperty()

    directors = RelationshipFrom('Person', 'DIRECTED')
    writters = RelationshipFrom('Person', 'WROTE')
    producers = RelationshipFrom('Person', 'PRODUCED')
    reviewers = RelationshipFrom('Person', 'REVIEWED')
    actors = RelationshipFrom('Person', 'ACTED_IN', model=ActedIn)


class Person(DjangoNode):
    id = IntegerProperty()
    name = StringProperty()
    born = IntegerProperty()

    follows = RelationshipTo('Person', 'FOLLOWS')
    directed = RelationshipFrom('Movie', 'DIRECTED')
    wrote = RelationshipFrom('Movie', 'WROTE')
    produced = RelationshipFrom('Movie', 'PRODUCED')
    reviewed = RelationshipFrom('Movie', 'REVIEWED')
    acted_in = RelationshipFrom('Movie', 'ACTED_IN')

