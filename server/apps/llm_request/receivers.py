from django.db.models.signals import post_save
from django.dispatch import receiver

from server.apps.llm_request.models import Message
from server.apps.services.tasks import send_text


@receiver(post_save, sender=Message)
def send_text_in_argilla(sender, instance, **kwargs):
    """Отправляем данные в argilla."""
    if kwargs.get("created"):
        send_text.apply_async(
            kwargs={"text": instance.text},
            countdown=1,
        )
