from django.http import HttpResponse
from django.shortcuts import render

def home_page(request):
    # return HttpResponse('homepage')
    return render(request, 'base_layout.html')
