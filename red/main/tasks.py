from uuid import uuid4

from datetime import timedelta

from celery import shared_task

from django.contrib.auth import get_user_model
from django.utils.timezone import now
from .models import EmailVerification


@shared_task()
def send_email_verification(user_id):
    record = EmailVerification.objects.create(code=uuid4(), user=get_user_model().objects.get(id=user_id),
                                              expiration=now() + timedelta(days=1))
    record.send_verification_email()
