"""
app_launcher.py — AECHO ka app-opening aur song-play karne wala module
"Aecho open YouTube" ya "aecho play my favorite song" jaise commands
ye file handle karti hai — Android intents use karke apps kholta hai.
"""

import re
from jnius import autoclass
from memory import get_favorite

Intent = autoclass('android.content.Intent')
Uri = autoclass('android.net.Uri')
PythonActivity = autoclass('org.kivy.android.PythonActivity')

# Common apps ke package names (jitne chahiye utne add kar sakte ho)
APP_PACKAGES = {
    "youtube": "com.google.android.youtube",
    "whatsapp": "com.whatsapp",
    "instagram": "com.instagram.android",
    "chrome": "com.android.chrome",
    "gmail": "com.google.android.gm",
    "settings": "com.android.settings",
    "camera": "com.android.camera",
    "spotify": "com.spotify.music",
}

OPEN_APP_TRIGGERS = [
    r"open (\w+)", r"launch (\w+)", r"(\w+) khol", r"(\w+) kholo"
]

PLAY_ON_TRIGGERS = [
    # "play <song> on spotify" / "spotify pe <song> chala"
    (r"play (.+) on spotify", "spotify"),
    (r"spotify (?:pe|par) (.+) chala", "spotify"),
    (r"play (.+) on youtube", "youtube"),
    (r"youtube (?:pe|par) (.+) chala", "youtube"),
]

PLAY_SONG_TRIGGERS = [
    r"play (.+)", r"(.+) chala", r"(.+) bajao"
]

FAVORITE_SONG_TRIGGERS = [
    "my favorite song", "mera favorite song"
]


def open_app(app_name):
    """Package name se app ko launch karta hai."""
    app_name = app_name.lower().strip()
    package = APP_PACKAGES.get(app_name)

    if not package:
        return f"I don't know how to open {app_name} yet."

    activity = PythonActivity.mActivity
    launch_intent = activity.getPackageManager().getLaunchIntentForPackage(package)

    if launch_intent:
        activity.startActivity(launch_intent)
        return f"Opening {app_name}."
    return f"{app_name} is not installed."


def play_on_youtube(song_name):
    """YouTube search intent ke through directly song play karta hai."""
    activity = PythonActivity.mActivity
    search_query = song_name.replace(" ", "+")
    url = f"https://www.youtube.com/results?search_query={search_query}"

    intent = Intent(Intent.ACTION_VIEW)
    intent.setData(Uri.parse(url))
    intent.setPackage(APP_PACKAGES["youtube"])
    activity.startActivity(intent)

    return f"Playing {song_name} on YouTube."


def play_on_spotify(song_name):
    """Spotify search intent ke through directly song play karta hai."""
    activity = PythonActivity.mActivity
    search_query = song_name.replace(" ", "%20")
    uri = f"spotify:search:{search_query}"

    intent = Intent(Intent.ACTION_VIEW)
    intent.setData(Uri.parse(uri))
    intent.setPackage(APP_PACKAGES["spotify"])
    activity.startActivity(intent)

    return f"Playing {song_name} on Spotify."


def handle_command(text):
    """
    Master function — text ko check karta hai ki ye app-open command hai
    ya song-play command (YouTube/Spotify), aur sahi action call karta hai.
    Match na hone par None return karta hai.
    """
    text_lower = text.lower().strip()

    # "play my favorite song" — memory se nikal ke YouTube pe play karega
    for trigger in FAVORITE_SONG_TRIGGERS:
        if trigger in text_lower:
            song = get_favorite("favorite_song")
            if song:
                return play_on_youtube(song)
            return "I don't have a favorite song saved yet."

    # "play <song> on spotify/youtube" — explicit platform mention
    for pattern, platform in PLAY_ON_TRIGGERS:
        match = re.search(pattern, text_lower)
        if match:
            song = match.group(1).strip()
            if platform == "spotify":
                return play_on_spotify(song)
            return play_on_youtube(song)

    # "open <app>" — youtube, spotify, instagram, whatsapp, etc.
    for pattern in OPEN_APP_TRIGGERS:
        match = re.search(pattern, text_lower)
        if match:
            return open_app(match.group(1))

    # "play <song name>" — bina platform bataye, default YouTube
    for pattern in PLAY_SONG_TRIGGERS:
        match = re.search(pattern, text_lower)
        if match:
            return play_on_youtube(match.group(1))

    return None
