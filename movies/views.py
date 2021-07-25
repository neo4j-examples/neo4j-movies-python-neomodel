from django.http import JsonResponse
from django.shortcuts import render
from neomodel import Traversal, match
from .models import Tag, Track


def movies_index(request):
    movies = Track.nodes.all()
    return render(request, 'index.html', {
        'movies': movies
    })

# Makes the cute graph UI
def graph(request):
    nodes = []
    rels = []
    movies = Tag.nodes.has(top_track=True)

    i = 0
    for movie in movies:
        nodes.append({'id': movie.uuid, 'title': movie.name, 'label': 'movie'})
        target = i
        i += 1

        for person in movie.has_tag:
            actor = {'id': person.uuid, 'title': person.title, 'label': 'actor'}

            try:
                source = nodes.index(actor)
            except ValueError:
                nodes.append(actor)
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

    movies = Tag.nodes.filter(name__icontains=q).has(top_track=True)
    return JsonResponse([{
        'id': movie.uuid, 
        'title': movie.name, 
        'tagline': movie.top_track.single().title, 
        'released': movie.top_track.single().uuid, 
        'label': 'movie'
    } for movie in movies], safe=False)
