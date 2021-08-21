from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, View
from django import forms

from chat.models import Twitte, Follow


class TwitteCreateForm(forms.ModelForm):

    class Meta:
        fields = ['text']
        model = Twitte


class HomePage(LoginRequiredMixin, ListView):
    model = Twitte
    template_name = 'home.html'
    login_url = reverse_lazy('login')


class TwitteCreate(LoginRequiredMixin, CreateView):
    model = Twitte
    form_class = TwitteCreateForm
    template_name = 'create.html'
    success_url = reverse_lazy('chat:home')
    
    def get_context_data(self, **kwargs):
        return super(TwitteCreate, self).get_context_data(**kwargs)
    
    def form_valid(self, form):
        if form.is_valid():
            form.instance.user = self.request.user
            form.save()
            return HttpResponseRedirect(self.success_url)
        else:
            return super().form_valid(form)


class FollowView(LoginRequiredMixin, View):

    def get(self, request):
        twitte_id = self.request.GET.get('twitte_id')
        twitte = Twitte.objects.filter(id=twitte_id).first()
        if not Follow.objects.filter(twitte=twitte, user=self.request.user).exists():
            Follow.objects.create(twitte=twitte, user=self.request.user)
        return HttpResponseRedirect(reverse('chat:home'))
