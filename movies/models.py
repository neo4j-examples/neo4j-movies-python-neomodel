from django.db import models
from django_neomodel import DjangoNode
from neomodel import ArrayProperty, StringProperty, IntegerProperty, RelationshipFrom, RelationshipTo, StructuredRel, UniqueIdProperty


class ActedIn(StructuredRel):
    roles = ArrayProperty(StringProperty())


class Movie(DjangoNode):
    uuid = UniqueIdProperty(primary_key=True)
    title = StringProperty()
    tagline = StringProperty()
    released = IntegerProperty()

    directors = RelationshipFrom('Person', 'DIRECTED')
    writters = RelationshipFrom('Person', 'WROTE')
    producers = RelationshipFrom('Person', 'PRODUCED')
    reviewers = RelationshipFrom('Person', 'REVIEWED')
    actors = RelationshipFrom('Person', 'ACTED_IN', model=ActedIn)

    class Meta:
        app_label = 'movies'


class Person(DjangoNode):
    uuid = UniqueIdProperty(primary_key=True)
    name = StringProperty()
    born = IntegerProperty()

    follows = RelationshipTo('Person', 'FOLLOWS')
    directed = RelationshipFrom('Movie', 'DIRECTED')
    wrote = RelationshipFrom('Movie', 'WROTE')
    produced = RelationshipFrom('Movie', 'PRODUCED')
    reviewed = RelationshipFrom('Movie', 'REVIEWED')
    acted_in = RelationshipFrom('Movie', 'ACTED_IN')

    class Meta:
        app_label = 'movies'

