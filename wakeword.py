"""
wakeword.py — AECHO wake word listener

Kaam: Android ke built-in SpeechRecognizer ko continuously chalata hai
aur jab bhi "aecho" bola jata hai, on_wake() callback trigger karta hai.
Ye background (service) aur app-open dono states mein kaam karega.

Note: Ye Android-specific hai (pyjnius se Android SpeechRecognizer API
use karta hai). Buildozer.spec mein permission chahiye:
    android.permissions = RECORD_AUDIO, INTERNET

Requirement: buildozer.spec ke requirements mein "pyjnius" add karna hoga.
"""

from jnius import autoclass, PythonJavaClass, java_method
from android.permissions import request_permissions, Permission

# Android classes
SpeechRecognizer = autoclass('android.speech.SpeechRecognizer')
RecognizerIntent = autoclass('android.speech.RecognizerIntent')
Intent = autoclass('android.content.Intent')
PythonActivity = autoclass('org.kivy.android.PythonActivity')
Locale = autoclass('java.util.Locale')

WAKE_WORD = "aecho"


class WakeWordListener:
    def __init__(self, on_wake_callback):
        """
        on_wake_callback: function jo AECHO sunte hi call hoga.
        Ye function island_overlay.py ko trigger karega baad mein.
        """
        self.on_wake_callback = on_wake_callback
        self.recognizer = None
        self.listening = False

    def request_mic_permission(self):
        request_permissions([Permission.RECORD_AUDIO])

    def start(self):
        """Continuous listening shuru karo."""
        self.listening = True
        activity = PythonActivity.mActivity
        self.recognizer = SpeechRecognizer.createSpeechRecognizer(activity)
        listener = self._build_listener()
        self.recognizer.setRecognitionListener(listener)
        self._listen_once()

    def _listen_once(self):
        """Ek listening cycle start karta hai — result aane ke baad khud restart hota hai."""
        if not self.listening:
            return
        intent = Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH)
        intent.putExtra(
            RecognizerIntent.EXTRA_LANGUAGE_MODEL,
            RecognizerIntent.LANGUAGE_MODEL_FREE_FORM,
        )
        intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE, Locale.getDefault())
        intent.putExtra(RecognizerIntent.EXTRA_PARTIAL_RESULTS, True)
        self.recognizer.startListening(intent)

    def _build_listener(self):
        outer = self

        class Listener(PythonJavaClass):
            __javainterfaces__ = ['android/speech/RecognitionListener']

            @java_method('(Landroid/os/Bundle;)V')
            def onResults(self, results):
                matches = results.getStringArrayList(
                    SpeechRecognizer.RESULTS_RECOGNITION
                )
                if matches and matches.size() > 0:
                    text = matches.get(0).lower()
                    if WAKE_WORD in text:
                        outer.on_wake_callback()
                # Restart listening for next phrase
                outer._listen_once()

            @java_method('(I)V')
            def onError(self, error):
                # Restart on error/timeout so it keeps listening continuously
                outer._listen_once()

            @java_method('(Landroid/os/Bundle;)V')
            def onPartialResults(self, partialResults):
                pass

            @java_method('()V')
            def onReadyForSpeech(self, params):
                pass

            @java_method('()V')
            def onBeginningOfSpeech(self):
                pass

            @java_method('(F)V')
            def onRmsChanged(self, rmsdB):
                pass

            @java_method('([B)V')
            def onBufferReceived(self, buffer):
                pass

            @java_method('()V')
            def onEndOfSpeech(self):
                pass

            @java_method('(ILandroid/os/Bundle;)V')
            def onEvent(self, eventType, params):
                pass

        return Listener()

    def stop(self):
        self.listening = False
        if self.recognizer:
            self.recognizer.stopListening()
            self.recognizer.destroy()
