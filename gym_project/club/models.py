from django.db import models
from datetime import date, timedelta

class Client(models.Model):
    full_name = models.CharField(max_length=200, verbose_name="ФИО")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    email = models.EmailField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата регистрации")

    def __str__(self):
        return self.full_name

class Service(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название услуги")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    duration_days = models.IntegerField(default=30, verbose_name="Длительность (дней)")

    def __str__(self):
        return self.name

class Subscription(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    start_date = models.DateField()
    is_active = models.BooleanField(default=True)

    def is_expired(self):
        month_ago = date.today() - timedelta(days=30)
        return date.today() > month_ago

    def str(self):
        return f"{self.client} - {self.service}"
