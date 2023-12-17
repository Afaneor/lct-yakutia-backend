import os

import argilla as rg
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')


rg.init(
    api_url=settings.ARGILLA_API_URL,
    api_key=settings.ARGILLA_API_KEY,
    workspace=settings.ARGILLA_WORKSPACE,
)


@app.task(bind=True)  # type: ignore
def send_text(
    self,
    text: str,
) -> None:
    """Отправление данные в argilla."""
    # Create a basic text classification record.
    textcat_record = rg.TextClassificationRecord(
        text=text,
        prediction=[("LABEL1", 0.8), ("LABEL2", 0.2)],
        annotation="LABEL1",
        multi_label=False,
    )

    # Create a basic token classification record.
    tokencat_record = rg.TokenClassificationRecord(
        text=text,
        tokens=['test', 'data'],
        prediction=[("TEST", 0, 3), ("LOC", 4, 7)],
    )

    # Create a basic text2text record.
    text2text_record = rg.Text2TextRecord(
        text=text,
        prediction=['test'],
    )

    # Upload (log) the records to corresponding datasets in the Argilla web app
    rg.log(textcat_record, "my_textcat_dataset")
    rg.log(tokencat_record, "my_tokencat_dataset")
    rg.log(tokencat_record, "my_text2text_dataset")
