import json
import os
import shutil
import re

from pymongo import MongoClient
from tqdm import tqdm

from clean_utils.clean import (
    remove_corrupted_characters,
    remove_gt,
    remove_img_token,
    retrieve_subject,
)
from clean_utils.export import bodies_to_txts, txt_to_json
from clean_utils.regex_dict import garbage_dict
from clean_utils.sample import generate_path
from db_utils.connect import extract_attachments_obj, extract_urls_obj
from db_utils.gen_dataset import create_dataset
from db_utils.tagging import (
    add_word_count,
    tag_html_documents,
    tags_from_attachments,
    tags_from_urls,
)


def load_thread(path):

    with open(path, "r", encoding="utf8", errors="ignore") as file:
        thread = file.read()
        thread_header, thread = thread.split("X-FileName:")
        thread = "\n".join(thread.split("\n")[2:])

    thread = remove_corrupted_characters(thread)

    return thread, thread_header


def clean_thread(in_paths, dst_folder, start=0):

    if not os.path.exists(dst_folder):
        os.makedirs(dst_folder)

    print(f"Loading {len(in_paths)} emails...")
    if start > 0:
        in_paths = in_paths[start:]

    for i, j in enumerate(tqdm(in_paths)):
        try:
            thread, thread_header = load_thread(j)
            out_filename = (
                f"{i+start}-{j.split('/')[-3]}_{j.split('/')[-2]}_{j.split('/')[-1]}"
            )
        except UnicodeDecodeError:
            pass
        except IsADirectoryError:
            pass
        try:
            txt_to_json(
                thread=thread,
                thread_header=thread_header,
                to_file=True,
                json_path=f"{dst_folder}/{out_filename}.json",
            )
        except:
            print(f"Error in {j}")

    print(f"Successfully cleaned {len(os.listdir(dst_folder))} emails")


def merge_json_files(json_folder_path, json_file_name):
    json_list = []
    print("Merging jsons...")
    for json_file in tqdm(os.listdir(json_folder_path)):
        if json_file.endswith(".json"):
            with open(f"{json_folder_path}/{json_file}", "r") as f:
                json_list.append(json.load(f))
    with open(f"{json_file_name}", "w") as f:
        json.dump(json_list, f)


def bodies_only_dataset(in_folder="json_out", out_folder="txt_out"):
    if not os.path.exists(out_folder):
        os.makedirs(out_folder)

    for i in tqdm(os.listdir(in_folder)):
        if i[0] == ".":
            continue
        with open(f"{in_folder}/{i}", "r") as f:
            data = json.load(f)
            bodies_to_txts(data, to_file=True, txt_path=f"{out_folder}/{i[:-5]}")

    print(f"Successfully extracted {len(os.listdir(out_folder))} email_bodies")


def move_unclean_data(folder_path="txt_out", dst_folder="header_miss"):
    if not os.path.exists(dst_folder):
        os.makedirs(dst_folder)

    for i in tqdm(os.listdir(folder_path)):

        with open(f"{folder_path}/{i}", "r") as file:
            thread = file.read()

            if "To:" in thread:
                shutil.move(f"{folder_path}/{i}", f"{dst_folder}/{i}")

    print(f"Removed {len(os.listdir('header_miss'))} unclean emails from dataset")


def db_cleaning_pipeline(db):
    print("Cleaning bodies...")
    for i in tqdm(db.enron_dataset.find()):

        new_body = remove_img_token(remove_gt(i["head_message"]["body"])).strip()

        new_body, subj = retrieve_subject(new_body)

        if subj:
            db.enron_dataset.update_one(
                {"_id": i["_id"]},
                {"$set": {"head_message.body": new_body, "head_message.subject": subj}},
            )
        else:

            db.enron_dataset.update_one(
                {"_id": i["_id"]},
                {"$set": {"head_message.body": new_body}},
            )

        for j, k in enumerate(i["messages"]):

            new_body = remove_img_token(remove_gt(k["body"])).strip()
            new_body, subj = retrieve_subject(new_body)

            if subj:
                db.enron_dataset.update_one(
                    {"_id": i["_id"]},
                    {
                        "$set": {
                            "messages." + str(j) + ".body": new_body,
                            "messages." + str(j) + ".subject": subj,
                        }
                    },
                )
            else:

                db.enron_dataset.update_one(
                    {"_id": i["_id"]},
                    {"$set": {"messages." + str(j) + ".body": new_body}},
                )
    print("Cleaning bodies done.")

    print("Extracting attachments...")
    extract_attachments_obj(db)
    print("Extracting attachments done.")

    print("Removing automatic footers...")
    for i in garbage_dict["replacement_strings"].keys():
        print(f"Removing {i} from bodies...")
        count = 0
        for j in tqdm(db.enron_dataset.find()):
            for k in garbage_dict["replacement_strings"][i]:
                if k in j["head_message"]["body"]:
                    new_body = j["head_message"]["body"].replace(k, "").strip()
                    db.enron_dataset.update_one(
                        {"_id": j["_id"]}, {"$set": {"head_message.body": new_body}}
                    )
                for l, m in enumerate(j["messages"]):
                    if k in m["body"]:
                        new_body = m["body"].replace(k, "").strip()
                        db.enron_dataset.update_one(
                            {"_id": j["_id"]},
                            {"$set": {"messages." + str(l) + ".body": new_body}},
                        )
                        count += 1
        print(f"Removed {count} instances of {i} from bodies")

    for i in garbage_dict["regex"].keys():
        print(f"Removing {i} from bodies...")
        for j in tqdm(db.enron_dataset.find()):
            for k in garbage_dict["regex"][i]:
                if re.search(k, j["head_message"]["body"]):
                    new_body = re.sub(k, "", j["head_message"]["body"]).strip()
                    db.enron_dataset.update_one(
                        {"_id": j["_id"]}, {"$set": {"head_message.body": new_body}}
                    )
                    count += 1
                for l, m in enumerate(j["messages"]):
                    if re.search(k, m["body"]):
                        new_body = re.sub(k, "", m["body"]).strip()
                        db.enron_dataset.update_one(
                            {"_id": j["_id"]},
                            {"$set": {"messages." + str(l) + ".body": new_body}},
                        )
                        count += 1
        print(f"Removed {count} instances of {i} from bodies")
    print("Removing automatic footers done.")

    print("Extracting urls...")
    extract_urls_obj(db)
    print("Extracting urls done.")

    print("Tagging Documents...")
    tags_from_attachments(db)
    print("Attachments tagged.")
    tags_from_urls(db)
    print("Urls tagged.")
    add_word_count(db)
    print("Word count added.")
    tag_html_documents(db)
    print("Done.")


SRC_FOLDER_PATH = "datasets/maildir"
SAMPLE_SIZE = 2700
SAMPLE_FOLDER_PATH = "sample"
DST_FOLDER_PATH = "output/json_out"
IN_PATHS = generate_path(SRC_FOLDER_PATH, "all")

client = MongoClient("mongodb://localhost:27017/")
db = client.email
create_dataset(db, 'email_bodies_3',balance_dataset=True, include_thread='safe')

client.close()
