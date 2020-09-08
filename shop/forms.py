from django import forms
from django.contrib.auth.models import User
from .models import Comment, BookOrder


class ProductReviewForm(forms.ModelForm):
    post_comment = forms.CharField(label='', widget=forms.Textarea(
        attrs={"placeholder": "Your Review", "rows": "4"}))

    class Meta:
        model = Comment
        fields = '__all__'
        exclude = ['post', 'name']


class BookOrderForm(forms.ModelForm):
    edition = forms.CharField(label='Edition', widget=forms.TextInput(
        attrs={"placeholder": "example:7th", }))
    contact = forms.CharField(label='Contact', widget=forms.TextInput(
        attrs={"placeholder": "your phone number here", }))

    class Meta:
        model = BookOrder
        fields = '__all__'
