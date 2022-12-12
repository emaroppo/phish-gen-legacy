from pymongo import MongoClient
from tqdm import tqdm
import os


def create_txt(email, to_file=False, txt_path=None):
    if "tags" in email:
        tags = list(set(email["tags"]))
        tags.sort()
    else:
        tags = []

    body = email["body"]
    prompt_model = (
        f"""[TAGS_START]{",".join(tags)}[TAGS_END][BODY_START]{body}[BODY_END]"""
    )

    if to_file:
        with open(txt_path, "w") as f:
            f.write(prompt_model)
    return prompt_model


client = MongoClient("localhost", 27017)
db = client.email


def create_dataset(db, target_dir):
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    cursor = db.enron_dataset.find()
    for i, j in tqdm(enumerate(cursor)):
        create_txt(j["head_message"], to_file=True, txt_path=f"{target_dir}/{i}.txt")
        for k, l in enumerate(j["messages"]):
            create_txt(l, to_file=True, txt_path=f"{target_dir}/{i}_{k}.txt")


create_dataset(db, "email_bodies")

client.close()
