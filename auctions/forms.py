from typing import Any
from django import forms

class AuctionListingForm(forms.Form):
    title = forms.CharField(
        label='Title',
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'from-control from-group',
            'placeholder':'Give it a Title '
        }
        )
    )

    description = forms.CharField(
        label='Description',
        required=True,
        widget=forms.Textarea(attrs={
            'class': 'form-control form-group',
            'placeholder': 'Tell more about product',
            'row': '3'
        }
        )
    )

    price = forms.DecimalField(
        label='Price',
        required=True,
        initial=0.00,
        widget=forms.NumberInput(attrs={
            'class': 'form-control form-group',
            'placeholder': 'Estimated Price (optional)',
            'min':'0.01',
            'max':'99999999.99',
            'step': '0.1'

        }
        )

    )

   
    starting_bid = forms.DecimalField(
        label='Starting bid',
        required=True,
        widget=forms.NumberInput(attrs={
            'class': 'form-control form-group',
            'placeholder': 'strating Bid',
            'min':'0.01',
            'max':'999999999.9',
            'step': '0.1'   
        }
        )
       
    )

    category = forms.CharField(
        label='Category',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-group',
            'autocomplete': 'on',
            'placeholder': 'Category (optional)'
        })
    )

    image_url = forms.URLField(
        label='Image URL',
        required=False,
        initial='https://images.app.goo.gl/h7sWyqSwujg2qvzN9',
        widget=forms.TextInput(attrs={
            'class': 'form-control form-group',
            'placeholder': 'Image URL (optional)',
        })
    )

    def clean_stsrting_bid(self):
        amount = float(self.cleaned_data.get('starting_bid'))
        if isinstance(amount,float) and amount > 0:
            return amount
        print(amount)
        raise forms.ValidationError('Should be a Number Larger Than 0')
    
    def clean_category(self):
        category = self.cleaned_data.get('category')
        return category.lower()
    

class CommentForm(forms.Form):
    text = forms.CharField(
        label='',
        required=True,
        widget=forms.Textarea(attrs={
            'class': 'form-control-md lead form-group',
            'row': '3',
            'cols':'100'
        }
        )
    )

    def clean_comment(self):
        text = self.cleaned_data.get('text')
        if len(text) > 0:
            return text
        return self.errors