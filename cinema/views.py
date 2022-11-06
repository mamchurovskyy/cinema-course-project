from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Avg
from django.http import (
    Http404,
    HttpResponse,
    HttpResponseRedirect,
    JsonResponse,
)
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from cinema.models import Film, Genre, Person, Vote


def film_list_view(request, genre_slug=None):
    """List all the movies or filter movies by a given genre."""

    genre = None
    genres = Genre.objects.all()
    films = Film.objects.all().select_related("genre")

    order_by_value = request.GET.get("order_by", "rating")

    if genre_slug is not None:
        genre = get_object_or_404(Genre, slug=genre_slug)
        films = films.filter(genre=genre)

    order_by_fields = {
        "rating": "-rating",
        "title": "title",
        "premiere": "-premiere",
    }
    try:
        films = films.order_by(order_by_fields[order_by_value])
    except KeyError:
        return HttpResponseRedirect(reverse("cinema:film_list"))

    paginator = Paginator(object_list=films, per_page=6)
    page = request.GET.get("page")

    try:
        films = paginator.page(number=page)
    except PageNotAnInteger:
        films = paginator.page(number=1)
    except EmptyPage:
        if request.is_ajax():
            # If AJAX request and page out of range return an empty page
            return HttpResponse("")
        # If page out of range return the last page of results
        films = paginator.page(number=paginator.num_pages)

    if request.is_ajax():
        return render(
            request=request,
            template_name="cinema/film_list.html",
            context={"films": films},
        )

    return render(
        request=request,
        template_name="cinema/cinema.html",
        context={
            "genre": genre,
            "genres": genres,
            "films": films,
        },
    )


def film_detail_view(request, slug):
    if request.method == "POST":
        if request.user.is_authenticated:
            value = int(request.POST["vote"])

            if value > 10 or value < 1:
                return JsonResponse(
                    data={"message": "Unvalid vote value!"}, status=400
                )
            try:
                film = Film.objects.get(slug=slug)
            except (ObjectDoesNotExist, MultipleObjectsReturned):
                return JsonResponse(
                    data={
                        "message": "Impossible to get the film by given slug!"
                    },
                    status=400,
                )

            Vote.objects.update_or_create(
                user=request.user,
                film=film,
                defaults={"rating": value},
            )
            # update film overall rating based on users votes
            film.rating = film.votes.aggregate(Avg("rating"))["rating__avg"]
            film.save()

            return JsonResponse(
                data={"overall_rating": film.rating},
                status=200,
            )
        else:
            return JsonResponse(
                {"message": "You're not authenticated!"}, status=400
            )
    else:
        try:
            film = Film.objects.get(slug=slug)
        except ObjectDoesNotExist:
            raise Http404("Film is not found!")
        except MultipleObjectsReturned:
            raise Http404("several records with same IDs were found!")

        if request.user.is_authenticated:
            try:
                vote = Vote.objects.get(
                    film__slug=slug, user__id=request.user.id
                ).rating
            except (ObjectDoesNotExist, MultipleObjectsReturned):
                vote = 0
        else:
            vote = 0

        # imdb_rating = imdb.get_rating_by_title(film.title)

    return render(
        request,
        "cinema/film_detail.html",
        {
            "film": film,
            "vote": vote,
            # "imdb_rating": imdb_rating
        },
    )


def people_list_view(request, person_role):
    if person_role not in ("actors", "directors"):
        raise Http404()

    if person_role == "actors":
        person_list = Person.objects.is_actor().filter().order_by("name")
    elif person_role == "directors":
        person_list = Person.objects.is_director().filter().order_by("name")

    paginator = Paginator(object_list=person_list, per_page=6)
    page = request.GET.get("page")

    try:
        person_list = paginator.page(number=page)
    except PageNotAnInteger:
        person_list = paginator.page(number=1)
    except EmptyPage:
        if request.is_ajax():
            # If AJAX request and page out of range return an empty page
            return HttpResponse("")
        # If page out of range return the last page of results
        person_list = paginator.page(number=paginator.num_pages)

    if request.is_ajax():
        return render(
            request=request,
            template_name="cinema/person_list.html",
            context={"person_list": person_list},
        )
    return render(
        request=request,
        template_name="cinema/actor_director_list.html",
        context={"section": person_role, "person_list": person_list},
    )


def person_detail_view(request, person_id):
    try:
        person = Person.objects.get(id=person_id)
    except ObjectDoesNotExist:
        raise Http404("Person not found.")
    except MultipleObjectsReturned:
        raise Http404("Multiple people with the same ID found.")

    actor_films = person.starred_films.order_by("-rating")
    director_films = person.directed_films.order_by("-rating")

    return render(
        request=request,
        template_name="cinema/person_detail.html",
        context={
            "person": person,
            "actor_films": actor_films,
            "director_films": director_films,
        },
    )
