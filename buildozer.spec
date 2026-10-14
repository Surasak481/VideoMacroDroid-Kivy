[app]
title = Video to MacroDroid
package.name = videotomacrodroid
package.domain = com.example
source.dir =.
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
requirements = python3,kivy==2.3.0,pyjnius,androidstorage4kivy
orientation = portrait
fullscreen = 0
android.permissions = READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,READ_MEDIA_VIDEO,READ_MEDIA_IMAGES
android.api = 33
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True
android.ant = auto

[buildozer]
log_level = 2
warn_on_root = 1
