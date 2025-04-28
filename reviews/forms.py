from django import forms
from reviews.models import Review
from users.forms import StyleFromMixin

class ReviewForm(StyleFromMixin, forms.ModelForm):
    class Meta:
        model = Review
        fields = ('dog', 'title', 'content', 'slug')