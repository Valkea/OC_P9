from itertools import chain

from django.db.models import CharField, Value, BooleanField  # , F
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from apps.reviews.forms import TicketForm, ReviewForm
from apps.reviews.models import Ticket, Review
from apps.user_graph.models import UserFollows


@login_required
def main_page(request):
    """
    Display :model:`reviews.Ticket` & :model:`reviews.Review` instances
    involving the current User or one of its :model:`user_graph.UserFollows` linked :model:`user.User`.

    Also add add a 'Review' button in order to answer open Tickets.

    **Context**

    ``posts``
        The combined selected instances of the:model:`reviews.Ticket` & :model:`reviews.Review` models
    ``source``
        A variable used to let the template know if they should act as 'main_page' or 'user_posts' content
    ``_source``
        A session variable used to let other views know that they should send back here once done

    **Template:**

    :template:'reviews/main.html'

    """

    followed = UserFollows.objects.filter(user=request.user).select_related(
        "followed_user"
    )

    followed = [x.followed_user for x in followed]
    followed.append(request.user)

    tickets_without_review = Ticket.objects.filter(
        review__isnull=True, user__in=followed
    )

    tickets_with_review = Ticket.objects.filter(review__isnull=False, user__in=followed)

    reviews = Review.objects.filter(Q(user__in=followed) | Q(ticket__user__in=followed))

    tickets_without_review = tickets_without_review.annotate(
        content_type=Value("TICKET", CharField()),
        has_review=Value(False, BooleanField()),
    ).select_related("user")

    tickets_with_review = tickets_with_review.annotate(
        content_type=Value("TICKET", CharField()),
        has_review=Value(True, BooleanField()),
    ).select_related("user")

    reviews = reviews.annotate(
        content_type=Value("REVIEW", CharField()),
        has_review=Value(True, BooleanField()),
    ).select_related("user")

    posts = sorted(
        chain(reviews, tickets_with_review, tickets_without_review),
        key=lambda post: post.time_created,
        reverse=True,
    )

    request.session["_source"] = "flux"

    return render(
        request,
        "reviews/main.html",
        {"posts": posts, "source": request.session.get("_source")},
    )


@login_required
def user_posts(request):
    """
    Display :model:`reviews.Ticket` & :model:`reviews.Review` instances involving the current User
    or other Users' Ticket instances whenever reviewed by the current User.

    Also add 'Edit' or 'Delete' buttons on its own Ticket or Review content.

    **Context**

    ``posts``
        The combined selected instances of the:model:`reviews.Ticket` & :model:`reviews.Review` models
    ``source``
        A variable used to let the template know if they should act as 'main_page' or 'user_posts' content
    ``_source``
        A session variable used to let other views know that they should send back here once done

    **Template:**

    :template:'reviews/main.html'

    """

    tickets_without_review = Ticket.objects.filter(
        review__isnull=True, user=request.user
    )

    tickets_with_review = Ticket.objects.filter(review__isnull=False, user=request.user)

    tickets_without_review = tickets_without_review.annotate(
        content_type=Value("TICKET", CharField()),
        has_review=Value(False, BooleanField()),
    ).select_related("user")

    tickets_with_review = tickets_with_review.annotate(
        content_type=Value("TICKET", CharField()),
        has_review=Value(True, BooleanField()),
    ).select_related("user")

    reviews = Review.objects.annotate(
        content_type=Value("REVIEW", CharField()),
        has_review=Value(True, BooleanField()),
    ).filter(user=request.user)

    posts = sorted(
        chain(reviews, tickets_with_review, tickets_without_review),
        key=lambda post: post.time_created,
        reverse=True,
    )

    request.session["_source"] = "posts"

    return render(
        request,
        "reviews/main.html",
        {"posts": posts, "source": request.session.get("_source")},
    )


@login_required
def add_ticket(request, ticket_id=None):
    """
    Display and handle the :model:`reviews.forms.TicketForm` used to add and edit :model:`reviews.Ticket` instances.

    **Context**

    ``form``
        An instance of the :model:`reviews.forms.TicketForm`

    **Template:**

    :template:'reviews/ticket.html'

    **Redirect:**

    Use the '_source' session parameter set by either 'main_page' or 'user_posts' views
    in order to redirect to the approrpiate view when form is validated.

    """

    ticket_instance = get_object_or_404(Ticket, pk=ticket_id) if ticket_id else None

    if request.method == "GET":
        print("GET:", ticket_instance, ticket_id)
        form = TicketForm(instance=ticket_instance)
        return render(request, "reviews/ticket.html", locals())

    elif request.method == "POST":
        print("POST:", ticket_instance, ticket_id)
        form = TicketForm(request.POST, request.FILES, instance=ticket_instance)

        if form.is_valid():
            new_ticket_instance = form.save(commit=False)
            new_ticket_instance.user = request.user
            new_ticket_instance.save()

            return redirect_flux(request.session.get("_source"))

        return render(request, "reviews/ticket.html", locals())


