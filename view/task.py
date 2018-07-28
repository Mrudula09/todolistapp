from django.views import View
from django.views.generic import CreateView,ListView,DeleteView,UpdateView
from django.forms import ModelForm
from django import forms
from django.shortcuts import render,redirect,reverse,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.urls import reverse_lazy

from todoapp.models import *

class AddTask(forms.ModelForm):
    class Meta:
        model = Task
        exclude =['id','user']
        fields = ('description','type','deadline','title')

class TaskList(LoginRequiredMixin,ListView):
    login_url = '/login/'
    model = Task
    form_class = AddTask
    context_object_name = 'result'
    template_name = 'task_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TaskList,self).get_context_data(**kwargs)
        context['result'] = self.model.objects.filter(user=self.request.user).values()
        context.update({'user_permissions': self.request.user.get_all_permissions})
        return context

class AddTaskView(LoginRequiredMixin,CreateView):
    login_url = '/login/'
    template_name = 'add_task.html'
    model = Task
    form_class = AddTask
    def get_context_data(self, **kwargs):
        context = super(AddTaskView, self).get_context_data(**kwargs)
        context.update({
            'form': context.get('form'),
            'user_permissions': self.request.user.get_all_permissions()
        })
        return context


    def post(self, request, *args, **kwargs):
        user = self.request.user
        task_form = AddTask(request.POST)
        if task_form.is_valid():
            task = task_form.save(commit=False)
            task.user=user
            task.save()
        return redirect('task_list')

class UpdateTask(LoginRequiredMixin,UpdateView):
    login_url = '/login/'
    form_class = AddTask
    template_name = 'update.html'
    model = Task

    def get_context_data(self, **kwargs):
        context = super(UpdateTask,self).get_context_data(**kwargs)
        task_form = context.get('task')
        context.update({
            'form' : context.get('form')
        })
        return context

    def post(self, request, *args, **kwargs):
        task = Task.objects.get(pk=kwargs.get('pk'))
        task_form = AddTask(request.POST,instance=task)
        task_form.save()
        return redirect('task_list')

class DeleteTask(LoginRequiredMixin,DeleteView):
    login_url = '/login/'
    model = Task
    template_name = 'add_task.html'
    form_class = AddTask
    success_url = 'task_list'
    def get(self, request,*args,**kwargs):
        return self.post(request,*args,**kwargs)

    def post(self, request, *args, **kwargs):
        self.delete(request,args,kwargs)
        return redirect('task_list')