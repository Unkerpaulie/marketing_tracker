from django import forms
from .models import Ad, Post
from .widgets import MarkdownRichTextWidget

class AdForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ['name', 'text', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ad Name'}),
            'text': MarkdownRichTextWidget(attrs={'class': 'form-control', 'placeholder': 'Ad Text (use markdown formatting)'}),
            'image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['ad', 'post_url', 'posted_at']
        widgets = {
            'ad': forms.Select(attrs={'class': 'form-control'}),
            'post_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Post URL'}),
            'posted_at': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }

