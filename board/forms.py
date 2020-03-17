from .models import Topic,Post
from django import forms

class TopicForm(forms.ModelForm):

    message=forms.CharField(widget=forms.Textarea(
    attrs={
    'rows':5,'placeholder':'What is your message'}
    ),max_length=4000,
    help_text="Max length is 4000"
    )

    class Meta:
        model=Topic
        fields=['subject','message']

class PostForm(forms.ModelForm):
    class Meta:
        model=Post
        fields=['message',]
        