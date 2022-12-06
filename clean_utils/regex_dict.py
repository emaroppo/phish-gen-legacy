regex_dict = {
    "signatures": {
        "general": r"Enron\s*North\s*America\s*Corp\.\s*([0-9]*\s[A-z\s]*,\s[A-z0-9\s]*\s)([A-z]*,\s[A-z]*\s+)[0-9]*\s([0-9]*-[0-9]*-[0-9]*\s)\(phone\)\s([0-9]*-[0-9]*-[0-9]*\s)\(fax\)\s([A-z.]*@enron.com)",
        "legal": r"Enron North America Corp.\s*Legal\s*Department\s*1400\s*Smith\s*Street,\s*EB\s*3885\s*Houston,\s*Texas\s*77002",
    },
    "head_headers":r"[A-z-]*:((.*)(\n\t.*)*)",
    "headers":{"from":r"From:\s*(.*)",
    "sent_datetime":(
        r"Sent:\s*(([A-z0-9,\s]+,\s*[0-9]{2,4})\s*([0-9]{1,2}:[0-9]{1,2} (AM|PM)))",
        r"Date:\s*([A-z0-9, \/:]*)",
    )
    "to": r"To:\s*((.*)(\n +.*)*)",
    "subject": r"Subject:\s*(.*\s*)",
    "importance": r"Importance:\s*([A-z0-9]*)",
    "cc": r"[Cc]{2}:(.*)"
    }
    "forwarded": r"-{3,}\s*Forwarded[\s\n]by\s*([A-z0-9\/\.\s_]+)[\s\n]on\s*(([0-9]{1,2}\/[0-9]{1,2}\/[0-9]{1,4})\s*([0-9]{1,2}:[0-9]{1,2}\s*(PM|AM)))\s*-{3,}",
    
}
