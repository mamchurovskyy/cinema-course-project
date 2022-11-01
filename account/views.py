from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from account.forms import ProfileEditForm, UserEditForm, UserSignUpForm
from account.models import Profile

User = get_user_model()


def user_signup_view(request):
    if request.method == "POST":
        user_form = UserSignUpForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data["password"])
            new_user.save()

            Profile.objects.create(user=new_user)

            return render(
                request=request,
                template_name="registration/register_done.html",
                context={"new_user": new_user},
            )
    else:
        user_form = UserSignUpForm()

    return render(
        request=request,
        template_name="registration/register.html",
        context={"form": user_form},
    )


@login_required
def user_profile_view(request):
    """Allow users to edit their personal information."""

    if request.method == "POST":
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(
            instance=request.user.profile,
            data=request.POST,
            files=request.FILES,
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(
                request=request, message="Profile updated successfully!"
            )
        else:
            messages.error(
                request=request, message="Error while updating your profile..."
            )
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    return render(
        request=request,
        template_name="registration/profile.html",
        context={"user_form": user_form, "profile_form": profile_form},
    )
