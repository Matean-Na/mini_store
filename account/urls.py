from django.urls import path, include
from .views import LoginView, RegistrationView, activate, profile
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('active/<uidb64>/<token>/', activate, name='activate'),
    path('profile/', profile, name='profile'),
    path('logout/', LogoutView.as_view(next_page="product_list"), name='logout'),
]