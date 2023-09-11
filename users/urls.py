from . import views
from django.urls import path
from djoser.views import TokenCreateView, TokenDestroyView

urlpatterns = [
    path('login/', TokenCreateView.as_view(), name='login'),
    path('logout/', TokenDestroyView.as_view(), name='logout'),
    path('page/', views.ProtectedView.as_view(), name='page')
]
