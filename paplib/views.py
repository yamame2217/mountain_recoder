from django.shortcuts import render
from .models import Mountain  

def mountain_list(request):
    mountains = Mountain.objects.all()
    context = {'mountains': mountains}
    return render(request, 'paplib/mountain_list.html', context)

def mountain_detail(request, pk):
    mountain = Mountain.objects.get(pk=pk) 
    context = {'mountain': mountain}
    return render(request, 'paplib/mountain_detail.html', context)