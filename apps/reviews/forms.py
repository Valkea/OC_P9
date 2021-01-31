from django.forms import ModelForm, HiddenInput

from apps.reviews.models import Ticket


class TicketForm(ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image', 'user']
        # widgets = {'user': HiddenInput()}
