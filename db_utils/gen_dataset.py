import os
from copy import deepcopy

from pymongo import MongoClient
from tqdm import tqdm


def create_txt(email, to_file=False, txt_path=None, simplified_prompt=True):
    if "tags" in email:
        tags = list(set(email["tags"]))
        tags.sort()
    else:
        tags = []

    body = email["body"]

    if simplified_prompt:
        prompt_model = body

        if "tags" in email:
            for i in email["tags"]:
                prompt_model = i + prompt_model
    else:
        prompt_model = (
            f"""[TAGS_START]{",".join(tags)}[TAGS_END][BODY_START]{body}[BODY_END]"""
        )

    if to_file and body.strip() != "":
        with open(txt_path, "w") as f:
            f.write(prompt_model)
    return prompt_model


def create_dataset(
    db,
    target_dir,
    scope="head_message",
    min_len=3,
    max_len=400,
    exclude_html=True,
    balance_dataset=False,
):
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    filter = []
    if exclude_html:
        filter.append({"head_message.is_html": {"$exists": False}})

    if min_len:
        filter.append({"head_message.word_count": {"$gte": min_len}})

    if max_len:
        filter.append({"head_message.word_count": {"$lte": max_len}})

    if len(filter) == 1:
        filter = filter[0]

    if len(filter) > 1:
        filter = {"$and": filter}

    if len(filter) > 0:
        cursor = db.enron_dataset.find(filter)
    else:
        cursor = db.enron_dataset.find()

    if balance_dataset:
        tagged_documents_count = db.enron_dataset.count_documents(
            {"head_message.tags": {"$exists": True}}
        )
        tagged_documents_filter = deepcopy(filter)
        tagged_documents_filter["$and"] += [{"head_message.tags": {"$exists": True}}]

        tagged_documents_cursor = db.enron_dataset.find(tagged_documents_filter)
        for i, j in tqdm(enumerate(tagged_documents_cursor)):
            create_txt(
                j["head_message"],
                to_file=True,
                txt_path=f"{target_dir}/{i}_tagged.txt",
            )
        untagged_documents_filter = deepcopy(filter)
        untagged_documents_filter["$and"] += [{"head_message.tags": {"$exists": False}}]
        untagged_documents_cursor = db.enron_dataset.find(
            untagged_documents_filter
        ).limit(tagged_documents_count)

        for i, j in tqdm(enumerate(untagged_documents_cursor)):
            create_txt(
                j["head_message"],
                to_file=True,
                txt_path=f"{target_dir}/{i}_untagged.txt",
            )

    else:

        cursor = db.enron_dataset.find()

        for i, j in tqdm(enumerate(cursor)):
            create_txt(
                j["head_message"], to_file=True, txt_path=f"{target_dir}/{i}.txt"
            )

            if scope == "messages" or scope == "all":
                for k, l in enumerate(j["messages"]):
                    create_txt(l, to_file=True, txt_path=f"{target_dir}/{i}_{k}.txt")
