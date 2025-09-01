from django.shortcuts import render, redirect
from .models import Mountain, ClimbRecord
from .forms import ClimbRecordForm, MountainForm
from django.views.generic import UpdateView, DeleteView, CreateView, ListView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from rest_framework import generics, viewsets, permissions
from .serializers import MountainSerializer, ClimbRecordSerializer, UserSerializer
from .permissions import IsOwnerOrReadOnly

def mountain_list(request):
    mountains = Mountain.objects.all().order_by('name')
    query = request.GET.get('q')
    if query:
        mountains = mountains.filter(name__icontains=query)

    context = {'mountains': mountains}
    return render(request, 'paplib/mountain_list.html', context)

def mountain_detail(request, pk):
    mountain = Mountain.objects.get(pk=pk)
    
    if request.method == 'POST':
        form = ClimbRecordForm(request.POST, request.FILES) 
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

class MyPageView(LoginRequiredMixin, ListView):
    model = ClimbRecord
    template_name = 'paplib/mypage.html'
    context_object_name = 'records'
    paginate_by = 10 

    def get_queryset(self):
        return ClimbRecord.objects.filter(user=self.request.user).order_by('-climb_date')

class MountainDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Mountain
    template_name = 'paplib/mountain_confirm_delete.html'
    success_url = reverse_lazy('mountain_list')

    def test_func(self):
        return self.request.user.is_staff

class MountainUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Mountain
    form_class = MountainForm 
    template_name = 'paplib/mountain_form.html' 

    def get_success_url(self):
        return reverse_lazy('mountain_detail', kwargs={'pk': self.object.pk})

    def test_func(self):
        return self.request.user.is_staff

class UserCreateAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny] 

class MountainViewSet(viewsets.ModelViewSet):
    queryset = Mountain.objects.all()
    serializer_class = MountainSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ClimbRecordViewSet(viewsets.ModelViewSet):
    queryset = ClimbRecord.objects.all()
    serializer_class = ClimbRecordSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class RegisterPageView(TemplateView):
    template_name = 'paplib/register.html'

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser] 