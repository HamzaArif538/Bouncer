from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Your Name'}))
    phone_number = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'placeholder': 'Your Phone Number'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Your Email'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Your Message'}))