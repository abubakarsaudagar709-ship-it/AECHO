"""
memory.py — AECHO ki conversational memory
User jo bhi casually bole (jaise "aecho mera favorite song X hai"),
uska yaad rakhna aur baad me use karna is file ka kaam hai.
Storage user_profile.py ke "favorites" dict ke through hoti hai,
taaki sab data ek hi jagah rahe.
"""

import re
from user_profile import load_profile, save_profile

# Patterns jinse "X mera Y hai" type statement pehchana jayega
REMEMBER_PATTERNS = [
    (r"my favorite (\w+) is (.+)", "favorite_{0}"),
    (r"mera favorite (\w+) (.+) hai", "favorite_{0}"),
    (r"remember (?:that )?my (\w+) is (.+)", "{0}"),
    (r"yaad rakh mera (\w+) (.+) hai", "{0}"),
]

# Patterns jinse baad me wapas poocha jayega
RECALL_PATTERNS = [
    (r"what is my favorite (\w+)", "favorite_{0}"),
    (r"mera favorite (\w+) kya hai", "favorite_{0}"),
    (r"play my favorite (\w+)", "favorite_{0}"),
]


def try_remember(text):
    """
    User ke text me se koi 'remember this' type statement dhundhta hai.
    Milne par profile me save karke confirmation return karta hai.
    Kuch na mile to None return karta hai.
    """
    text_lower = text.lower().strip()

    for pattern, key_template in REMEMBER_PATTERNS:
        match = re.search(pattern, text_lower)
        if match:
            groups = match.groups()
            key = key_template.format(groups[0])
            value = groups[-1].strip()

            profile = load_profile()
            profile["favorites"][key] = value
            save_profile(profile)

            return f"Got it, I'll remember that."

    return None


def try_recall(text):
    """
    User kuch pooch raha hai jo pehle save hua tha (jaise favorite song).
    Milne par saved value return karta hai, warna None.
    """
    text_lower = text.lower().strip()

    for pattern, key_template in RECALL_PATTERNS:
        match = re.search(pattern, text_lower)
        if match:
            key = key_template.format(match.group(1))
            profile = load_profile()
            value = profile["favorites"].get(key)

            if value:
                return value

    return None


def get_favorite(key_name):
    """Direct lookup — jaise get_favorite('favorite_song')"""
    profile = load_profile()
    return profile["favorites"].get(key_name)
