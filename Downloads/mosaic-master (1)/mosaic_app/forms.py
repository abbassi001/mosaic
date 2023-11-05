from django.forms import modelformset_factory
from django import  forms
from .models import InvoiceItem, FundItem

class InvoiceItemForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(InvoiceItemForm, self).__init__(*args, **kwargs)
        self.fields['monthly_price'].widget.attrs['readonly'] = True

    class Meta:
        """Meta definition for InvoiceItemform."""

        model = InvoiceItem
        exclude = ['id', 'invoice']
        
InvoiceItemFormset = modelformset_factory(InvoiceItem, form=InvoiceItemForm)

class FundItemForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FundItemForm, self).__init__(*args, **kwargs)

    class Meta:
        """Meta definition for FundItemform."""

        model = FundItem
        exclude = ['id', 'fundmanagement']
        
FundItemFormset = modelformset_factory(FundItem, form=FundItemForm)

