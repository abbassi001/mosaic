from django.forms import modelformset_factory
from django import  forms
from .models import InvoiceItem


class InvoiceItemForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(InvoiceItemForm, self).__init__(*args, **kwargs)
        self.fields['monthly_price'].widget.attrs['readonly'] = True

    class Meta:
        """Meta definition for InvoiceItemform."""

        model = InvoiceItem
        exclude = ['id', 'invoice']
        
InvoiceItemFormset = modelformset_factory(InvoiceItem, form=InvoiceItemForm)

