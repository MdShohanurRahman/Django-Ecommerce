from ckeditor.widgets import CKEditorWidget
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *
import datetime


class createad(forms.ModelForm):
    # description = forms.CharField(label='', widget=CKEditorWidget(
    #     attrs={"placeholder": "write short description ", 'class': 'richtexteditor', }))
    class Meta:
        model = MesService
        fields = '__all__'
        exclude = ['ad_author', 'check']


class createAuthor(forms.ModelForm):
    Date_Of_Birth = forms.DateField(
        widget=forms.widgets.DateInput(attrs={'type': 'date', 'title': 'Date Of Birth'}))
    contact = forms.CharField(widget=forms.TextInput(
        attrs={"placeholder": "01xxxxxxxxx", }))

    class Meta:
        model = AuthorProfile
        fields = '__all__'
        exclude = ['name', 'check']

    def clean_contact(self, *args, **kwargs):
        contact = self.cleaned_data.get('contact')
        if len(contact) != 11:
            raise forms.ValidationError("your contact is not valid")
        else:
            return contact


# class creteCategory(forms.ModelForm):
#     class Meta: 
#         model = Category

#         fields = [
#             'category_name',
#         ]

class LoginForm(forms.Form):
    username = forms.CharField(label='Username or Email', widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput)


class registerUser(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2',
        ]

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError('This email has already taken')
        return email


class EducationInfoForm(forms.ModelForm):
    student_id = forms.CharField(widget=forms.TextInput(
        attrs={"placeholder": 'it-15059'}))

    class Meta:
        model = TuitionService
        fields = '__all__'
        exclude = ['ad_author', 'check']

    def __init__(self, *args, **kwargs):
        super(EducationInfoForm, self).__init__(*args, **kwargs)
        self.fields["category"].widget = forms.widgets.CheckboxSelectMultiple()
        self.fields["category"].help_text = "check item, which you are best.you can multiple select"
        self.fields["category"].queryset = TuitionServiceSubject.objects.all()
        self.fields['category'].label = 'Check your interest'
