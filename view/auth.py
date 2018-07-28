from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404, redirect


class loginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()

class loginView(View):
    def get(self,request):
        form = loginForm
        return render(request,template_name='login.html',context={'form':form})

    def post(self,request):
        form = loginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(
                request,
                username=username,
                password=password
            )
            if user is not None:
                login(request,user)
                return redirect('task_list')
            return redirect('login_page')

def logout_user(request):
    logout(request)
    return redirect('login_page')

class signUpForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    username = forms.CharField()
    password = forms.CharField()

class signupView(View):
    def get(self,request):
        form = signUpForm
        return render(request,template_name='signup.html',context={'form':form})

    def post(self,request):
        form = signUpForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(**form.cleaned_data)
            user = authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user is not None:
                login(request, user)

        return redirect('task_list')