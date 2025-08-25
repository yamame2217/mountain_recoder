from django.shortcuts import render
from .models import Mountain  

def mountain_list(request):
    mountains = Mountain.objects.all()
    context = {'mountains': mountains}
    return render(request, 'paplib/mountain_list.html', context) 