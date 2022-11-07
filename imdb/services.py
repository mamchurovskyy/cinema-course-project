import requests
from django.conf import settings


def _make_request(url, **params):
    """Perform GET request to the RapidAPI."""

    headers = {
        "X-RapidAPI-Key": "c9be4bddafmsh059079e90a6d103p17a634jsna6a41297293e",
        "X-RapidAPI-Host": "imdb8.p.rapidapi.com",
    }

    response = requests.request("GET", url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()


def _get_movie_id_by_title(title: str) -> str | None:
    url = "https://imdb8.p.rapidapi.com/title/find"

    response = _make_request(url=url, q=title)

    if response is not None and "results" in response:
        result = response["results"][0]

        if result["title"].lower() == title.lower().strip():
            return result["id"][7:-1]


def _get_movie_rating_by_id(movie_id: str) -> float | None:
    url = "https://imdb8.p.rapidapi.com/title/get-ratings"

    response = _make_request(url=url, tconst=movie_id)

    if response is not None and "rating" in response:
        return float(response["rating"])


def get_movie_rating_by_title(title: str) -> float | None:
    movie_id = _get_movie_id_by_title(title=title)
    rating = _get_movie_rating_by_id(movie_id=movie_id)

    return rating
