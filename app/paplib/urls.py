from django.urls import path
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from . import views
from .views import (
    ClimbRecordUpdateView, 
    ClimbRecordDeleteView, 
    MountainCreateView, 
    MountainUpdateView, 
    MountainDeleteView,
    MyPageView
)

router = routers.DefaultRouter()
router.register(r'mountains', views.MountainViewSet)
router.register(r'records', views.ClimbRecordViewSet)
router.register(r'users', views.UserViewSet)

urlpatterns = [
    path('', views.mountain_list, name='mountain_list'),
    path('mountain/add/', MountainCreateView.as_view(), name='mountain_add'),
    path('mountain/<int:pk>/', views.mountain_detail, name='mountain_detail'),
    path('mountain/<int:pk>/edit/', MountainUpdateView.as_view(), name='mountain_edit'), 
    path('mountain/<int:pk>/delete/', MountainDeleteView.as_view(), name='mountain_delete'),
    path('record/<int:pk>/edit/', ClimbRecordUpdateView.as_view(), name='record_edit'),
    path('record/<int:pk>/delete/', ClimbRecordDeleteView.as_view(), name='record_delete'),
    path('mypage/', MyPageView.as_view(), name='mypage'),

    path('api/', include(router.urls)),
]