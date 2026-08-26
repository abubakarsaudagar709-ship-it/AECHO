"""
main.py — AECHO ka entry point
Saari modules ko yahan jodta hai: wake word sunna, island dikhana,
identity/security/memory check karna, command handle karna, aur bolna.
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView

from wakeword import WakeWordListener
from island_overlay import IslandOverlay
from identity import check_identity_query, get_wake_greeting
from security import (
    detect_address_preference,
    check_false_creator_claim,
    get_creator_denial_response,
)
from memory import try_remember, try_recall
from app_launcher import handle_command
from voice_output import VoiceOutput
from user_profile import load_profile, save_profile, set_owner, set_address_preference


class AechoUI(BoxLayout):
    """Chat-style screen — Claude jaisa layout, black+red theme."""

    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", **kwargs)

        self.chat_log = Label(
            text="",
            size_hint_y=None,
            valign="top",
            halign="left",
            markup=True,
        )
        self.chat_log.bind(texture_size=self._update_height)

        scroll = ScrollView()
        scroll.add_widget(self.chat_log)

        self.input_box = TextInput(
            hint_text="Type or say 'AECHO'...",
            size_hint_y=None,
            height=50,
            multiline=False,
        )
        self.input_box.bind(on_text_validate=self.on_submit)

        self.add_widget(scroll)
        self.add_widget(self.input_box)

    def _update_height(self, instance, size):
        self.chat_log.height = size[1]

    def append_log(self, sender, text):
        self.chat_log.text += f"\n[b]{sender}:[/b] {text}"

    def on_submit(self, instance):
        text = self.input_box.text
        self.input_box.text = ""
        App.get_running_app().handle_user_text(text)


class AechoApp(App):
    def build(self):
        self.voice = VoiceOutput()
        self.island = IslandOverlay()
        self.wakeword = WakeWordListener(on_wake_callback=self.on_wake)
        self.ui = AechoUI()

        self.profile = load_profile()

        # Pehli baar app open hui to naam poochenge
        if not self.profile.get("is_owner_set"):
            self.ui.append_log("AECHO", "What should I call you?")
        else:
            greeting = get_wake_greeting(
                self.profile.get("name"),
                self.profile.get("address_preference"),
            )
            self.ui.append_log("AECHO", greeting)

        self.wakeword.request_mic_permission()
        self.island.request_overlay_permission()
        self.wakeword.start()

        return self.ui

    def on_wake(self):
        """Wake word 'aecho' sunte hi ye call hota hai."""
        self.island.show()

    def handle_user_text(self, text):
        """Ek hi jagah se saari logic route hoti hai — text/voice dono ke liye."""
        self.ui.append_log("You", text)

        # Step 1: agar owner ka naam abhi set nahi hua
        if not self.profile.get("is_owner_set"):
            self.profile = set_owner(text.strip())
            reply = f"Nice to meet you, {text.strip()}."
            self._respond(reply)
            return

        # Step 2: false creator claim check
        if check_false_creator_claim(text):
            self._respond(get_creator_denial_response())
            return

        # Step 3: address preference set karna ("call me sir" etc.)
        new_address = detect_address_preference(text)
        if new_address:
            self.profile = set_address_preference(new_address)
            self._respond(f"Okay, I'll call you {new_address}.")
            return

        # Step 4: identity questions (who are you, founder, full form)
        identity_reply = check_identity_query(text)
        if identity_reply:
            self._respond(identity_reply)
            return

        # Step 5: memory — remember something
        remember_reply = try_remember(text)
        if remember_reply:
            self._respond(remember_reply)
            return

        # Step 6: app open / play song commands
        command_reply = handle_command(text)
        if command_reply:
            self._respond(command_reply)
            return

        # Step 7: kuch match nahi hua
        self._respond("I didn't quite get that.")

    def _respond(self, text):
        self.ui.append_log("AECHO", text)
        self.voice.speak(text)
        self.island.hide()


if __name__ == "__main__":
    AechoApp().run()
