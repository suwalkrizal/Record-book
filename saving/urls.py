from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from . import views

router = DefaultRouter()
router.register('members', GroupMemberViewSet)
router.register('records', RecordViewSet)
router.register('deposits', DepositedByViewSet)


urlpatterns = [
    path('api/', include(router.urls)),
    
    path('login/', views.login_view, name='login'),
]
