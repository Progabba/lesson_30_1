from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from lms.models import Course, Lesson

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


class Payment(models.Model):
    CASH = 'cash'
    TRANSFER = 'transfer'

    PAYMENT_METHOD_CHOICES = [
        (CASH, 'Наличные'),
        (TRANSFER, 'Перевод на счет'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='payments')
    payment_date = models.DateTimeField(auto_now_add=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True, related_name='payments')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, null=True, blank=True, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES)
    session_id = models.CharField(max_length=50, blank=True, null=True)
    link = models.URLField(max_length=400, blank=True, null=True)

    def __str__(self):
        return f"{self.user.email} - {self.amount} ({self.payment_method})"