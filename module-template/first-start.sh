#!/system/bin/sh
# Only suppress the unavailable MIUI first-use handoff. Do not accept CTA.
MODDIR=${0%/*}
exec >>"$MODDIR/first-start.log" 2>&1
echo "First-start compatibility: $(date)"
[ "$(getprop ro.product.device)" = odin ] || exit 1
[ "$(sha256sum /system/priv-app/MiuiCamera/MiuiCamera.apk | cut -d ' ' -f 1)" = e744879ea93177b190938afb5dfca9038daa365a4cc32d5784147ea07f626f86 ] || exit 1
# Credential-encrypted app storage must be available before writing preferences.
n=0
until [ "$(am get-started-user-state 0 2>/dev/null)" = RUNNING_UNLOCKED ]; do
 n=$((n+1)); [ "$n" -le 150 ] || { echo "User locked; skipped. Retry action after unlock."; exit 1; }
 sleep 2
done
APP=/data/user/0/com.android.camera
[ -d "$APP" ] || { echo "App data unavailable; skipped"; exit 1; }
P=$APP/shared_prefs/camera_settings_global.xml
KEY=pref_camera_first_use_hint_shown_key
if [ -f "$P" ] && grep -q "$KEY" "$P"; then
 echo "Existing first-use choice preserved"
 exit 0
fi
# Prevent the app from overwriting a concurrently edited preference file.
# Binder shell commands must not receive a /data/adb log file descriptor.
am force-stop --user 0 com.android.camera >/dev/null 2>&1 || { echo "Cannot stop camera; preserved"; exit 1; }
OWNER=$(stat -c %u:%g "$APP") || exit 1
mkdir -p "$APP/shared_prefs" || exit 1
chown "$OWNER" "$APP/shared_prefs" || exit 1
chmod 0771 "$APP/shared_prefs" || exit 1
TMP=$P.odin-first-start-tmp
trap 'rm -f "$TMP"' EXIT
if [ -f "$P" ]; then
 grep -q "$KEY" "$P" && exit 0
 grep -q '</map>' "$P" || { echo "Unrecognized XML; preserved"; exit 1; }
 # Keep the first backup only; it remains private and is not uploaded.
 [ -e "$P.odin-first-start-backup" ] || cp -p "$P" "$P.odin-first-start-backup" || exit 1
 restorecon "$P.odin-first-start-backup" || exit 1
 sed 's@</map>@<boolean name="pref_camera_first_use_hint_shown_key" value="false" /></map>@' "$P" >"$TMP" || exit 1
else
 printf '%s\n' '<?xml version="1.0" encoding="utf-8" standalone="yes" ?>' '<map><boolean name="pref_camera_first_use_hint_shown_key" value="false" /></map>' >"$TMP" || exit 1
fi
chown "$OWNER" "$TMP" || exit 1
chmod 0600 "$TMP" || exit 1
restorecon "$APP/shared_prefs" "$TMP" || exit 1
mv -f "$TMP" "$P" || exit 1
restorecon "$P"
echo "Missing first-use hint initialized; CTA and other preferences unchanged"
