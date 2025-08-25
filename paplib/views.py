from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Mountain, ClimbRecord
from .forms import ClimbRecordForm, MountainForm
from django.views.generic import UpdateView, DeleteView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy

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

class ClimbRecordUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ClimbRecord
    form_class = ClimbRecordForm
    template_name = 'paplib/record_form.html'

    def get_success_url(self):
        record = self.get_object()
        return reverse_lazy('mountain_detail', kwargs={'pk': record.mountain.pk})

    def test_func(self):
        record = self.get_object()
        return self.request.user == record.user

class ClimbRecordDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = ClimbRecord
    template_name = 'paplib/record_confirm_delete.html'

    def get_success_url(self):
        record = self.get_object()
        return reverse_lazy('mountain_detail', kwargs={'pk': record.mountain.pk})

    def test_func(self):
        record = self.get_object()
        return self.request.user == record.user

class MountainCreateView(LoginRequiredMixin, CreateView):
    model = Mountain
    form_class = MountainForm
    template_name = 'paplib/mountain_form.html'
    success_url = reverse_lazy('mountain_list')