from django.shortcuts import render, redirect, get_object_or_404

from apps.reviews.forms import TicketForm, ReviewForm
from apps.reviews.models import Ticket, Review

# from apps.user_graph.models import User


def main_reviews(request):
    tickets = Ticket.objects.all()
    return render(request, "reviews/main.html", locals())


def add_ticket(request, ticket_id=None):

    # ticket_instance = Ticket.objects.get(pk=ticket_id) if ticket_id else None
    ticket_instance = get_object_or_404(Ticket, pk=ticket_id) if ticket_id else None

    if request.method == "GET":
        print("GET:", ticket_instance, ticket_id)
        form = TicketForm(instance=ticket_instance)
        return render(request, "reviews/ticket.html", locals())

    elif request.method == "POST":
        print("POST:", ticket_instance, ticket_id)
        form = TicketForm(request.POST, request.FILES, instance=ticket_instance)

        if form.is_valid():
            ticket = form.save()
            return redirect("reviews:main_reviews")

        return render(request, "reviews/ticket.html", locals())


def add_review(request, review_id=None):

    review_instance = get_object_or_404(Review, pk=review_id) if review_id else None

    if request.method == "GET":
        print("GET:", review_instance, review_id)
        form = ReviewForm(instance=review_instance)
        return render(request, "reviews/review.html", locals())

    elif request.method == "POST":
        print("POST:", review_instance, review_id)
        form = ReviewForm(request.POST, request.FILES, instance=review_instance)

        if form.is_valid():
            review = form.save()
            return redirect("reviews:main_reviews")

        return render(request, "reviews/review.html", locals())
