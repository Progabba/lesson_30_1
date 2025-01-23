from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

from django.utils.timezone import now
from datetime import timedelta
from django.contrib.auth import get_user_model

User = get_user_model()


@shared_task
def send_course_update_email(course_id, email_list):
    from .models import (
        Course,
    )  # Импортируем внутри задачи, чтобы избежать циклического импорта

    course = Course.objects.get(id=course_id)
    subject = f"Обновление материалов курса: {course.name}"
    message = f"Уважаемый пользователь,\n\nКурс '{course.name}' был обновлен. Пожалуйста, ознакомьтесь с новыми материалами."

    for email in email_list:
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])


@shared_task
def block_inactive_users():
    one_month_ago = now() - timedelta(days=30)
    inactive_users = User.objects.filter(last_login__lt=one_month_ago, is_active=True)

    for user in inactive_users:
        user.is_active = False
        user.save()
