from django.http import JsonResponse
from django.shortcuts import render
from neomodel import Traversal, match
from .models import Movie, Person, Tag, Track


def movies_index(request):
    movies = Movie.nodes.all()
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

    #here temporarily
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


def serialize_cast(person, job, rel=None):
    return {
        'id': person.id,
        'name': person.name,
        'job': job,
        'role': rel.roles if rel else None
    }


def movie_by_title(request, title):
    movie = Movie.nodes.get(title=title)
    cast = []

    for person in movie.directors:
        cast.append(serialize_cast(person, 'directed'))

    for person in movie.writters:
        cast.append(serialize_cast(person, 'wrote'))

    for person in movie.producers:
        cast.append(serialize_cast(person, 'produced'))

    for person in movie.reviewers:
        cast.append(serialize_cast(person, 'reviewed'))

    for person in movie.actors:
        rel = movie.actors.relationship(person)
        cast.append(serialize_cast(person, 'acted', rel))

    return JsonResponse({
        'id': movie.id, 
        'title': movie.title, 
        'tagline': movie.tagline, 
        'released': movie.released, 
        'label': 'movie',
        'cast': cast
    })
