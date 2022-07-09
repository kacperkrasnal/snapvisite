import datetime

import extra_views
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, TemplateView, UpdateView, View, DeleteView, FormView
from django.core.exceptions import PermissionDenied

from .forms import *
from .mixins import OwnerAccessMixin, UserConfirmMixin
from .models import *


class MainPageView(TemplateView):
    template_name = "snapvisite/main_page.html"


class CreateCompanyFirstStepView(LoginRequiredMixin, UserConfirmMixin, CreateView):
    """
    First step to create a company.
    Current logged user can name and select categories for his company.
    """
    model = Company
    form_class = CreateCompanyFirstStepForm
    template_name = 'snapvisite/create_company_first_step.html'

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

    def form_valid(self, form):
        """
        In creator company owner always be current logged user.
        """
        obj = form.save(commit=False)
        obj.owner = self.request.user
        obj.save()
        """!!!THIS STILL NEEDS TO BE HERE???"""
        obj = form.save_m2m()
        return HttpResponseRedirect(reverse_lazy('snapvisite:company_panel'))


class CompanyPanelView(LoginRequiredMixin, ListView):
    model = Company
    template_name = "snapvisite/company_panel.html"

    def get_queryset(self):
        user = self.request.user
        return Company.objects.filter(owner=user)


class YourCompanyView(OwnerAccessMixin, DetailView):
    model = Company
    template_name = "snapvisite/your_company.html"


class EditCompanyNameView(OwnerAccessMixin, SuccessMessageMixin, UpdateView):
    """ EDITOR """
    model = Company
    form_class = UpdateCompanyNameForm
    template_name = "snapvisite/company_editor.html"
    success_message = 'Company name changed successfully'

    def get_success_url(self):
        pk = self.kwargs["pk"]
        return reverse("snapvisite:your_company", kwargs={"pk": pk})


class EditCompanyPhotoView(OwnerAccessMixin, SuccessMessageMixin, UpdateView):
    """ EDITOR """
    model = Company
    form_class = UpdateCompanyPhotoForm
    template_name = "snapvisite/company_editor.html"
    success_message = 'Company picture added successfully'

    def get_success_url(self):
        pk = self.kwargs["pk"]
        return reverse("snapvisite:your_company", kwargs={"pk": pk})


class EditCompanyDescriptionView(OwnerAccessMixin, SuccessMessageMixin, UpdateView):
    """ EDITOR """
    model = Company
    form_class = UpdateCompanyDescriptionForm
    template_name = "snapvisite/company_editor.html"
    success_message = 'Company description added successfully.'

    def get_success_url(self):
        pk = self.kwargs["pk"]
        return reverse("snapvisite:your_company", kwargs={"pk": pk})


class EditCompanyCategoriesView(OwnerAccessMixin, UpdateView):
    """ EDITOR """
    model = Company
    form_class = EditCategoriesForm
    template_name = "snapvisite/company_editor.html"
    success_message = 'Company categories updated successfully.'

    def form_valid(self, form, *args, **kwargs):
        form.save(commit=False)
        form.save()
        form.save_m2m()
        id_company = self.kwargs["pk"]
        return HttpResponseRedirect(reverse('snapvisite:your_company', kwargs={"pk": id_company}))


class CreateAddressView(UserPassesTestMixin, SuccessMessageMixin, CreateView):
    pk_url_kwarg = 'company_id'
    """ EDITOR """
    model = Address
    form_class = AddressForm
    template_name = 'snapvisite/address.html'
    success_message = 'Company address added successfully.'

    def form_valid(self, form, *args, **kwargs):
        form.instance.company_id = self.kwargs['company_id']
        obj = form.save(commit=False)
        obj.save()
        return HttpResponseRedirect(reverse('snapvisite:your_company', kwargs={"pk": form.instance.company_id}))

    def test_func(self):
        obj = self.get_object(Company.objects.all())
        return obj.owner == self.request.user


