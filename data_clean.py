import json
import os
from clean_utils.export import txt_to_json, bodies_to_txts
from clean_utils.sample import generate_path
import shutil


def load_thread(path):

    with open(path, "r", encoding="utf8", errors="ignore") as file:
        thread = file.read()
        thread_header, thread = thread.split("X-FileName:")
        thread = "\n".join(thread.split("\n")[2:])

    return thread, thread_header


def clean_thread(in_paths, dst_folder):

    if not os.path.exists(dst_folder):
        os.makedirs(dst_folder)

    print(f"Loading {len(in_paths)} emails...")

    counter = 0

    for i in in_paths:
        try:
            thread, thread_header = load_thread(i)
            counter += 1
            out_filename = (
                f"{counter}-{i.split('/')[-3]}_{i.split('/')[-2]}_{i.split('/')[-1]}"
            )
        except UnicodeDecodeError:
            pass
        except IsADirectoryError:
            pass

        txt_to_json(
            thread_id=counter,
            thread=thread,
            thread_header=thread_header,
            to_file=True,
            json_path=f"{dst_folder}/{out_filename}.json",
        )

        if counter % 1000 == 0:
            print(f"Successfully cleaned {counter} emails")

    print(f"Successfully cleaned {counter} emails")
    print("Done!")


folder_path = "txt_out"
"""
SRC_FOLDER_PATH = "maildir"
SAMPLE_SIZE = 2700
SAMPLE_FOLDER_PATH = "sample"
DST_FOLDER_PATH = "json_out"


IN_PATHS = generate_path(SRC_FOLDER_PATH, "all")
clean_thread(IN_PATHS, DST_FOLDER_PATH)


if not os.path.exists(folder_path):
    os.makedirs(folder_path)

counter = 0
for i in os.listdir("json_out"):
    if i[0] == ".":
        continue
    with open(f"json_out/{i}", "r") as f:
        counter += 1
        data = json.load(f)
        bodies_to_txts(data, to_file=True, txt_path=f"{folder_path}/{i[:-5]}")
        if counter % 1000 == 0:
            print(f"Successfully converted {counter} threads")

print(len(os.listdir("txt_out")))
"""
if not os.path.exists("header_miss"):
    os.makedirs("header_miss")

counter = 1
counter_1 = 1
for i in os.listdir(folder_path):

    with open(f"{folder_path}/{i}", "r") as file:
        thread = file.read()

        if "To:" in thread:
            shutil.move(f"{folder_path}/{i}", f"header_miss/{i}")
            counter += 1

        if counter % 1000 == 0:
            print(f"Moved {counter}/{counter_1} emails")
    counter_1 += 1


"""


SRC_FOLDER_PATH = "maildir"
SAMPLE_SIZE = 2700
SAMPLE_FOLDER_PATH = "sample"
DST_FOLDER_PATH = "json_out"


IN_PATHS = generate_path(SRC_FOLDER_PATH, "all")
clean_thread(IN_PATHS, DST_FOLDER_PATH)"""
