from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect

from .forms import SignUpForm
from .models import User


def signup(request):

    if request.method == "POST":
        form = SignUpForm(request.POST)

        try:
            user = User.objects.get(username=request.POST["username"])
            form.error = "Ce nom d'utilisateur est déjà pris"
        except User.DoesNotExist:

            try:
                user = User.objects.get(email=request.POST["email"])
                print(user, user.email)
                form.error = "Cette adresse email est déjà enregistrée"

            except User.DoesNotExist:

                if form.is_valid():
                    form.save()

                    # Login and reidrect to base page
                    username = form.cleaned_data.get("username")
                    raw_password = form.cleaned_data.get("password1")
                    user = authenticate(username=username, password=raw_password)
                    login(request, user)
                    return redirect("reviews:main_page")
                else:
                    raw_password1 = request.POST["password1"]
                    raw_password2 = request.POST["password2"]
                    if raw_password1 != raw_password2:
                        form.error = "Votre mot de passe n'est pas identique dans les deux champs"
                    else:
                        form.error = "Votre mot de passe ne respecte pas les critères obligatoires"

    else:
        form = SignUpForm()

    return render(request, "registration/signup.html", {"form": form})
