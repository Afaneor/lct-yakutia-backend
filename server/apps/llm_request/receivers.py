from django.db.models.signals import post_save
from django.dispatch import receiver

from server.apps.llm_request.models import Message


@receiver(post_save, sender=Message)
def send_data_argilla(sender, instance, **kwargs):
    """Отправляем данные в argilla."""
    if kwargs.get("created"):
        create_default_workflow_for_company.apply_async(
            kwargs={"company_id": instance.id},
            countdown=1,
        )
