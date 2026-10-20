#!/system/bin/sh
MODDIR=${0%/*}
LIBDIR=/data/data/com.android.camera/app_qigsaw/5.0.0.0/ambilight/v1.3.5@20220126/nativeLib/arm64-v8a
TARGET=$LIBDIR/libcamera_ambilight_ambt_qcom.so
SRC=$MODDIR/compat/ambilight
LOG=$MODDIR/ambilight-bind.log
exec >"$LOG" 2>&1
echo "Ambilight loader compatibility; $(date)"
[ -f "$TARGET" ] || { echo "Exact cached plugin not present; no changes"; exit 0; }
[ ! -d /dev/dma_heap ] && [ -c /dev/ion ] || { echo "ION-only guard not met"; exit 0; }
[ "$(sha256sum "$TARGET" | cut -d ' ' -f 1)" = 43a09f5ab1599d15c385a1b2cdc5051323e435e55ece4961c59bd6212089ead2 ] || { echo "Plugin hash mismatch; no changes"; exit 1; }
OWNER=$(stat -c %u:%g "$TARGET")
CONTEXT=$(ls -Zd "$TARGET" | cut -d ' ' -f 1)
for NAME in libcamera_ambilight_ambt_qcom.so libodinheap.so; do
 chown "$OWNER" "$SRC/$NAME" || exit 1
 chmod 0600 "$SRC/$NAME" || exit 1
 chcon "$CONTEXT" "$SRC/$NAME" || exit 1
done
ALIAS=$LIBDIR/libodinheap.so
if [ ! -e "$ALIAS" ]; then
 touch "$ALIAS" || exit 1
 chown "$OWNER" "$ALIAS" || exit 1
 chmod 0600 "$ALIAS" || exit 1
 chcon "$CONTEXT" "$ALIAS" || exit 1
fi
[ "$(stat -c %s "$ALIAS")" = 0 ] || { echo "Alias already exists; no changes"; exit 1; }
mount --bind "$SRC/libodinheap.so" "$ALIAS" || exit 1
mount --bind "$SRC/libcamera_ambilight_ambt_qcom.so" "$TARGET" || { umount "$ALIAS"; exit 1; }
sha256sum "$TARGET" "$ALIAS"
echo "Bound loader name and private original allocator; original plugin file unchanged beneath bind"
