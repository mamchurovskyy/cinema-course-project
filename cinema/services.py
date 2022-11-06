from cinema.models import Film, Genre, Person, Vote


def get_all_genres(**filters):
    return Genre.objects.filter(**filters)


def get_all_films(**filters):
    return Film.objects.filter(**filters)


def get_all_actors(**filters):
    return Person.objects.is_actor().filter(**filters)


def get_all_directors(**filters):
    return Person.objects.is_director().filter(**filters)


def get_person_by_id(person_id: int):
    return Person.objects.get(id=person_id)


def get_film_by_slug(slug: str):
    return Film.objects.get(slug=slug)


def order_query_by_field(query, field_name: str):
    return query.order_by(field_name)


def vote_film_rating(value, film, user):
    """
    If Vote exists with Vote.film=film & Vote.user=user then update Vote.rating=value and return Vote
    Else create and return new Vote with Vote.film=film & Vote.user=user & Vote.rating=value
    """
    vote, _ = Vote.objects.update_or_create(
        user=user,
        film=film,
        defaults={"rating": value},
    )
    return vote


def get_user_vote_rating(film_slug: int, user_id: int) -> int:
    """
    Returns object Vote with Vote.film.id=film_id, Vote.user.id=user_id

    If there are no results that match the query, it will raise a DoesNotExist exception.
    If more than one item matches, it will raise MultipleObjectsReturned.
    """

    return Vote.objects.get(film__slug=film_slug, user__id=user_id).rating
