import hashlib

def hash_text(text: str):
    text = " ".join(text.split())
    return hashlib.md5(text.encode()).hexdigest()