from django.db import models
from django_neomodel import DjangoNode
from neomodel import ArrayProperty, StringProperty, IntegerProperty, RelationshipFrom, RelationshipTo, StructuredRel, UniqueIdProperty

class TrackGroup(DjangoNode):
    uuid = UniqueIdProperty(primary_key=True)
    title = StringProperty()
    type = StringProperty()

    has_tag = RelationshipTo('Tag', 'HAS_TAG')
    has_track = RelationshipTo('Track', 'HAS_TRACK')
    owns = RelationshipFrom('RUser', 'OWNS')

    class Meta:
        app_label = 'tracks'

class Tag(DjangoNode):
    uuid = UniqueIdProperty(primary_key=True)
    name = StringProperty()

    has_tag = RelationshipFrom('TrackGroup', 'HAS_TAG')
    top_track = RelationshipTo('Track', 'TOP_TRACK')

    def set_top_track(self):
        self.top_track.disconnect_all()
        query = f'''
            MATCH (tag:Tag)
            WHERE tag.name='{self.name}'
            WITH tag
            MATCH (tag:Tag)<-[:HAS_TAG]-(tg:TrackGroup)-[:HAS_TRACK]->(track:Track)
            MATCH (tg)<-[:OWNS]-(u:RUser) 
            WITH tag as tag, track as track, count(DISTINCT u) as rank
            LIMIT 1
            MERGE (tag)-[:TOP_TRACK]->(track)
            '''
        self.cypher(query)

    class Meta:
        app_label = 'tracks'

class Track(DjangoNode):
    uuid = UniqueIdProperty(primary_key=True)
    title = StringProperty()

    has_track = RelationshipFrom('Track', 'HAS_TRACK')

    class Meta:
        app_label = 'tracks'

class RUser(DjangoNode):
    uuid = UniqueIdProperty(primary_key=True)
    title = StringProperty()

    owns = RelationshipTo('TrackGroup', 'OWNS')

    class Meta:
        app_label = 'tracks'

