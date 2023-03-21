import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models
from dateutil.relativedelta import relativedelta


class User(AbstractUser):
    image = models.ImageField(upload_to="users_images", null=True, blank=True)


class Magazine(models.Model):
    DAILY = 'daily'
    WEEKLY = 'weekly'
    MONTHLY = 'monthly'
    QUARTERLY = 'quarterly'
    BIANNUAL = 'biannual'
    ANNUAL = 'annual'

    FREQUENCY_CHOICES = [(DAILY, 'Daily'),
                         (WEEKLY, 'Weekly'),
                         (MONTHLY, 'Monthly'),
                         (QUARTERLY, 'Quarterly'),
                         (BIANNUAL, 'Biannual'),
                         (ANNUAL, 'Annual'),
                         ]
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    frequency = models.CharField(max_length=50, choices=FREQUENCY_CHOICES)

    def __str__(self):
        return self.name


FREQUENCY_DELTA_MAP = {
    Magazine.DAILY: relativedelta(days=1),
    Magazine.WEEKLY: relativedelta(weeks=1),
    Magazine.MONTHLY: relativedelta(months=1),
    Magazine.QUARTERLY: relativedelta(months=3),
    Magazine.BIANNUAL: relativedelta(months=6),
    Magazine.ANNUAL: relativedelta(years=1),
}


class Subscription(models.Model):
    subscriber = models.ForeignKey(User, on_delete=models.CASCADE)
    magazine = models.ForeignKey(Magazine, on_delete=models.CASCADE)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)

    @staticmethod
    def create_subscription(magazine, time_amount, user):
        start_date = datetime.date.today()
        frequency_delta = FREQUENCY_DELTA_MAP.get(magazine.frequency)
        end_date = start_date + frequency_delta * time_amount
        subscription = Subscription(subscriber=user, magazine=magazine, start_date=start_date, end_date=end_date)
        return subscription

    def increase_end_date(self,time_amount):
        frequency_delta = FREQUENCY_DELTA_MAP.get(self.magazine.frequency)
        self.end_date += frequency_delta * time_amount

    def __str__(self):
        return f"{self.subscriber.username} subscribed to {self.magazine.name}"


class Payment(models.Model):
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def create_payment(subscription, time_amount):
        price = subscription.magazine.price
        amount = price * time_amount
        payment = Payment(subscription=subscription, amount=amount)
        return payment

    def __str__(self):
        return f"{self.subscription.subscriber.username} paid {self.amount} for subscription to {self.subscription.magazine.name} "
