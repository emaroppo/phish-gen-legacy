import os
import random


def generate_path(src_folder, sample_size=None):
    email_paths = list()

    for i in os.listdir(src_folder):
        for j in ["inbox", "sent"]:

            try:
                email_paths += [
                    f"{src_folder}/{i}/{j}/{k}"
                    for k in os.listdir(f"{src_folder}/{i}/{j}/")
                    if k[0] != "."
                ]
            except FileNotFoundError:
                pass
            except NotADirectoryError:
                pass

    if type(sample_size) is int:
        email_paths_sample = random.sample(email_paths, sample_size)
        return email_paths_sample

    if type(sample_size) is float and sample_size < 1:
        email_paths_sample = random.sample(
            email_paths, int(len(email_paths) * sample_size)
        )
        return email_paths_sample

    else:
        return email_paths
