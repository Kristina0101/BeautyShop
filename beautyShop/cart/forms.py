from django import forms
from shop.models import Products


class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(label="Количество", coerce=int)
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)

    def __init__(self, *args, max_quantity=20, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['quantity'].choices = [(i, str(i)) for i in range(1, max_quantity + 1)]