from django.shortcuts import render
from django.http import HttpResponse




def index(request):
    

    return render(request, 'Financo/index.html')


def about_us(request):
    
    return render(request,"Financo/about-us.html")
