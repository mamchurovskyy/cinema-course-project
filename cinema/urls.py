from django.urls import path

from cinema import views

app_name = "cinema"
urlpatterns = [
    path(route="", view=views.film_list_view, name="film_list"),
    path(
        route="<slug:genre_slug>/",
        view=views.film_list_view,
        name="film_list_by_genre",
    ),
    path(
        route="films/<slug:slug>/",
        view=views.film_detail_view,
        name="film_detail",
    ),
    path(
        route="people/<person_role>/",
        view=views.people_list_view,
        name="people_list",
    ),
    path(
        route="person/<int:person_id>",
        view=views.person_detail_view,
        name="person_detail",
    ),
]
