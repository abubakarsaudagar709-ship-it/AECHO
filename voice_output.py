"""
voice_output.py — AECHO ka text-to-speech (voice output)
Android ke built-in TTS engine ko use karta hai, male voice set karke.
Baad mein isi file mein custom/cloned voice switch karna aasan hoga.
"""

from jnius import autoclass, PythonJavaClass, java_method

TextToSpeech = autoclass('android.speech.tts.TextToSpeech')
Locale = autoclass('java.util.Locale')
PythonActivity = autoclass('org.kivy.android.PythonActivity')
Voice = autoclass('android.speech.tts.Voice')


class VoiceOutput:
    def __init__(self):
        self.tts = None
        self.ready = False
        self._init_tts()

    def _init_tts(self):
        activity = PythonActivity.mActivity
        listener = self._build_init_listener()
        self.tts = TextToSpeech(activity, listener)

    def _build_init_listener(self):
        outer = self

        class InitListener(PythonJavaClass):
            __javainterfaces__ = ['android/speech/tts/TextToSpeech$OnInitListener']

            @java_method('(I)V')
            def onInit(self, status):
                if status == TextToSpeech.SUCCESS:
                    outer.tts.setLanguage(Locale.US)
                    outer._select_male_voice()
                    outer.ready = True

        return InitListener()

    def _select_male_voice(self):
        """Available voices me se ek male voice dhundh ke set karta hai."""
        voices = self.tts.getVoices()
        if voices is None:
            return

        iterator = voices.iterator()
        while iterator.hasNext():
            voice = iterator.next()
            name = voice.getName().lower()
            # Android voice names me aksar "male"/"female" mention hota hai
            if "male" in name and "female" not in name:
                self.tts.setVoice(voice)
                return
        # Male voice specifically na mile to default hi rehne do

    def speak(self, text):
        """Diya gaya text bolta hai."""
        if not self.ready:
            return
        from android.speech.tts import TextToSpeech as TTSClass
        utterance_id = "aecho_utterance"
        self.tts.speak(text, TextToSpeech.QUEUE_FLUSH, None, utterance_id)

    def stop(self):
        """Abhi bol raha ho to rok deta hai."""
        if self.tts:
            self.tts.stop()

    def shutdown(self):
        """App band hote waqt TTS engine release karna zaroori hai."""
        if self.tts:
            self.tts.shutdown()
