from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth.models import AnonymousUser


class DefaultMixin:
    title = 'RED'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title

        return context


class ValidateMixin:
    @staticmethod
    def check_password(password: str, repeat_password: str, username: str):
        return password == repeat_password and len(password) >= 8 and (
                not password.isnumeric()) and username != password

    @staticmethod
    def check_username(username: str):
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890@.+-_"
        for symbol in username:
            if symbol in alphabet:
                continue
            else:
                return False
        else:
            return True


class AnonymousRequiredMixin:
    anonymous_redirect_url = reverse_lazy('index')

    def get(self, *args, **kwargs):
        if not self.request.user.is_anonymous:
            return HttpResponseRedirect(self.anonymous_redirect_url)
        return super().get(*args, **kwargs)


class RequestInFormMixin:
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


class FormWithRequestMixin:
    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

