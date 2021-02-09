from django.forms import (
    ModelForm,
    ImageField,
    FileInput,
    RadioSelect,
    ChoiceField,
    Textarea,
)

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
            "title": "Titre",
            "description": "Description",
        }

        widgets = {
            "description": Textarea(attrs={"class": "ticket__textarea"}),
        }


class ReviewForm(ModelForm):
    # rating = CharField(label='Rating', widget=TextInput(attrs={'min': 1, 'max': '5', 'type': 'number'}))
    CHOICES = [(str(x), str(x)) for x in range(0, 6)]
    # CHOICES = [('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')]
    rating = ChoiceField(label="Evaluation", widget=RadioSelect, choices=CHOICES)

    class Meta:
        model = Review
        fields = ["headline", "rating", "body"]

        labels = {
            "headline": "Titre de la revue",
            "rating": "Evaluation",
            "body": "Revue",
        }

        widgets = {
            "body": Textarea(attrs={"class": "review__textarea"}),
        }
