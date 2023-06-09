from django.http import HttpResponseRedirect
from django.urls import reverse_lazy


class DefaultMixin:
    title = 'RED'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title

        return context


class ValidateMixin:
    @staticmethod
    def check_password(password: str, repeat_password: str, username: str):
        if password == repeat_password and len(password) >= 8 and (
                not password.isnumeric()) and username != password:
            return True
        else:
            return False


class AnonymousRequiredMixin:
    anonymous_redirect_url = reverse_lazy('index')

    def get_context_data(self, *args, **kwargs):
        if not self.user.is_anonymous():
            return HttpResponseRedirect(self.anonymous_redirect_url)
        return super().get_context_data(*args, **kwargs)
