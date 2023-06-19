from typing import Any
from django import http
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import UserRegisterForm, UserLoginForm, EditProfileForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Relation


class UserRegisterView(View):
    form_class = UserRegisterForm
    template_name = 'accounts/register.html'
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.error(request, 'You are logged in', 'danger')
            redirect('shop:home')
        return super().dispatch(request, *args, **kwargs)
            
    
    
    def get(self, request, *args, **kwargs):
        form = self.form_class
        return render(request, self.template_name, {
            "form": form
        })
    
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.create_user(username=cd['username'], email=cd['email'], password=cd['password1'])
            messages.success(request, 'Registered', 'success')
            login(request, user)
            return redirect('shop:home')
        return render(request, self.template_name, {
            "form": form 
        })
            
            
class UserLoginView(View):
    form_class = UserLoginForm
    template_name = 'accounts/login.html'
    
    def setup(self, request, *args, **kwargs):
        self.next = request.GET.get('next')
        return super().setup(request, *args, **kwargs)
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.error(request, 'You are logged in', 'danger')
            return redirect('shop:home')
        return super().dispatch(request, *args, **kwargs)
    
    
    def get(self, request, *args, **kwargs):
        form = self.form_class
        return render(request, self.template_name, {
            "form": form 
        })
    
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, "Logged in", "success")
                if self.next:
                    return redirect(self.next)
                return redirect('shop:home')
            messages.error(request, "username and password doesn't match", "danger")
        return render(request, self.template_name, {
            "form": form
        })
        
class UserLogoutView(LoginRequiredMixin, View):
    
    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, 'Logged out', "success")
        return redirect('shop:home')
    
    
    
class UserProfileView(LoginRequiredMixin, View):
    
    def setup(self, request, *args, **kwargs):
        self.user = get_object_or_404(User, pk=kwargs['user_id'])
        self.followed = self.user.follower.count()
        self.followings = self.user.following.count()
        return super().setup(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        user = self.user
        posts = user.user_posts.all()
        is_following = False
        relation = Relation.objects.filter(from_user=request.user, to_user=user)
        if relation.exists():
            is_following = True
        return render(request, 'accounts/profile.html', {
            "user": user,
            "posts": posts ,
            "is_following": is_following,
            "followed": self.followed,
            "following": self.followings
        })
        
        
        
class FollowUserView(LoginRequiredMixin, View):
    
    def setup(self, request, *args, **kwargs):
        self.user_instance = get_object_or_404(User, pk=kwargs['user_id'])
        return super().setup(request, *args, **kwargs)
    
    
    def dispatch(self, request, *args, **kwargs):
        user = self.user_instance
        if request.user != user:
            return super().dispatch(request, *args, **kwargs)
        messages.error(request, 'You can not follow yourself', 'danger')
        return redirect('accounts:profile', self.user_instance.id)
    
    
    def get(self, request, *args, **kwargs):
        if Relation.objects.filter(from_user=request.user, to_user=self.user_instance).exists():
            messages.error(request, 'You have already followed this user')
        else:
            Relation.objects.create(from_user=request.user, to_user=self.user_instance)
            messages.success(request, 'You have followed this user', 'success')
        return redirect('accounts:profile', self.user_instance.id)
            
        
        
class UnfollowUserView(LoginRequiredMixin, View):
    
    def setup(self, request, *args, **kwargs):
        self.user_instance = User.objects.get(pk=kwargs['user_id'])
        return super().setup(request, *args, **kwargs)
    
    def dispatch(self, request, *args, **kwargs):
        if request.user != self.user_instance:
            return super().dispatch(request, *args, **kwargs)
        messages.error(request, 'You cant follow or unfollow yourself', 'danger')
        return redirect('accounts:profile', self.user_instance.id)
    
    def get(self, request, *args, **kwargs):
        relation = Relation.objects.filter(from_user=request.user, to_user=self.user_instance)
        if relation.exists():
            relation.delete()
            messages.success(request, 'Unfollowed')
        else:
            messages.error(request, 'You have not followed this user yet', 'danger')
        return redirect("accounts:profile", self.user_instance.id)
    

class UserGetFollowersView(LoginRequiredMixin, View):
    
    def setup(self, request, *args, **kwargs):
        self.user_instance = User.objects.get(pk=kwargs['user_id'])
        return super().setup(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        final_list = self.user_instance.follower.all()
        return render(request, 'accounts/followers.html', {
            "followers": final_list
        })
            

class UserGetFollowingsView(LoginRequiredMixin, View):
    
    def setup(self, request, *args, **kwargs):
        self.user_instance = User.objects.get(pk=kwargs['user_id'])
        return super().setup(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        final_list = self.user_instance.following.all()
        return render(request, 'accounts/followings.html', {
            "followings": final_list
        })
        

class EditProfileView(LoginRequiredMixin, View):
    form_class = EditProfileForm
    
    def get(self, request, *args, **kwargs):
        form = self.form_class(instance=request.user.profile, initial={"email": request.user.email})
        return render(request, 'accounts/edit_user.html', {
            "form": form
        })
        
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            request.user.email = form.cleaned_data['email']
            request.user.save()
            messages.success(request, 'edited', 'success')
        return redirect("accounts:profile", request.user.id)