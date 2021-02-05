from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import SignUpForm
from .models import User, UserFollows


@login_required
def show_user_graph(request, msg=None):

    followed = UserFollows.objects.filter(followed_user=request.user).select_related(
        "user"
    )
    following = UserFollows.objects.filter(user=request.user).select_related(
        "followed_user"
    )

    msg = request.session.get("_msg")
    request.session["_msg"] = ""

    return render(
        request,
        "user_graph/main.html",
        {"msg": msg, "following": following, "followed": followed},
    )


@login_required
def add_link(request):

    if request.method == "POST":

        user_name = request.POST["findname"]

        try:
            user_instance = User.objects.get(username=user_name)

            if user_instance == request.user:
                msg = "Vous ne pouvez pas vous suivre vous même"
            else:

                try:
                    UserFollows.objects.get(
                        followed_user=user_instance, user__username=request.user
                    )
                    msg = "Vous suivez déjà cet utilisateur"

                except UserFollows.DoesNotExist:

                    # Identique aux deux lignes suivantes
                    # UserFollows.objects.create(user=request.user, followed_user=user_instance)
                    new_link = UserFollows(
                        user=request.user, followed_user=user_instance
                    )
                    new_link.save()

                    print(user_instance, user_instance.email)
                    msg = "L'utilisateur a été ajouté à votre liste de contacts"

        except User.DoesNotExist:
            msg = "L'utilisateur n'a pas été trouvé"

    request.session["_msg"] = msg

    return redirect("show_user_graph")


@login_required
def remove_link(request, link_id):

    UserFollows.objects.filter(id=link_id).delete()
    return redirect("show_user_graph")


def signup(request):

    if request.method == "POST":
        form = SignUpForm(request.POST)

        try:
            user = User.objects.get(username=request.POST['username'])
            form.error = "Ce nom d'utilisateur est déjà pris"
        except User.DoesNotExist:

            try:
                user = User.objects.get(email=request.POST['email'])
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
