
from email.utils import parseaddr, parsedate_to_datetime
import regex as re

regex_fw=r'[-\s]{3,}Forwarded\s+by\s+(?P<sender>.*)\s+on\s+(?P<datetime>(?P<date>[\d\/]{8,})\s+(?P<time>[\d:]{5,}\s+[AP]M))\s+-{2,}'
regex1=r'(?:"(?P<name>.*?)"\s+<(?P<email_address>(?:[^@]+)@(?:[^>]+))>|(?P<email_address1>\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b))\son\s(?P<datetime>(?P<date>(?:\d\d\/){2}\d{4})\s*(?P<time>\d{2}:\d{2}:\d{2}\s+(?:AM|PM)))\s+(?:to:\s+(?P<to>((?:.*)\s)*?))?(?:cc:\s+(?P<cc>((.*)\s)*?))?(?:subject:\s+(?P<subject>((?:.*)\s)*?))?\s'
regex2=r'-{1,}\s*?Original\s*?Message\s*?-{1,}\s+(?:From:\s+"(?P<name>.*)"\s+<(?P<email_address>.*)>)\s(?:To:\s+<(?P<to>(.*)>))\s+(?:Sent:\s+(?P<datetime>(.*)))\s+(?:Subject:\s+(?P<subject>(.*)))\s'
regex2_1=r'-{1,}\s*?Original\s*?Message\s*?-{1,}\s+(?:From:\s+(?:"?(?P<name>(?!@).*)"?\s+)?)(?:<?(?P<email_address>.*@.*)>?\s)?(?P<datetime>Sent:\s+(.*))\s+(?P<to>To:(?:"?(?P<name_to>(?!@).*)"?\s+)?)(?:Cc:(?P<cc>(?:"?(?P<name_cc>(?!@).*)"?\s+)?(?:<?(?P<email_address_cc>.*@.*)>?\s+)?))?(?:Subject:\s+?(?P<subject>(.*?)))\s'
regex3=r'(Sender:\s+(.*))\s+(?P<email>Reply-To:\s+(.*))\s+(From:\s+(.*))\s+(To:\s+(.*))\s+(Subject:\s+(.*))\s+(Date:\s+(.*))\s+'
regex4=r'(?P<name1>.+?)\s+(?P<datetime>(?P<date>[\d\/]{8,})\s+?(?P<time>[\d:]{4,}\s+[AP]M))\s+?To:(?P<to>.*)\s+?cc:(?P<cc>.*\s*?)*?Subject:(?P<subject>.*\s+?)*?\n'

regex_list=[regex1,regex2,regex2_1,regex3,regex4]

compiled_regex_patterns=[re.compile(i, re.IGNORECASE | re.MULTILINE) for i in regex_list]

def parse_addresses(addresses):
    if type(addresses) is list:
        addresses = [parseaddr(i) for i in addresses]
        addresses = [(i[0], i[1].lower()) for i in addresses]
        addresses = [{"name": i[0], "email": i[1]} for i in addresses]
        for i in addresses:
            if i["name"] == "":
                del i["name"]
            if i["email"] == "":
                del i["email"]
    else:
        addresses = parseaddr(addresses)
        addresses = {"name": addresses[0], "email": addresses[1].lower()}
        if addresses["name"] == "":
            del addresses["name"]
        if addresses["email"] == "":
            del addresses["email"]

    return addresses

# extract email addresses and names from main headers
def extract_main_headers(email):
    headers = email._headers
    headers = {i[0]: i[1] for i in headers}  # convert to dict

    # sanitize keys
    headers = {
        k.lower().replace("-", "_").replace(".", ""): v
        for k, v in headers.items()
    }
    headers["sender"] = headers.pop("from")

    # parse names and emails

    for i in ["sender", "to", "cc", "bcc"]:
        if i in headers:
            headers[i] = parse_addresses(headers[i])

    # parse date
    headers["date"] = parsedate_to_datetime(headers["date"])

    return headers

def extract_main_body(email):
    body = email.get_body(preferencelist=("plain")).get_content()
    return body

def parse_string(input_string, compiled_regex_pattern):
    matches = list(re.finditer(compiled_regex_pattern, input_string))

    text_chunks = []
    start = 0
    for match in matches:
        text_chunks.append(input_string[start:match.start()].strip())
        start = match.end()
    text_chunks.append(input_string[start:].strip())

    result = []
    for match, text in zip(matches, text_chunks[1:]):  # skip the text before the first pattern
        result.append({
            "header": match.groupdict(),
            "body": text,
            "start": match.start(),
            "end": match.end()
        })

    return result

def parse_string_multi(input_string, main_headers, regex_patterns=compiled_regex_patterns):
    results = []

    for pattern in regex_patterns:
        matches = parse_string(input_string, pattern)
        for match in matches:
            if ('email_address' not in match['header'] or match['header']['email_address'] is None) and ('email_address1' in match['header'] and match['header']['email_address1'] is not None):
                match['header']['email_address'] = match['header']['email_address1']
                del match['header']['email_address1'] 
            match['body'] = match['body'].strip()
            match['header'] = {k: v.strip() for k, v in match['header'].items() if v is not None}
        results.extend(matches)
    
    # Sort results
    results.sort(key=lambda x: x['start']) 
    
    # If no matches were found, add the main_headers with the entire input_string as body
    if len(results) == 0:
        results.append({'header': main_headers, 'body': input_string, 'start': 0, 'end': len(input_string)})
        
    return results


