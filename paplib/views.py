from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Mountain, ClimbRecord
from .forms import ClimbRecordForm

def mountain_list(request):
    mountains = Mountain.objects.all()
    context = {'mountains': mountains}
    return render(request, 'paplib/mountain_list.html', context)

def mountain_detail(request, pk):
    mountain = Mountain.objects.get(pk=pk)
    
    if request.method == 'POST':
        form = ClimbRecordForm(request.POST)
        if form.is_valid():
            new_record = form.save(commit=False)
            new_record.user = request.user
            new_record.mountain = mountain
            new_record.save()
            return redirect('mountain_detail', pk=mountain.pk) 
    else:
        form = ClimbRecordForm()

    records = ClimbRecord.objects.filter(mountain=mountain).order_by('-climb_date')

    context = {
        'mountain': mountain,
        'records': records, 
        'form': form,
    }
    return render(request, 'paplib/mountain_detail.html', context)