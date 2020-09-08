from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):
    contact_no = forms.CharField(widget=forms.TextInput(
        attrs={"placeholder": "01xxxxxxxxx", }))

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address', 'postal_code', 'contact_no']

    def clean_contact(self, *args, **kwargs):
        contact_no = self.cleaned_data.get('contact_no')
        if len(contact_no) != 11:
            raise forms.ValidationError("your contact is not valid")
        else:
            return contact_no
