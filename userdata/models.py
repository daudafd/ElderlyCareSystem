from django.db import models
from django.contrib.auth.models import User
from datetime import date

class Client(models.Model):
    # Personal Information
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    marital_status = models.CharField(max_length=20, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)  # New field for storing age persistently
    phone = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    weight = models.CharField(max_length=4, null=True, blank=True)
    height = models.CharField(max_length=3, null=True, blank=True)

    def calculate_age(self):
        if self.dob:
            today = date.today()
            return today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))
        return None

    def save(self, *args, **kwargs):
        self.age = self.calculate_age()
        super(Client, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Vital(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    temperature = models.FloatField(null=True, blank=True)
    blood_pressure = models.CharField(max_length=10, null=True, blank=True)
    genotype = models.CharField(max_length=10, null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['client', 'date'], name='unique_client_date')
        ]

    def __str__(self):
        return f'Vitals for {self.client} on {self.date}'
