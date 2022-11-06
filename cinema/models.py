from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django_countries.fields import CountryField


class Genre(models.Model):
    name = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(max_length=50, unique=True, null=True, blank=True)

    class Meta:
        ordering = ("name",)
        indexes = (models.Index(fields=("name",)),)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("cinema:film_list_by_genre", args=(self.slug,))

    def __str__(self) -> str:
        return self.name


class PersonQuerySet(models.QuerySet):
    def is_actor(self):
        return self.filter(starred_films__isnull=False).distinct()

    def is_director(self):
        return self.filter(directed_films__isnull=False).distinct()


class Person(models.Model):
    GENDER_CHOICES = [
        ("M", "Male"),
        ("F", "Female"),
    ]

    image = models.ImageField(
        upload_to="people/%Y/%m/%d/", null=True, blank=True, default=None
    )
    name = models.CharField(max_length=60)
    birthday = models.DateField(null=True, blank=True)
    gender = models.CharField(
        max_length=1, choices=GENDER_CHOICES, null=True, blank=True
    )

    objects = PersonQuerySet.as_manager()

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Person"
        verbose_name_plural = "People"


class Film(models.Model):
    slug = models.SlugField(max_length=255, unique=True)
    poster = models.ImageField(
        upload_to="films/%Y/%m/%d/", null=True, blank=True, default=None
    )
    title = models.CharField(max_length=100)
    premiere = models.DateField()
    country = CountryField(blank=True)
    duration = models.IntegerField(null=True, blank=True)
    rating = models.FloatField(editable=False, blank=True, default=0.0)
    profit = models.BigIntegerField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    genre = models.ForeignKey(
        Genre, related_name="films", on_delete=models.SET_NULL, null=True
    )
    directors = models.ManyToManyField(
        Person, related_name="directed_films", blank=True
    )
    actors = models.ManyToManyField(
        Person, related_name="starred_films", blank=True
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("cinema:film_detail", kwargs={"slug": self.slug})

    def __str__(self) -> str:
        return self.title


class Vote(models.Model):
    film = models.ForeignKey(Film, on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    rating = models.SmallIntegerField(editable=False)

    def __str__(self) -> str:
        return f"Film_{self.film.id}: {self.rating} from User_{self.user.id}"

    class Meta:
        unique_together = (
            "film",
            "user",
        )
