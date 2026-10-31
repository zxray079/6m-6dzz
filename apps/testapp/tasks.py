from celery import shared_task
from django.contrib.auth import get_user_model
from datetime import timedelta
from django.utils import timezone
import time

User = get_user_model()

@shared_task
def send_welcome_email_task(user_email):
    time.sleep(5)
    print(f"Приветственное письмо отправлено на {user_email}")
    return f"Письмо отправлено на {user_email}"

@shared_task
def clean_inactive_users_task(days=30):
    date_limit = timezone.now() - timedelta(days=days)


    users = User.objects.filter(
        is_active=False,
        date_joined__lt=date_limit
    )

    count = users.count()
    users.delete()

    return f"Удалено неактивных пользователей: {count}"


@shared_task
def send_daily_admin_report_task():
    stats = {
        "ADMIN": User.objects.filter(is_superuser=True).count(),
        "MODERATOR": User.objects.filter(
            is_staff=True,
            is_superuser=False
        ).count(),
        "USER": User.objects.filter(
            is_staff=False,
            is_superuser=False
        ).count(),
    }

    print(f"Статистика пользователей: {stats}")
    return stats