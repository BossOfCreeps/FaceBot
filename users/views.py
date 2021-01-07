from django.contrib.auth import logout, login
from django.core.mail import send_mail
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.utils.html import strip_tags
from django.views import View
from jinja2 import Template

from FaceBot import settings
from users.models import CustomUser


class SignUp(View):
    def post(self, request, *args, **kwargs):
        user = CustomUser.objects.create_user(request.POST["email"], request.POST["password"], is_active=False)
        m = Template(open('main/templates/mail_template.html').read()).render(user=user)
        send_mail('FaceBot account activation', strip_tags(m), settings.EMAIL_HOST_USER, [user.email], html_message=m)
        return HttpResponseRedirect(request.GET.get("path", ""))


class SignIn(View):
    def post(self, request, *args, **kwargs):
        if CustomUser.objects.get(email=request.POST["email"]).check_password(request.POST["password"]):
            login(request, CustomUser.objects.get(email=request.POST["email"]))
        return HttpResponseRedirect(request.GET.get("path", ""))


class SignOut(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(request.GET.get("path", ""))


class Activate(View):
    def get(self, request, *args, **kwargs):

        user = CustomUser.objects.filter(activation_token=request.GET["activation_token"]).order_by("-id")[0]
        if not user.is_active:
            user.is_active = True
            user.activation_token = "NULL"
            user.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return HttpResponseRedirect(reverse('index'))
        else:
            raise Http404()
