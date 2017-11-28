from django.shortcuts import get_object_or_404, render

from django.views import generic
import operator
import sys
from .models import Ctgov
from django.db.models import Q
import requests
import functools


##class IndexView(generic.ListView):
#    template_name = 'trials/index.html'
#    context_object_name = 'latest_trials_list'
#    paginate_by = 25
#    def get_queryset(self):
#        return Ctgov.objects.order_by('-rank')

class DetailView(generic.DetailView):
    model = Ctgov
    template_name = 'trials/detail.html'

#class ResultsView(generic.DetailView):
#    model = Ctgov
#    template_name = 'trials/results.html'

class SearchListView(generic.ListView):
    """
    Display a List page filtered by the search query.
    """
    template_name = 'trials/index.html'
    context_object_name = 'latest_trials_list'
    paginate_by = 25
    def get_queryset(self):
        result = Ctgov.objects.order_by('-rank')

        query = self.request.GET.get('q')
        synonyms = []
        if query:
            query_list = query.split()
            for q in query_list:
                url = "http://havoc.appliedinformaticsinc.com/concepts?term=" + q + "&user=156&token=4qz-cd4f7154ada7eeb63249"
                r = requests.get(url)
                if r.status_code == 200:
                    if eval(r.text):
                        cui = eval(r.text)[0]['cui']
                    else:
                        continue
                url = "http://havoc.appliedinformaticsinc.com/concepts/"+cui+"/synonyms?user=156&token=4qz-cd4f7154ada7eeb63249"
                r = requests.get(url)
                if r.status_code == 200:
                    synonyms.extend(eval(r.text))
            if synonyms:
                result = result.filter(
                    functools.reduce(operator.or_,(Q(detailed_description_textblock__contains=q) for q in synonyms)))
            else:
                return result[0:0]

        return result