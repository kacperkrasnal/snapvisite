from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy


class OwnerAccessMixin(UserPassesTestMixin):

    def test_func(self):
        obj = self.get_object()
        return obj.owner == self.request.user


class UserConfirmMixin(UserPassesTestMixin):

    @property
    def test_func(self):
        try:
            obj = self.get_object()
            confirmed = obj.confirm
            if not confirmed:
                raise PermissionDenied
            elif confirmed:
                return True
        except AttributeError:
            HttpResponseRedirect(reverse_lazy("snapvisite:home-page"), {'messages': 'Before using our service you '
                                                                                    'need to register and confirm '
                                                                                    'your email address.'})
