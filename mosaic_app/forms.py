from django.forms import modelformset_factory
from django import  forms
from .models import InvoiceItem


class InvoiceItemForm(forms.ModelForm):
    """Form definition for InvoiceItem."""

    class Meta:
        """Meta definition for InvoiceItemform."""

        model = InvoiceItem
        exclude = ['invoice']
        
InvoiceItemFormset = modelformset_factory(InvoiceItem, form=InvoiceItemForm)

