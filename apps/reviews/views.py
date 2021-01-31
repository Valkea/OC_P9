from django.shortcuts import render, redirect

from apps.reviews.forms import TicketForm
from apps.user_graph.models import User


def main_reviews(request):
    return render(request, "reviews/main.html")


def add_ticket(request, ticket_id=None):

    if request.method == "GET":
        form = TicketForm()
        return render(request, 'reviews/ticket.html', locals())

    elif request.method == "POST":
        form = TicketForm(request.POST, request.FILES)

        # user = User.objects.create_user("Bobby2", "email@shedge.com", "bob")
        # user = User.objects.get(pk="1")
        # print(user)
        # form.user = user
        # form.user_id = user.id

        if form.is_valid():
            print("Coucou")
            ticket = form.save()
            # ticket = Ticket.objects.create(user=user, )

        return redirect('reviews:main_reviews')


def OLD_ticket(request, ticket_id=None):
    print("ticket_id:", ticket_id)
    if ticket_id is None:
        # if request.method == 'GET':
        return render(request, "reviews/ticket.html", {"id": 4})
    else:
        # elif request.method == 'POST':
        return render(request, "reviews/ticket.html", {"id": ticket_id})
