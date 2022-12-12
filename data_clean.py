import json
import os
import shutil
from clean_utils.export import txt_to_json, bodies_to_txts
from clean_utils.sample import generate_path
from tqdm import tqdm


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

    for i in tqdm(in_paths):
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

    print(f"Successfully cleaned {len(os.listdir(dst_folder))} emails")


# merge all json files in json_out folder into one json file as a list of json objects
def merge_json_files(json_folder_path, json_file_name):
    json_list = []
    for json_file in os.listdir(json_folder_path):
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


SRC_FOLDER_PATH = "maildir"
SAMPLE_SIZE = 2700
SAMPLE_FOLDER_PATH = "sample"
DST_FOLDER_PATH = "json_out"
# IN_PATHS = generate_path(SRC_FOLDER_PATH, "all")

move_unclean_data(folder_path="email_bodies")
