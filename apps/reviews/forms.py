from django.forms import ModelForm, ImageField, FileInput  # , HiddenInput

from apps.reviews.models import Ticket, Review


class TicketForm(ModelForm):

    image = ImageField(
        label=("Image"),
        required=False,
        error_messages={"invalid": ("Image files only")},
        widget=FileInput,
    )

    class Meta:
        model = Ticket
        fields = ["title", "description", "image"]
        # widgets = {'user': HiddenInput()}
        labels = {
            'title': 'Titre',
            'description': 'Description',
        }


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ["headline", "rating", "body"]

        labels = {
            'headline': 'Titre de la revue',
            'rating': 'Evaluation',
            'body': 'Revue',
        }
