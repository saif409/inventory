from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver


# Create your models here.
ROLE_CHOICES = (
    (1, 'Admin'),
    (2, 'Supervisor'),
    (3, 'User'),
)

REVIEW_CHOICES = (
    (1, 'OneStar'),
    (2, 'TwoStar'),
    (3, 'ThreeStar'),
    (4, 'FourStar'),
    (5, 'FiveStar'),
)

STATUS_CHOICES = (
    (1, 'Active'),
    (2, 'InActive'),
    (3, 'Rejected'),
)


class Surveyor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,  related_name='user_info')
    address = models.CharField(max_length=200)
    profile_picture = models.ImageField()
    country = models.CharField(max_length=100)
    division = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    sub_district = models.CharField(max_length=100)
    email = models.CharField(max_length=100,null=True, blank=True)
    graduation_subject = models.CharField(max_length=200)
    university = models.CharField(max_length=200)
    skills = models.CharField(max_length=200)
    area = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    description = models.TextField()
    designation = models.CharField(max_length=100)
    experience = models.CharField(max_length=200)
    role = models.IntegerField(choices=ROLE_CHOICES, null=True, default=3)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    status = models.IntegerField(choices=STATUS_CHOICES, null=True, default=2)

    def __str__(self):
        return str(self.user)


class Stock(models.Model):
    product_name = models.CharField(max_length = 200)
    quantity = models.IntegerField()
    unit_price = models.IntegerField()
    created_date = models.DateField(auto_now_add=True)
    user = models.CharField(max_length=200)
    is_delete = models.BooleanField(default=False)

    def __str__(self):
        return self.product_name

    @property
    def total_price(self):
        return self.quantity * self.unit_price


class Sell(models.Model):
    product_name = models.CharField(max_length=200)
    buy_price = models.IntegerField()
    quantity = models.IntegerField()
    sell_price = models.IntegerField()
    note = models.TextField(null=True, blank=True)
    created_date = models.DateField(auto_now_add=True)
    user = models.CharField(max_length=200)
    is_delete = models.BooleanField(default=False)

    def __str__(self):
        return self.product_name

    @property
    def total_sell_price(self):
        return self.quantity * self.sell_price

    @property
    def total_buy_price(self):
        return self.quantity * self.buy_price

    @property
    def profit(self):
        return self.total_sell_price - self.total_buy_price

