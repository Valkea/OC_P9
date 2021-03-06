from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import UserFollows
from apps.user.models import User


@login_required
def show_user_graph(request, msg=None):
    """
    Display the followed and following :model:`user.User` instances.

    **Context**

    ``msg``
        A parameter providing an optional message to display
    ``following``
        The :model:`user.User` instances matching the :model:`UserFollows`
        where the 'user' is the current User
    ``followed``
        The :model:`user.User` instances matching the :model:`UserFollows`
        where the 'followed_user' is the current User

    **Template:**

    :template:'user_graph/main.html'

    """

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
    """
    Create a new :model:`user_graph.UserFollows` instance to link two :model:`user.User`.
    The first one is the current User and the second is the one matching the 'findname' POST parameter.

    **Context**

    ``_msg``
        A session veriable used to pass error messages to the next view

    **Redirect:**

    To the main 'show_user_graph' view

    """

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
    """
    Delete the :model:`user_graph.UserFollows` instance associated to the provided link_id parameter.

    **Redirect:**

    To the main 'show_user_graph' view

    """

    UserFollows.objects.filter(id=link_id).delete()
    return redirect("show_user_graph")