class UpdateAddressView(UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    """ EDITOR """
    model = Address
    form_class = AddressForm
    template_name = 'snapvisite/address.html'
    success_message = 'Company address updated successfully.'

    def get_success_url(self):
        company_id = self.kwargs['company_id']
        return reverse('snapvisite:your_company', kwargs={"pk": company_id})

    def test_func(self):
        obj = self.get_object()
        return obj.company.owner == self.request.user


class ScheduleListView(ListView):
    model = Schedule

    def get_queryset(self):
        return Schedule.objects.filter(company=self.kwargs['company_id'])


class ScheduleUpdateView(UpdateView):
    model = Schedule
    form_class = ScheduleDayForm
    template_name = "snapvisite/company_editor.html"

    def get_success_url(self):
        company_id = self.kwargs['company_id']
        return reverse('snapvisite:schedule_company', kwargs={"company_id": company_id})


class CreateServiceView(UserPassesTestMixin, CreateView):
    """ EDITOR """
    pk_url_kwarg = 'company_id'
    form_class = ServiceForm
    template_name = 'snapvisite/company_editor.html'

    def test_func(self):
        obj = self.get_object(Company.objects.all())
        return obj.owner == self.request.user

    def form_valid(self, form, *args, **kwargs):
        form.instance.company_id = self.kwargs['company_id']
        obj = form.save(commit=False)
        obj.save()
        return HttpResponseRedirect(reverse('snapvisite:your_company', kwargs={"pk": form.instance.company_id}))


class UpdateServiceView(UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    """ EDITOR """
    model = Service
    form_class = ServiceForm
    template_name = 'snapvisite/company_editor.html'
    success_message = 'Company service updated successfully.'

    def get_success_url(self):
        company_id = self.kwargs['company_id']
        return reverse('snapvisite:your_company', kwargs={"pk": company_id})

    def test_func(self):
        obj = self.get_object()
        return obj.company.owner == self.request.user


class DeleteServiceView(SuccessMessageMixin, DeleteView):
    model = Service
    success_message = 'Company service deleted successfully.'

    def get_success_url(self):
        return reverse('snapvisite:your_company', kwargs={"pk": self.kwargs['company_id']})


class UpdateContactView(UpdateView):
    """ EDITOR """
    model = Company
    form_class = ContactForm
    template_name = "snapvisite/company_editor.html"

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse('snapvisite:your_company', kwargs={"pk": pk})


class CompanyListSearchView(View):

    def post(self, *args):
        """
        Select box with categories with value category_id
        button CATEGORIES have value == 0, and it means search in all categories.
        """
        all_categories_id = 0
        if 'category' in self.request.POST:
            category_id = int(self.request.POST['category'])
        else:
            category_id = all_categories_id

        if category_id != all_categories_id:
            if self.request.POST['city']:
                searched_city = self.request.POST['city']
                company_list = Company.objects.filter(
                    category__id=category_id, address__city__icontains=searched_city)
            else:
                company_list = Company.objects.filter(category__id=category_id)
            return render(self.request, 'snapvisite/company_list.html', {'company_list': company_list})
        else:
            if self.request.POST['city']:
                searched_city = self.request.POST['city']
                company_list = Company.objects.filter(
                    address__city__icontains=searched_city)
            else:
                company_list = Company.objects.all()
            return render(self.request, 'snapvisite/company_list.html', {'company_list': company_list})


class CompanyUserView(UserConfirmMixin, DetailView):
    model = Company
    template_name = "snapvisite/company_user_detail.html"

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

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        today = datetime.datetime.now()
        now = datetime.date(int(today.year), int(today.month), int(today.day))
        data["days_list"] = CompanyDay.objects.filter(
            company__id=self.kwargs["pk"], date__gte=now)
        return data


class CreateCompanyDay(UserPassesTestMixin, CreateView):
    pk_url_kwarg = 'company_id'
    model = CompanyDay
    form_class = CompanyDayForm
    template_name = 'snapvisite/company_editor.html'

    def test_func(self):
        obj = self.get_object(Company.objects.all())
        return obj.owner == self.request.user

    def form_valid(self, form, *args, **kwargs):
        form.instance.company_id = self.kwargs['company_id']
        obj = form.save(commit=False)
        obj.save()
        return HttpResponseRedirect(reverse('snapvisite:company_terminal', kwargs={"pk": form.instance.company_id}))


class CreateMultipleCompanyDayView(FormView):
    pk_url_kwarg = 'company_id'
    form_class = CompanyDayMultipleForm
    template_name = 'snapvisite/company_editor.html'

    def form_valid(self, form):
        company = Company.objects.get(id=self.kwargs['company_id'])
        now = datetime.datetime.today().date()
        number_of_days = form.cleaned_data.get('number_of_days')
        if company.companyday_set.exists():
            last_created_date = CompanyDay.objects.filter(company=company).order_by('-date').first().date
            last_created_date += datetime.timedelta(days=1)
            for _ in range(number_of_days):
                instance = CompanyDay(
                    date=last_created_date,
                    company=company
                )
                instance.save()
                last_created_date += datetime.timedelta(days=1)
        else:
            for _ in range(number_of_days):
                instance = CompanyDay(
                    date=now,
                    company=company
                )
                instance.save()
                now += datetime.timedelta(days=1)

        return HttpResponseRedirect(reverse('snapvisite:company_terminal', kwargs={"pk": self.kwargs['company_id']}))


class DeleteCompanyDayView(DeleteView):
    model = CompanyDay

    def get_success_url(self):
        return reverse('snapvisite:company_terminal', kwargs={"pk": self.kwargs['company_id']})


class CompanyTerminalView(OwnerAccessMixin, DetailView):
    model = Company
    template_name = "snapvisite/terminal.html"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        today = datetime.datetime.now()
        now = datetime.date(int(today.year), int(today.month), int(today.day))
        page = self.request.GET.get('page')
        data['days'] = Paginator(CompanyDay.objects.filter(company__id=self.kwargs["pk"], date__gte=now), 7).get_page(
            page)
        return data


class CreateSingleTimeSlotView(CreateView):
    model = TimeSlot
    template_name = 'snapvisite/company_editor.html'
    form_class = CompanyTimeSlotForm

    def form_valid(self, form):
        company_id = CompanyDay.objects.get(
            id=self.kwargs['day_id']).company_id
        form.instance.company_day_id = self.kwargs['day_id']
        obj = form.save(commit=False)
        obj.save()
        return HttpResponseRedirect(reverse('snapvisite:company_terminal', kwargs={'pk': company_id}))


class CreateMultipleTimeSlotView(FormView):
    form_class = CompanyTimeSlotMultipleForm
    template_name = 'snapvisite/company_editor.html'

    def form_valid(self, form):
        company_id = CompanyDay.objects.get(
            id=self.kwargs['day_id']).company_id
        from_time = form.cleaned_data.get('from_time')
        to_time = form.cleaned_data.get('to_time')
        delta = datetime.timedelta(minutes=form.cleaned_data.get('delta'))
        while from_time <= to_time:
            instance = TimeSlot(
                start_time=from_time,
                company_day=CompanyDay.objects.get(id=self.kwargs['day_id'])
            )
            instance.save()
            from_time = (datetime.datetime.combine(
                datetime.date(1, 1, 1), from_time) + delta).time()
        return HttpResponseRedirect(reverse('snapvisite:company_terminal', kwargs={'pk': company_id}))


class DeleteTimeSlotView(DeleteView):
    model = TimeSlot

    def get_success_url(self):
        return reverse('snapvisite:company_terminal', kwargs={"pk": self.kwargs['company_id']})


class UserTerminal(UserConfirmMixin, DetailView):
    model = Company
    template_name = 'snapvisite/terminal_user.html'

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

    def get_context_data(self, **kwargs):
        data = super().get_context_data()
        today = datetime.datetime.now()
        now = datetime.date(int(today.year), int(today.month), int(today.day))
        page = self.request.GET.get('page')
        data['today'] = now
        data['time_now'] = today
        data['days'] = Paginator(CompanyDay.objects.filter(company__id=self.kwargs["pk"], date__gte=now), 7).get_page(
            page)

        data["service_id"] = self.kwargs["service_id"]
        return data


class CreateAppointmentView(CreateView):
    today = datetime.datetime.now().date().strftime("%d-%m-%Y")
    model = Appointment
    form_class = CreateAppointmentForm
    template_name = "snapvisite/appointment.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.service_id = self.kwargs["service_id"]
        form.instance.time_slot_id = self.kwargs["timeslot_id"]
        obj = form.save(commit=False)
        form.instance.appointment_code = Appointment.create_appointment_code(
            obj)
        obj.save()
        user_timeslot = TimeSlot.objects.get(id=self.kwargs["timeslot_id"])
        user_timeslot.status = False
        user_timeslot.save()
        # sending mail about reservation on user email address.
        user_appointment = Appointment.objects.get(time_slot=user_timeslot)
        subject = f"Your new reservation from {self.today}"
        message = f"\
        Hello {self.request.user.first_name}!\n\
        You received that mail from reason of new reservation in our service.\n\
        You snap visit:\n\
        On {user_timeslot.company_day.date} at {user_timeslot.start_time}.\n\
        For {user_appointment.service.name} in {user_timeslot.company_day.company.company_name}.\n\
        With additional information for employees:\n\
        {user_appointment.note}\n\
        Please arrive on time.\n\
        Thank you for using our service!"
        from_email = settings.EMAIL_HOST_USER
        to_email = [self.request.user.email, ]
        #send_mail(subject, message, from_email, to_email)
        return HttpResponseRedirect(reverse_lazy('snapvisite:home-page'))


class SendMailToCompany(FormView):
    form_class = SendMailForm
    template_name = 'snapvisite/send_mail.html'

    def form_valid(self, form):
        subject = f'{self.request.user.email}: {form.cleaned_data["subject"]}'
        message = f'\
        {datetime.datetime.now()}\n\
        {form.cleaned_data["message"]}\n\
        From User: {self.request.user.email}\n\
        If u want to give feedback send email to email adress above.'
        from_email = self.request.user.email
        to_email = [Company.objects.get(id=self.kwargs["company_id"]).email, ]
        #send_mail(subject, message, from_email, to_email)
        return HttpResponseRedirect(reverse_lazy("snapvisite:home-page"))
