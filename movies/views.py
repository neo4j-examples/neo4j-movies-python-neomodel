from django.http import JsonResponse
from django.shortcuts import render
from neomodel import Traversal, match
from .models import Movie, Person


def movies_index(request):
    movies = Movie.nodes.all()
    return render(request, 'index.html', {
        'movies': movies
    })


def graph(request):
    nodes = []
    rels = []
    movies = Movie.nodes.has(actors=True)

    i = 0
    for movie in movies:
        nodes.append({'id': movie.id, 'title': movie.title, 'label': 'movie'})
        target = i
        i += 1

        for person in movie.actors:
            actor = {'id': person.id, 'title': person.name, 'label': 'actor'}

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

    movies = Movie.nodes.filter(title__icontains=q)
    return JsonResponse([{
        'id': movie.id, 
        'title': movie.title, 
        'tagline': movie.tagline, 
        'released': movie.released, 
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
