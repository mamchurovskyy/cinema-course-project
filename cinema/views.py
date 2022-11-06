from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import (
    Http404,
    HttpResponse,
    HttpResponseRedirect,
    JsonResponse,
)
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from cinema import services
from cinema.models import Film, Genre, Person


def film_list_view(request, genre_slug=None):
    """List all the movies or filter movies by a given genre."""

    genre = None
    genres = Genre.objects.all()
    films = Film.objects.all()

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
            if request.user.is_active:
                value = int(request.POST["vote"])

                if value > 10 or value < 1:
                    return JsonResponse(
                        {"message": "Unvalid vote value"}, status=400
                    )

                try:
                    film = services.get_film_by_slug(slug)
                except (ObjectDoesNotExist, MultipleObjectsReturned):
                    return JsonResponse(
                        {"message": "Something went wrong with Film"},
                        status=400,
                    )

                new_rating = (
                    "%.1f"
                    % services.vote_film_rating(
                        value, film, request.user
                    ).rating
                )

                return JsonResponse(
                    {
                        "message": "You voted {}".format(value),
                        "new_rating": new_rating,
                    },
                    status=200,
                )
            else:
                return JsonResponse(
                    {"message": "User is not active"}, status=400
                )
        else:
            return JsonResponse(
                {"message": "User is not authenticated"}, status=400
            )
    else:
        try:
            film = services.get_film_by_slug(slug)
        except ObjectDoesNotExist:
            raise Http404("Film not found")
        except MultipleObjectsReturned:
            raise Http404("Found several records with same id")

        if request.user.is_authenticated and request.user.is_active:
            try:
                vote = services.get_user_vote_rating(slug, request.user.id)
            except ObjectDoesNotExist or MultipleObjectsReturned:
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
        person = services.get_person_by_id(person_id=person_id)
    except ObjectDoesNotExist:
        raise Http404("Person not found.")
    except MultipleObjectsReturned:
        raise Http404("Multiple people with the same ID found.")

    actor_films = services.order_query_by_field(
        person.starred_films, "-rating"
    )
    director_films = services.order_query_by_field(
        person.directed_films, "-rating"
    )

    return render(
        request=request,
        template_name="cinema/person_detail.html",
        context={
            "person": person,
            "actor_films": actor_films,
            "director_films": director_films,
        },
    )
