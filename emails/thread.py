class EMailThread:
    @staticmethod
    def from_id(id_, db):
        return EMailThread(
            **db.enron_dataset.find_one({"_id": id_})["head_message"]["header"]
        )

    @staticmethod
    def from_text(text):

        headers, thread = cleaning_pipeline.parse_email_thread(text)
        headers = EMailHeader(**headers)
        thread = EMail.

        # remove corrupted characters
        thread = re.sub(r"(=09|=20|=01|=\n)", r"", thread)

    def __init__(self, head_email=None, messages=list()):
        self.head_email = head_email
        self.messages = messages