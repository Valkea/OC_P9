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


def add_link(request):

    if request.method == "POST":
        print("ADD LINK - POST show_user_graph", request.POST, request.POST["findname"])

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


def remove_link(request, link_id):
    print("REMOVE LINK:", link_id)
    UserFollows.objects.filter(id=link_id).delete()
    return redirect("show_user_graph")


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect("reviews:main_page")
    else:
        form = SignUpForm()
    return render(request, "registration/signup.html", {"form": form})
