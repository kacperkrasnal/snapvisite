import datetime

from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, View
from snapvisite.mixins import UserConfirmMixin
from snapvisite.models import Appointment

from .forms import ConfirmMailForm
from .forms import RegistrationProfileForm, UpdateProfileForm
from .models import Profile
from .utils import account_confirmation_mail


class CreateProfileView(SuccessMessageMixin, CreateView):
    form_class = RegistrationProfileForm
    template_name = 'account/registration_form.html'
    success_message = 'Your account has been created successfully.'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.save()
        #account_confirmation_mail(obj.user_name, obj.email, obj.id)
        return HttpResponseRedirect(reverse_lazy('snapvisite:home-page'))


class ResendConfirmationMail(SuccessMessageMixin, View):
    success_message = 'Confirmation link sent successfully on your account email.'

    def get(self, *args):
        user = self.request.user
        account_confirmation_mail(user.user_name, user.email, user.id)
        return HttpResponseRedirect(reverse_lazy('snapvisite:home-page'))


class DetailProfileView(UserConfirmMixin, DetailView):
    model = Profile

    def test_func(self):
        try:
            user = self.request.user
            confirmed = user.confirm
            if not confirmed:
                raise PermissionDenied
            elif confirmed:
                return True
        except AttributeError:
            HttpResponseRedirect(reverse_lazy("snapvisite:home-page"))


class UpdateProfileView(UpdateView):
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'account/profile_edit.html'

    def get_success_url(self):
        pk = self.kwargs["pk"]
        return reverse("account:profile_detail", kwargs={"pk": pk})


class CheckAppointmentsView(DetailView):
    model = Profile
    template_name = 'account/appointments.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data()
        today = datetime.datetime.now()
        now = datetime.date(int(today.year), int(today.month), int(today.day))
        data['appointments_future'] = Appointment.objects.filter(user__id=self.kwargs["pk"],
                                                                 time_slot__company_day__date__gte=now)
        data['appointments_history'] = Appointment.objects.filter(user__id=self.kwargs["pk"],
                                                                  time_slot__company_day__date__lt=now)
        return data


class ConfirmEmailView(UpdateView):
    model = Profile
    form_class = ConfirmMailForm
    template_name = "account/mail_confirm.html"

    def form_valid(self, form):
        user_id = self.kwargs["pk"]
        user = Profile.objects.get(id=user_id)
        user.confirm = True
        user.save()
        return HttpResponseRedirect(reverse_lazy("snapvisite:home-page"))


def custom_error_403(request, exception):
    return render(request, 'account/403.html')
