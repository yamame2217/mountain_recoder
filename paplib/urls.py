from django.urls import path
from . import views
from .views import ClimbRecordUpdateView, ClimbRecordDeleteView

urlpatterns = [
    path('', views.mountain_list, name='mountain_list'),
    path('mountain/<int:pk>/', views.mountain_detail, name='mountain_detail'),
    path('record/<int:pk>/edit/', ClimbRecordUpdateView.as_view(), name='record_edit'),
    path('record/<int:pk>/delete/', ClimbRecordDeleteView.as_view(), name='record_delete'),
]