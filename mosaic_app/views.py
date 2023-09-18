from django.conf import settings
from django.shortcuts import render
from django.utils import translation
from django.shortcuts import render, HttpResponse, HttpResponseRedirect


def change_language(request, new_language):
    next_url = request.GET.get('next')
    response = HttpResponseRedirect(next_url) if next_url else HttpResponse(status=204)
    request.session[translation.LANGUAGE_SESSION_KEY] = new_language
    translation.activate(new_language)
    response.set_cookie(settings.LANGUAGE_COOKIE_NAME, new_language)
    return response


def index(request):
    

    return render(request, 'Financo/index.html')


def about_us(request):
    
    return render(request,"Financo/about-us.html")
