from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views import View


class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request, "index.html")

    def post(self, request, *args, **kwargs):
        return HttpResponseRedirect()
