from django import forms

class PropertySearch(forms.Form):
    location = forms.CharField(required=False)
    name = forms.CharField(required=False)
    min_price = forms.DecimalField(required=False)
    max_price = forms.DecimalField(required=False)



    