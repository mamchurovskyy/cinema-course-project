from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import (
    PasswordResetConfirmView,
    PasswordResetView,
)
from django.urls import include, path, reverse_lazy

from . import views

app_name = "account"
urlpatterns = [
    path(route="signup/", view=views.user_signup_view, name="signup"),
    path(route="profile/", view=views.user_profile_view, name="profile"),
    path(
        route="password_reset/",
        view=PasswordResetView.as_view(
            success_url=reverse_lazy("account:password_reset_done"),
        ),
        name="password_reset",
    ),
    path(
        route="reset/<uidb64>/<token>/",
        view=PasswordResetConfirmView.as_view(
            success_url=reverse_lazy("account:password_reset_complete")
        ),
        name="password_reset_confirm",
    ),
    path("", include("django.contrib.auth.urls")),
]
