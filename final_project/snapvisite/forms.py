import datetime

from django import forms
from django.core.exceptions import NON_FIELD_ERRORS
from django.core.exceptions import ValidationError

from .models import Company, Category, Address, Schedule, Service, CompanyDay, TimeSlot, Appointment


class CreateCompanyFirstStepForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ('company_name', 'category')

    company_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-lg'}))
    category = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )


class EditCategoriesForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ('category',)

    category = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        exclude = ('company',)

    city = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-lg'}))
    postal_code = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-lg'}))
    street_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-lg'}))
    street_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-lg'}))
    apartment_number = forms.CharField(required=False,
                                       widget=forms.TextInput(attrs={'class': 'form-control form-control-lg'}))

    def clean(self):
        cleaned_data = super().clean()
        city = cleaned_data.get("city")
        if not city[0].isupper():
            raise ValidationError({"city": "First letter of city had to be uppercase."})


class UpdateCompanyNameForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ('company_name',)

    company_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-lg'}))


class UpdateCompanyDescriptionForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ('description',)

    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control form-control-lg', 'rows': 5}))


class UpdateCompanyPhotoForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ('photo',)

    widgets = {
        'photo': forms.FileInput(attrs={'class': 'form-control form-control-lg'})
    }


time_widget = forms.TimeInput(attrs={'class': 'timepicker'})


class ScheduleDayForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ('day_of_week', 'open_time', 'close_time')
    day_of_week = (forms.CharField(disabled=True, widget=forms.TextInput(attrs={'class': 'form-control'})))
    open_time = forms.TimeField(required=False, widget=forms.TimeInput(attrs={'class': 'form-control timepicker'}))
    close_time = forms.TimeField(required=False, widget=forms.TimeInput(attrs={'class': 'form-control timepicker'}))

    def clean(self):
        cleaned_data = super().clean()
        open_time = cleaned_data.get("open_time")
        close_time = cleaned_data.get("close_time")
        if open_time and not close_time:
            raise ValidationError({"close_time": "You have to define close time"})
        if close_time and not open_time:
            raise ValidationError({"open_time": "You have to define open time"})

        if isinstance(open_time, datetime.time):
            if open_time > close_time:
                raise ValidationError({"open_time": "Start time have to be lower than end time"})


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        exclude = ('company',)

    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-lg'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control form-control-lg', 'rows': 3}))
    time = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control form-control-lg', 'min': '15',
                                                              'placeholder': "Put time in minutes. Like '60' = 1h,"
                                                                             " '30' = 30min, '90' = 1h 30min"}))
    price = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control form-control-lg',
                                                               'placeholder': 'Use only full numbers like: 10.00, 15,'
                                                                              ' 25.00, 25 ',
                                                               'step': 1}))


class ContactForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ('phone_number', 'email')

    phone_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))


class CompanyDayForm(forms.ModelForm):
    class Meta:
        model = CompanyDay
        exclude = ('company',)
        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': f'You cant duplicate your working days.'
            }
        }

    date = forms.DateField(widget=forms.NumberInput(attrs={'type': 'date'}))


class CompanyDayMultipleForm(forms.Form):
    help_text_n_days = "If u never create workday before these will be created from today date." \
                       " Otherwise from last created date"

    number_of_days = forms.IntegerField(label="How many days into the future you want to create.",
                                        help_text=help_text_n_days,
                                        widget=forms.NumberInput(attrs={
                                            'class': 'form-control',
                                            'placeholder': 'Enter in example: 30 to make workdays for month.'
                                        }))


class CompanyTimeSlotForm(forms.ModelForm):
    class Meta:
        model = TimeSlot
        fields = ('start_time',)

    start_time = forms.TimeField(widget=forms.TimeInput(attrs={'class': 'form-control timepicker'}))


class CompanyTimeSlotMultipleForm(forms.Form):
    from_time = forms.TimeField(required=True, label="Start Time", widget=forms.TimeInput(attrs={'class': 'form-control timepicker'}))
    to_time = forms.TimeField(required=True, label="End Time", widget=forms.TimeInput(attrs={'class': 'form-control timepicker'}))
    delta = forms.IntegerField(required=True, label="Time step(in minutes)",
                               widget=forms.NumberInput(attrs={
                                   'class': 'form-control form-control-lg',
                                   'placeholder': 'Enter minutes. What step to create a new slot.'
                               }))

    def clean(self):
        cleaned_data = super().clean()
        from_time = cleaned_data.get("from_time")
        to_time = cleaned_data.get("to_time")

        if from_time > to_time:
            raise ValidationError({"to_time": "Start time have to be lower than end time"})


class CreateAppointmentForm(forms.ModelForm):
    CHOICES = [(True, 'Pay with card now.'), (False, 'Pay by cash on visit.')]

    class Meta:
        model = Appointment
        fields = ('note', 'payment_status')

    note = forms.CharField(label='Additional information', widget=forms.Textarea(
        attrs={'class': 'form-control form-control-lg', 'rows': 3}))
    payment_status = forms.ChoiceField(label='Payment option',
                                       widget=forms.RadioSelect(attrs={'class': 'form-check'}), choices=CHOICES)


class SendMailForm(forms.Form):
    subject = forms.CharField(required=True, label="Subject", widget=forms.TextInput(attrs={'class': 'form-control'}))
    message = forms.CharField(required=True, label="Message", widget=forms.Textarea(attrs={'class': 'form-control'}))

