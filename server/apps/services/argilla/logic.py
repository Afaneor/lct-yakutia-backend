import argilla as rg


rg.init(api_url='http://0.0.0.0:6900/', api_key='admin.apikey', workspace='admin')


# Create a basic text classification record
textcat_record = rg.TextClassificationRecord(
    text="Hello world, this is me!",
    prediction=[("LABEL1", 0.8), ("LABEL2", 0.2)],
    annotation="LABEL1",
    multi_label=False,
)

# Create a basic token classification record
tokencat_record = rg.TokenClassificationRecord(
    text="Michael is a professor at Harvard",
    tokens=["Michael", "is", "a", "professor", "at", "Harvard"],
    prediction=[("NAME", 0, 7), ("LOC", 26, 33)],
)

# Create a basic text2text record
text2text_record = rg.Text2TextRecord(
    text="My name is Sarah and I love my dog.",
    prediction=["Je m'appelle Sarah et j'aime mon chien."],
)

# Upload (log) the records to corresponding datasets in the Argilla web app
rg.log(textcat_record, "my_textcat_dataset")
rg.log(tokencat_record, "my_tokencat_dataset")
rg.log(tokencat_record, "my_text2text_dataset")