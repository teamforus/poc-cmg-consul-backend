from django.shortcuts import render
from django.views import generic
from django.views.generic import TemplateView



class IndexView(TemplateView):
    template_name = 'dashboard/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)

        return context

# Create your views here.
