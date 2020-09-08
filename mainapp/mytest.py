from django import forms
from .models import *
import datetime

BIRTH_YEAR_CHOICES = ('1980', '1981', '1982')
FAVORITE_COLORS_CHOICES = (
    ('blue', 'Blue'),
    ('green', 'Green'),
    ('black', 'Black'),
)
CHOICES = [('select1', 'select 1'),
           ('select2', 'select 2')]


class ProductForm(forms.ModelForm):
    title = forms.CharField(label='Your Title',
                            widget=forms.TextInput(
                                attrs={"placeholder": "your title", "size": 10, }))

    description = forms.CharField(help_text='Not more than 100 character',
                                  required=False, widget=forms.Textarea(
            attrs={
                "class": "new-class-name two",
                "id": "my-id-for-textarea",
                'title': 'Description',
                "rows": '10',
                "cols": '30',
                'size': '40'

            }
        ))
    price = forms.DecimalField(initial=120.22)
    captcha_answer = forms.IntegerField(label='2 + 2', label_suffix=' =')
    mobileno = forms.CharField(initial='+880')
    day = forms.DateField(initial=datetime.date.today)
    birth_year = forms.DateField(widget=forms.SelectDateWidget(years=BIRTH_YEAR_CHOICES))
    favorite_colors = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=FAVORITE_COLORS_CHOICES,
    )

    select = forms.ChoiceField(
        required=False,
        # widget=forms.Select,
        widget=forms.RadioSelect,
        choices=CHOICES,
    )

    my_choice_field = forms.ChoiceField(choices=CHOICES)

    class Meta:
        model = Product
        fields = [
            'title',
            'description',
            'price'
        ]

    def clean_title(self, *args, **kwargs):
        title = self.cleaned_data.get('title')
        if 'shohan' not in title:
            raise forms.ValidationError("shohan is not there")
        elif 'shomik' not in title:
            raise forms.ValidationError("shomik is not there")
        if not title.endswith(".com"):
            raise forms.ValidationError("this is not ends with .com")
        else:
            return title


class RawProducForm(forms.Form):
    title = forms.CharField(label='', widget=forms.TextInput(attrs={"placeholder": "your title"}))
    description = forms.CharField(required=False, widget=forms.Textarea(
        attrs={
            "class": "new-class-name two",
            "id": "my-id-for-textarea",
            "rows": 20,
            "cols": 100
        }
    ))
    price = forms.DecimalField()

    