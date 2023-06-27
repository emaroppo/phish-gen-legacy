import re

def remove_corrupted_characters(body):
    body = re.sub(r"(=09|=20|=01|=\n)", r"", body)
    return body


def remove_gt(body):
    body = body.split("\n")
    new_body = []
    for i in body:
        new_body.append(i.lstrip("> "))
    new_body = "\n".join(new_body)
    return new_body


def remove_img_token(body):
    return body.replace("[IMAGE]", "").strip()







