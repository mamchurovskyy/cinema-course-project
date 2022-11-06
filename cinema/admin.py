from django.contrib import admin

from cinema.models import Film, Genre, Person, Vote


@admin.register(Film)
class FilmAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "premiere",
        "country",
        "rating",
        "profit",
    )
    exclude = ("slug",)
    list_filter = (
        "premiere",
        "country",
        "rating",
        "profit",
        "genre",
    )
    search_fields = (
        "title",
        "description",
    )
    ordering = (
        "title",
        "premiere",
    )
    raw_id_fields = (
        "genre",
        "directors",
        "actors",
    )


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_filter = ("name",)
    search_fields = ("name",)


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "birthday",
        "gender",
    )
    list_filter = (
        "birthday",
        "gender",
    )
    search_fields = ("name",)


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_filter = (
        "rating",
        "film",
    )
