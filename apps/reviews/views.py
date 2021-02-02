from itertools import chain

from django.db.models import CharField, Value, BooleanField  # , F
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from apps.reviews.forms import TicketForm, ReviewForm
from apps.reviews.models import Ticket, Review

# from apps.user_graph.models import User


@login_required
def main_reviews(request):

    # tickets = Ticket.objects.all()
    # reviews = Review.objects.all()
    # reviews = reviews.annotate(
    #             type=Value('TICKET', CharField())
    #             ).values(
    #                     'id',
    #                     'headline',
    #                     'body',
    #                     'time_created',
    #                     'rating',
    #                     'ticket',
    #                     'user'
    #             )

    # tickets = Ticket.objects.all()
    # tickets = tickets.annotate(
    #             value=F('review__ticket'),
    #             type=Value('TICKET', CharField())
    #             ).values(
    #                     'id',
    #                     'title',
    #                     'description',
    #                     'user',
    #                     'image',
    #                     'time_created',
    #                     'review__ticket',
    #                     'type')

    # tickets = tickets.annotate(content_type=Value("TICKET", CharField()))
    # reviews = reviews.annotate(content_type=Value("REVIEW", CharField()))

    # #  combine and sort the two types of posts
    # posts = sorted(
    #     chain(reviews, tickets), key=lambda post: post['time_created'], reverse=True
    # )

    tickets_without_review = Ticket.objects.filter(review__isnull=True).all()
    tickets_without_review = tickets_without_review.annotate(
        content_type=Value("TICKET", CharField()),
        has_review=Value(False, BooleanField()),
    )

    tickets_with_review = Ticket.objects.filter(review__isnull=False).all()
    tickets_with_review = tickets_with_review.annotate(
        content_type=Value("TICKET", CharField()),
        has_review=Value(True, BooleanField()),
    )

    reviews = Review.objects.annotate(
        content_type=Value("REVIEW", CharField()),
        has_review=Value(True, BooleanField()),
    )

    posts = sorted(
        chain(reviews, tickets_with_review, tickets_without_review),
        key=lambda post: post.time_created,
        reverse=True,
    )

    return render(request, "reviews/main.html", {"posts": posts})


@login_required
def add_ticket(request, ticket_id=None):

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
            return redirect("reviews:main_reviews")

        return render(request, "reviews/ticket.html", locals())


@login_required
def delete_ticket(request, ticket_id):

    ticket_instance = get_object_or_404(Ticket, pk=ticket_id)
    ticket_instance.delete()
    return redirect("reviews:main_reviews")


@login_required
def new_review(request, review_id=None, ticket_id=None):

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
                return redirect("reviews:main_reviews")

        return render(request, "reviews/review.html", locals())


@login_required
def add_review(request, review_id=None, ticket_id=None):

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
            return redirect("reviews:main_reviews")

        return render(request, "reviews/review.html", locals())


@login_required
def delete_review(request, review_id):

    review_instance = get_object_or_404(Review, pk=review_id)
    review_instance.delete()
    return redirect("reviews:main_reviews")
