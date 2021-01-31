from django.forms import ModelForm  # , HiddenInput

from apps.reviews.models import Ticket, Review


class TicketForm(ModelForm):
    class Meta:
        model = Ticket
        fields = ["title", "description", "image", "user"]
        # widgets = {'user': HiddenInput()}


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ["ticket", "user", "headline", "rating", "body"]