@login_required
def delete_ticket(request, ticket_id):
    """
    Delete the :model:`reviews.Ticket` instance associated to the provided ticked_id parameter.

    **Redirect:**

    Use the '_source' session parameter set by either 'main_page' or 'user_posts' views
    in order to redirect to the approrpiate view.

    """

    ticket_instance = get_object_or_404(Ticket, pk=ticket_id)
    ticket_instance.delete()
    return redirect_flux(request.session.get("_source"))


@login_required
def new_review(request, review_id=None, ticket_id=None):
    """
    Display and handle the :model:`reviews.forms.TicketForm` used
    to add and edit :model:`reviews.Ticket` instances and also
    display and handle the :model:`reviews.forms.ReviewForm` used
    to add and edit :model:`reviews.Review` instances.

    **Context**

    ``form``
        An instance of the :model:`reviews.forms.ReviewForm`

    ``formticket``
        An instance of the :model:`reviews.forms.TicketForm`

    ``review_instance``
        An instance of the :model:`reviews.Review`  # Not currently used from the Template

    ``ticket_instance``
        An instance of the :model:`reviews.Ticket`  # Not currently used from the Template

    **Template:**

    :template:'reviews/review.html'

    **Redirect:**

    Use the '_source' session parameter set by either 'main_page' or 'user_posts' views
    in order to redirect to the approrpiate view whenthe forms are validated.

    """

    print("new_review:", request.method, review_id, ticket_id)

    review_instance = get_object_or_404(Review, pk=review_id) if review_id else None
    ticket_instance = get_object_or_404(Ticket, pk=ticket_id) if ticket_id else None

    if request.method == "GET":

        form = ReviewForm(instance=review_instance)
        formticket = TicketForm(instance=None)

        return render(request, "reviews/review.html", locals())

    elif request.method == "POST":

        form = ReviewForm(request.POST, request.FILES, instance=review_instance)
        formticket = TicketForm(request.POST, request.FILES, instance=ticket_instance)

        if formticket.is_valid():
            new_ticket_instance = formticket.save(commit=False)
            new_ticket_instance.user = request.user

            if form.is_valid():
                new_review_instance = form.save(commit=False)
                new_review_instance.ticket = new_ticket_instance
                new_review_instance.user = request.user
                new_ticket_instance.save()
                new_review_instance.save()

                return redirect_flux(request.session.get("_source"))

        return render(request, "reviews/review.html", locals())


@login_required
def add_review(request, review_id=None, ticket_id=None):
    """
    Display and handle the :model:`reviews.forms.ReviewForm` used
    to add and edit :model:`reviews.Review` instances.

    **Context**

    ``form``
        An instance of the :model:`reviews.forms.ReviewForm`

    ``review_instance``
        An instance of the :model:`reviews.Review`  # Not currently used from the Template

    **Template:**

    :template:'reviews/review.html'

    **Redirect:**

    Use the '_source' session parameter set by either 'main_page' or 'user_posts' views
    in order to redirect to the approrpiate view whenthe forms are validated.

    """

    print("add_review:", request.method, review_id, ticket_id)

    review_instance = get_object_or_404(Review, pk=review_id) if review_id else None

    if review_id is not None:
        ticket_instance = review_instance.ticket
    else:
        ticket_instance = get_object_or_404(Ticket, pk=ticket_id) if ticket_id else None

    if request.method == "GET":

        form = ReviewForm(instance=review_instance)

        return render(request, "reviews/review.html", locals())

    elif request.method == "POST":

        form = ReviewForm(request.POST, request.FILES, instance=review_instance)

        if form.is_valid():
            new_review_instance = form.save(commit=False)
            new_review_instance.ticket = ticket_instance
            new_review_instance.user = request.user
            new_review_instance.save()

            return redirect_flux(request.session.get("_source"))

        return render(request, "reviews/review.html", locals())


@login_required
def delete_review(request, review_id):
    """
    Delete the :model:`reviews.Review` instance associated to the provided review_id parameter.

    **Redirect:**

    Use the '_source' session parameter set by either 'main_page' or 'user_posts' views
    in order to redirect to the approrpiate view.

    """

    review_instance = get_object_or_404(Review, pk=review_id)
    review_instance.delete()
    return redirect_flux(request.session.get("_source"))


def redirect_flux(source):
    """Redirect to 'main_page' or 'user_posts' views according to the provided parameter.

    Parameters
    ----------
    source: str
        'posts' ot redirect to 'user_posts' and something else to redirect to 'main_page'

    """

    print("redirect_flux:", source)
    if source == "posts":
        return redirect("reviews:user_posts")
    else:
        return redirect("reviews:main_page")
