[app]
title = BPL Football Manager
package.name = bplmanager
package.domain = org.abunoman
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
requirements = python3,kivy==2.3.0

orientation = portrait
fullscreen = 1
android.archs = arm64-v8a
android.allow_backup = True
android.api = 33
android.minapi = 21

[buildozer]
log_level = 2
warn_on_root = 0
