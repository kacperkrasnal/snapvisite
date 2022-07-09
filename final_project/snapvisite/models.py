import uuid
from django.dispatch import receiver
from django.db.models.signals import post_save
from account.models import Profile
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Category(models.Model):
    category_name = models.CharField(max_length=40)
    photo = models.ImageField(blank=True, null=True, upload_to='category_image')

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return f'{self.category_name}'


def save_photo(instance, filename):
    filename = f'{uuid.uuid1()}_{filename}'
    return f'company_photos/{instance.company_name}_{instance.id}/{filename}'


class Company(models.Model):
    company_name = models.CharField(max_length=35)
    photo = models.ImageField(blank=True, null=True, upload_to=save_photo)
    description = models.TextField(blank=True, null=True, max_length=310)
    created_date = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(Profile, on_delete=models.PROTECT)
    category = models.ManyToManyField(Category)
    phone_number = PhoneNumberField(blank=True, null=True)
    email = models.EmailField(verbose_name='email', max_length=80, unique=True, blank=True, null=True)

    class Meta:
        verbose_name = 'company'
        verbose_name_plural = 'companies'

    def __str__(self):
        return f'{self.company_name}'


class Address(models.Model):
    city = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=8)
    street_name = models.CharField(max_length=50)
    street_number = models.CharField(max_length=50)
    apartment_number = models.CharField(max_length=5, blank=True, null=True)
    company = models.OneToOneField(Company, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name = 'address'
        verbose_name_plural = 'addresses'

    def __str__(self):
        return f'({self.city} {self.street_name} {self.street_number})'


class CompanyDay(models.Model):
    date = models.DateField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('company', 'date')
        verbose_name = 'companyday'
        verbose_name_plural = 'companydays'
        ordering = ('date',)

    def __str__(self):
        return f'({self.date})'


class Schedule(models.Model):
    DAYS = (('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'),
            ('Friday', 'Friday'), ('Saturday', 'Saturday'), ('Sunday', 'Sunday'))
    day_of_week = models.CharField(max_length=50, choices=DAYS, null=True, blank=True)
    open_time = models.TimeField(null=True, blank=True, default=None)
    close_time = models.TimeField(null=True, blank=True, default=None)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'schedule'
        verbose_name_plural = 'schedules'

    def __str__(self):
        return f'{self.company} {self.day_of_week}'


@receiver(post_save, sender=Company)
def company_created_add_schedule(sender, instance, created, *args, **kwargs):
    if created:
        for schedule_day in range(len(Schedule.DAYS)):
            Schedule.objects.create(day_of_week=Schedule.DAYS[schedule_day][0], company=instance)


class Service(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()
    time = models.IntegerField(default=30,
                               help_text="Put time in minutes. Like '60' = 1h, '30' = 30min, '90' = 1h 30min")
    price = models.DecimalField(max_digits=6, decimal_places=2)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'service'
        verbose_name_plural = 'services'

    def __str__(self):
        return f'{self.name} {self.company.company_name}'


class TimeSlot(models.Model):
    start_time = models.TimeField()
    status = models.BooleanField(default=True)
    company_day = models.ForeignKey(CompanyDay, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'timeslot'
        verbose_name_plural = 'timeslots'
        ordering = ('start_time',)

    def __str__(self):
        return f'({self.company_day.company.company_name};\
         {self.company_day.date}[Available: {self.status} Id: {self.pk}]; ({self.start_time}))'


class Appointment(models.Model):
    note = models.CharField(max_length=128, null=True, blank=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    time_slot = models.OneToOneField(TimeSlot, on_delete=models.CASCADE)
    payment_status = models.BooleanField(default=False,
                                         choices=[(True, 'Pay with card now'), (False, 'Pay by cash on visit')])
    appointment_code = models.CharField(max_length=50, default="123")

    class Meta:
        verbose_name = 'appointment'
        verbose_name_plural = 'appointments'

    def __str__(self):
        return f'(Id: {self.pk} {self.user.email}-{self.service.name}' \
               f' [{self.time_slot.start_time}])'

    def create_appointment_code(self):
        return f'{self.user.pk}{self.service.company.company_name[:3]}{uuid.uuid1()}'
