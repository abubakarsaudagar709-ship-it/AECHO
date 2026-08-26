"""
user_profile.py — AECHO ka user data storage
Naam, preferred address, language, aur transfer password hash
yahan JSON file mein save/load hota hai.
"""

import json
import os

PROFILE_PATH = "aecho_user_profile.json"

DEFAULT_PROFILE = {
    "is_owner_set": False,       # True jab pehli baar Abubakar ka naam set ho jaye
    "name": None,                # current user ka naam
    "nickname": None,            # optional nickname
    "address_preference": None,  # "call me by this" wala term
    "language": "english",
    "transfer_password_hash": None,  # jab tak koi transfer na ho, None
    "favorites": {}              # jaise favorite song etc. (memory.py bhi use karega)
}


def load_profile():
    """Profile file load karta hai, agar na ho to default profile return karta hai."""
    if not os.path.exists(PROFILE_PATH):
        return DEFAULT_PROFILE.copy()

    with open(PROFILE_PATH, "r") as f:
        return json.load(f)


def save_profile(profile):
    """Profile ko JSON file mein save karta hai."""
    with open(PROFILE_PATH, "w") as f:
        json.dump(profile, f, indent=2)


def set_owner(name):
    """Pehli baar setup — Abubakar ka naam set karta hai."""
    profile = load_profile()
    profile["name"] = name
    profile["is_owner_set"] = True
    save_profile(profile)
    return profile


def set_address_preference(term):
    """'call me by this' wala preferred address save karta hai."""
    profile = load_profile()
    profile["address_preference"] = term
    save_profile(profile)
    return profile


def set_transfer_password(password_hash):
    """Ownership transfer se pehle password hash yahan store hota hai."""
    profile = load_profile()
    profile["transfer_password_hash"] = password_hash
    save_profile(profile)
    return profile


def reset_for_new_user(new_name, new_nickname=None):
    """
    Jab AECHO transfer ho jaye kisi doosre user ko, iska profile reset
    hoke naye user ka naam/nickname set karta hai. Purana password hash
    clear ho jata hai — naya owner chahe to naya set
