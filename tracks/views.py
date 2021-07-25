from django.http import JsonResponse
from django.shortcuts import render
from neomodel import Traversal, match
from .models import Tag, Track


def tracks_index(request):
    tracks = Track.nodes.all()
    return render(request, 'index.html', {
        'tracks': tracks
    })

# Makes the cute graph UI
def graph(request):
    nodes = []
    rels = []
    tags = Tag.nodes.has(top_track=True)

    i = 0
    for tag in tags:
        nodes.append({'id': tag.uuid, 'title': tag.name, 'label': 'tag'})
        target = i
        i += 1

        for trackgroup in tag.has_tag:
            group = {'id': trackgroup.uuid, 'title': trackgroup.title, 'label': 'group'}

            try:
                source = nodes.index(group)
            except ValueError:
                nodes.append(group)
                source = i
                i += 1
            rels.append({"source": source, "target": target})

    return JsonResponse({"nodes": nodes, "links": rels})


def search(request):
    try:
        q = request.GET["q"]
    except KeyError:
        return JsonResponse([])

    #here temporarily, we don't want to do this every time
    for tags_to_update in Tag.nodes.filter(name__icontains=q):
        tags_to_update.set_top_track()

    tags = Tag.nodes.filter(name__icontains=q).has(top_track=True)
    return JsonResponse([{
        'id': tag.uuid, 
        'title': tag.name, 
        'tagline': tag.top_track.single().title, 
        'released': tag.top_track.single().uuid, 
        'label': 'movie'
    } for tag in tags], safe=False)
