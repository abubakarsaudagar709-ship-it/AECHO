"""
island_overlay.py — "AECHO island" popup
Wake word trigger hote hi top pe ek chota black rounded popup dikhata hai
jisme "AECHO" likha hota hai — jab tak AECHO sun/respond kar raha hai.
Ye system-level overlay hai, isliye background aur app-open dono me kaam karega.

buildozer.spec mein extra permission chahiye:
    android.permissions = SYSTEM_ALERT_WINDOW, RECORD_AUDIO, INTERNET
"""

from jnius import autoclass
from android.permissions import request_permissions, Permission

WindowManager = autoclass('android.view.WindowManager')
LayoutParams = autoclass('android.view.WindowManager$LayoutParams')
PixelFormat = autoclass('android.graphics.PixelFormat')
TextView = autoclass('android.widget.TextView')
GradientDrawable = autoclass('android.graphics.drawable.GradientDrawable')
Color = autoclass('android.graphics.Color')
Gravity = autoclass('android.view.Gravity')
PythonActivity = autoclass('org.kivy.android.PythonActivity')
Build = autoclass('android.os.Build')
Handler = autoclass('android.os.Handler')
Looper = autoclass('android.os.Looper')

HIDE_DELAY_MS = 3000  # 3 second baad island khud hide ho jayega


class IslandOverlay:
    def __init__(self):
        self.activity = PythonActivity.mActivity
        self.window_manager = None
        self.view = None
        self.showing = False

    def request_overlay_permission(self):
        request_permissions([Permission.SYSTEM_ALERT_WINDOW])

    def _build_view(self):
        text_view = TextView(self.activity)
        text_view.setText("AECHO")
        text_view.setTextColor(Color.parseColor("#FF2D2D"))  # red text
        text_view.setTextSize(14)
        text_view.setGravity(Gravity.CENTER)
        text_view.setPadding(40, 20, 40, 20)

        bg = GradientDrawable()
        bg.setColor(Color.parseColor("#0A0A0A"))  # black background
        bg.setCornerRadius(50)
        text_view.setBackground(bg)

        return text_view

    def _get_layout_type(self):
        # Android version ke hisaab se overlay type alag hota hai
        if Build.VERSION.SDK_INT >= 26:
            return LayoutParams.TYPE_APPLICATION_OVERLAY
        return LayoutParams.TYPE_PHONE

    def show(self):
        """Wake word detect hote hi ye call hoga (wakeword.py ke callback se)."""
        if self.showing:
            return

        self.window_manager = self.activity.getSystemService(
            self.activity.WINDOW_SERVICE
        )
        self.view = self._build_view()

        params = LayoutParams(
            LayoutParams.WRAP_CONTENT,
            LayoutParams.WRAP_CONTENT,
            self._get_layout_type(),
            LayoutParams.FLAG_NOT_FOCUSABLE | LayoutParams.FLAG_NOT_TOUCHABLE,
            PixelFormat.TRANSLUCENT,
        )
        params.gravity = Gravity.TOP | Gravity.CENTER_HORIZONTAL
        params.y = 60  # top se thoda gap, dynamic island jaisa

        self.window_manager.addView(self.view, params)
        self.showing = True

        # Auto hide after delay
        handler = Handler(Looper.getMainLooper())
        handler.postDelayed(self.hide, HIDE_DELAY_MS)

    def hide(self):
        """Listening/response khatam hote hi island hide ho jata hai."""
        if self.showing and self.view:
            self.window_manager.removeView(self.view)
            self.showing = False
            self.view = None
