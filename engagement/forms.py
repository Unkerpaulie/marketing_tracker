from django import forms
from .models import Contact, Engagement

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'fb_url']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contact Name'}),
            'fb_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Facebook URL'}),
        }

class EngagementForm(forms.ModelForm):
    class Meta:
        model = Engagement
        fields = ['contact', 'content', 'notes', 'message_url']
        widgets = {
            'contact': forms.Select(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Engagement Content', 'rows': 4}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Notes', 'rows': 3}),
            'message_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Message URL (optional)'}),
        }

