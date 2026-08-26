"""
identity.py — AECHO ki identity + greeting logic
Full form, founder info, "who are you", aur time-based greeting yahan handle hota hai.
"""

import datetime

FOUNDER_NAME = "Mr. Abubakar Saudagar"
FULL_FORM = "Abubakar's Enhanced Cognitive Handling Operator"

# Questions jo "who made you / who is your founder" type ke honge
FOUNDER_TRIGGERS = [
    "who made you", "who created you", "who is your founder",
    "who is your creator", "tumhe kisne banaya", "tera founder kaun hai",
    "tumhara creator kaun hai", "who built you"
]

FULLFORM_TRIGGERS = [
    "what is your full form", "your full form", "aecho ka full form",
    "full form of aecho", "what does aecho stand for"
]

WHOAMI_TRIGGERS = [
    "who are you", "what are you", "tum kaun ho", "aap kaun hain"
]


def get_founder_response():
    return f"I was created by {FOUNDER_NAME}, The Greatest of all time."


def get_fullform_response():
    return f"AECHO stands for {FULL_FORM}."


def get_whoami_response():
    return f"I am AECHO — {FULL_FORM}."


def check_identity_query(text):
    """
    User ka bola hua text check karta hai — agar founder, full form,
    ya "who are you" se related sawal hai to sahi fixed response
    return karta hai. Match na hone par None return karega.
    """
    text = text.lower()

    for trigger in WHOAMI_TRIGGERS:
        if trigger in text:
            return get_whoami_response()

    for trigger in FOUNDER_TRIGGERS:
        if trigger in text:
            return get_founder_response()

    for trigger in FULLFORM_TRIGGERS:
        if trigger in text:
            return get_fullform_response()

    return None


def get_time_based_greeting():
    """Current time ke hisaab se greeting return karta hai."""
    hour = datetime.datetime.now().hour

    if 5 <= hour < 12:
        time_part = "good morning"
    elif 12 <= hour < 17:
        time_part = "good afternoon"
    elif 17 <= hour < 21:
        time_part = "good evening"
    else:
        time_part = "good night"

    return f"Assalamualaikum sir, {time_part}"


def get_wake_greeting(user_name, address_preference=None):
    """
    Wake word trigger hone par ye call hoga.
    user_name: profile mein saved naam
    address_preference: "call me by this" wala preferred term (jaise
    "Mr. Abubakar Saudagar" / "sir" / "Abu" / "abubakar")
    """
    greeting = get_time_based_greeting()

    if address_preference:
        # Agar preferred address set hai, usko priority denge
        return greeting.replace("sir", address_preference)

    return greeting
