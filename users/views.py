from django.shortcuts import render , HttpResponse , redirect , get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm , UserUpdateForm , ProfileUpdateForm , ChangePasswordForm
from verify_email.email_handler import send_verification_email , send_mail
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import os
from .models import Follow
from blog.models import Post
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
"""def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            inactive_user = send_verification_email(request, form)
            #username = form.cleaned_data.get('username')
            messages.info(request , "Confirmation Email Sent!")
            return redirect('login')
    else:
        form = UserRegisterForm()
        return render(request , 'users/register.html' , {'form' : form})"""

class register(View):
    template_name = 'users/register.html'
    
    def get(self , request):
        form = UserRegisterForm()
        return render(request , self.template_name , {'form':form})
    
    def post(self , request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            inactive_user = send_verification_email(request, form)
            username = form.cleaned_data.get('username')
            messages.info(request , "Confirmation Email Sent!")
            return redirect('login')
        else:
            return redirect('register')


class profile(LoginRequiredMixin , View):
    template_name = 'users/profile.html'
    def get(self , request):
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(request.FILES , instance=request.user.profile)
        context = {
            'u_form':u_form,
            'p_form':p_form
        }
        return render(request , self.template_name , context)
    def post(self , request):
        u_form = UserUpdateForm(request.POST , instance=request.user)
        p_form = ProfileUpdateForm(request.POST , request.FILES , instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request , 'your account has been updated')
            return redirect('profile')
        else:
            errors = {
                'u_errors':u_form.errors,
                'p_errors':p_form.errors,
            }
            messages.error(request , f"{errors.values()}")
            return redirect('profile')
"""
@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST , instance=request.user)
        p_form = ProfileUpdateForm(request.POST , request.FILES ,instance=request.user.profile)
        old_img_path = request.user.profile.image.path
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            if 'image' in p_form.changed_data:
                if os.path.exists(old_img_path):
                    os.remove(old_img_path)
            messages.success(request , f'Your Account has been updated!')
            return redirect('profile')
        else :
            messages.error(request , u_form.errors)
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        context = {
        'u_form' : u_form,
        'p_form' : p_form,
        }
    return render(request , 'users/profile.html' , context)"""

class change_password(LoginRequiredMixin , View):
    def get(self , request):
        form = ChangePasswordForm()
        return render(request , 'users/change_password.html' , {'form':form})
    def post(self , request):
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            user = request.user
            current_password = form.cleaned_data.get('current_password')
            new_password = form.cleaned_data.get('new_password')
            confirm_new_password = form.cleaned_data.get('confirm_new_password')
            if user.check_password(current_password) and new_password == confirm_new_password:
                user.set_password(new_password)
                user.save()
                messages.success(request , 'Password Changed Successfully')
                return redirect('login')
            if not user.check_password(current_password):
                messages.error(request , 'Incorrect Current Password')
                return redirect('change-password')
            if new_password != confirm_new_password:
                messages.error(request , 'Passwords not match')
                return redirect('change-password')    
        else:
            return redirect('change-password')  
"""@login_required
def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            user = request.user
            current_password = form.cleaned_data.get('current_password')
            new_password = form.cleaned_data.get('new_password')
            confrim_new_password = form.cleaned_data.get('confirm_new_password')
            if user.check_password(current_password) and new_password == confrim_new_password:
                user.set_password(new_password)
                user.save()
                messages.success(request , "Password change successfully!")
                return redirect('blog-home')
            elif not user.check_password(current_password):
                messages.error(request , "Incorrect current password!")
                return redirect('change-password')
            elif new_password != confrim_new_password:
                messages.error(request , "Passwords not match!")
                return redirect('change-password')
    else:
        form = ChangePasswordForm()
        return render(request , 'users/change_password.html' , {'form' : form})"""

@login_required
def UserProfile(request , author):
    post_author = User.objects.get(username=author)
    post = Post.objects.filter(author=post_author).first()
    user = request.user
    if (Follow.objects.filter(user = post_author , follower = user)):
        button_text = 'Unfollow'
    else:
        button_text = 'follow'
    context = {
        'post_author': post_author,
        'post': post,
        'button_text' : button_text
    }
    return render(request , 'Users/user-profile.html' , context)

@login_required
def FollowUser(request, author):
    follower = request.user
    post_author = User.objects.get(username = author)
    follow = Follow.objects.filter(user=post_author, follower=follower).first()

    if follow is None and post_author != follower:
        follow_obj = Follow.objects.create(user=post_author, follower=follower)
    else:
        follow.delete()

    return redirect('user-profile' , author)