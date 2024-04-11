from django import forms

class AuctionListingForm(forms.Form):
    title = forms.CharField(
        label='Title',
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'from-control from-group',
            'placeholder':'Give it a Title '
        })
    )