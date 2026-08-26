[app]
title = AECHO
package.name = aecho
package.domain = org.abubakarsaudagar

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 1.0

requirements = python3,kivy,pyjnius,android

android.permissions = RECORD_AUDIO,INTERNET,SYSTEM_ALERT_WINDOW

android.api = 33
android.minapi = 24
android.ndk = 25b
android.archs = arm64-v8a,armeabi-v7a

orientation = portrait
fullscreen = 0

icon.filename = %(source.dir)s/assets/icon.png

[buildozer]
log_level = 2
warn_on_root = 1
