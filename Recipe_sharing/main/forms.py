# forms.py
from django import forms
from recipe.models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Add a comment...'}),
        }
