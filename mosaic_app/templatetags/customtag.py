from django import template

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