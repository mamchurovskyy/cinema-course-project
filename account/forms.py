from django import forms
from django.contrib.auth import get_user_model

from account.models import Profile

User = get_user_model()


class UserLogInForm(forms.Form):
    email = forms.EmailField(
        max_length=254,
    )
    password = forms.CharField(widget=forms.PasswordInput)


class UserSignUpForm(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Repeat password", widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name")

    def clean_password2(self) -> str:
        """Compare the second password against the first one."""

        cd = self.cleaned_data
        if cd["password"] != cd["password2"]:
            raise forms.ValidationError("The entered passwords do not match.")
        return cd["password2"]

    def clean_email(self) -> str:
        """Prevents user from registering with an existing email."""

        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "The email you entered is already in use."
            )
        return email


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
        )

    def clean_email(self) -> str:
        """
        Prevents user from changing current email to already existing one.
        """

        email = self.cleaned_data["email"]
        qs = User.objects.exclude(id=self.instance.id).filter(email=email)
        if qs.exists():
            raise forms.ValidationError(
                "The email you entered is already in use."
            )
        return email


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            "birthday",
            "avatar",
        )
        widgets = {
            "birthday": forms.DateInput(
                format=("%Y-%m-%d"), attrs={"type": "date"}
            ),
        }
