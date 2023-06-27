from emails.header import EMailHeader
from pipeline.pipeline import parse_email_thread


class EMail:
    @staticmethod
    def from_id(id_, db):
        return EMail(**db.enron_dataset.find_one({"_id": id_})["head_message"])

    @staticmethod
    def from_txt(txt_file):

        headers, body = parse_email_thread(txt_file)
        # drop empty headers
        headers = {k: v for k, v in headers.items() if v}
        headers = EMailHeader(**headers)

        return EMail(headers=headers, body=body, path=txt_file)

    def __init__(
        self,
        **kwargs,
    ):
        self.headers = kwargs["headers"]
        self.body = kwargs["body"]

    def __repr__(self):
        return f"Headers: {self.headers}\nBody: {self.body}"

    def save(self, db):
        entry = self.__dict__
        entry["headers"] = entry["headers"].__dict__
        email_id = db.enron_dataset.insert_one(self.__dict__).inserted_id
        return email_id

    def update(self, db):
        db.enron_dataset.update_one(
            {"_id": self._id},
            {"$set": self.__dict__},
        )
        return True
