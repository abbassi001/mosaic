from django import template
from mosaic_app.models import Invoice

register = template.Library()

@register.filter
def get_chat_name(chat, request):
    name = ""
    if chat.participants.count() == 2:
        for usr in chat.participants.all():
            if usr != request.user:
                name = f"{usr}"
    else:
        for usr in chat.participants.all():
            if usr != request.user:
                name = f'{name.join(f"{usr}")}, '
    return name

@register.simple_tag
def invoice_numbers():
    invoices = Invoice.objects.all()
    
    return {
        "paid":invoices.filter(status="paid").count(),
        "unpaid":invoices.filter(status="unpaid").count(),
        "all":invoices.count(),
        }