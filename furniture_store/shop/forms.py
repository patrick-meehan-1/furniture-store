from . models import Review
from django import  forms

class ReviewForm(forms.ModelForm):
    # Define choices for the rating field
    RATING_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )

    # Override the rating field to use ChoiceField with the defined choices
    rating = forms.ChoiceField(choices=RATING_CHOICES, label='Rating')

    class Meta:
        model = Review
        fields = ["review", "rating"]
    
    