from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.views.generic import CreateView, DetailView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.conf import settings

from .forms import LoginUserForm, RegisterUserForm, ProfileUpdateForm, UserPasswordChangeForm


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    redirect_authenticated_user=True
    
    
class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')
    redirect_authenticated_user=True
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')  
        return super().dispatch(request, *args, **kwargs)

    

class ProfileUser(DetailView):
    model = get_user_model()
    template_name = 'users/profile.html'
    extra_context = {'default_image': settings.DEFAULT_USER_IMAGE}
    
    def get_object(self, queryset=None):
        return self.request.user
    
    def __str__(self):
        return self.username
    
    
class EditProfile(UpdateView):
    model = get_user_model()
    template_name = 'users/edit_profile.html'
    form = ProfileUpdateForm
    fields = ['photo', 'username']
    success_url = reverse_lazy('users:profile')
    
    def get_object(self, queryset=None):
        return self.request.user
    
    
class UserPasswordChange(PasswordChangeView):
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy("users:password_change_done")
    template_name = "users/password_change_form.html"
