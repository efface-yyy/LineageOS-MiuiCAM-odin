#!/system/bin/sh
MODDIR=${0%/*}
chcon u:object_r:cameraserver_exec:s0 "$MODDIR/system/bin/cameraserver"
chmod 0755 "$MODDIR/system/bin/cameraserver"
resetprop -n sys.camera.miui.apk 1
chcon u:object_r:vendor_configs_file:s0 "$MODDIR/system/vendor/etc/media_codecs.xml" "$MODDIR/system/vendor/etc/media_codecs_lahaina.xml"

# Runtime-only opt-in for the exact driver missing Xiaomi post-init support.
resetprop -n persist.vendor.camera.odin_postinit_compat 0
if [ "$(sha256sum /vendor/lib/modules/camera.ko | cut -d ' ' -f 1)" = 054b477e19cd0cb8a015f0ce28295db6c688e14a022fed90ad5919caa12ef51c ]; then
 resetprop -n persist.vendor.camera.odin_postinit_compat 1
fi
chcon u:object_r:vendor_file:s0 "$MODDIR/system/vendor/lib64/hw/camera.qcom.so"
chcon u:object_r:vendor_file:s0 "$MODDIR/system/vendor/lib/libtinycompress.so"
