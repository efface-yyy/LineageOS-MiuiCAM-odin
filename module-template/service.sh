#!/system/bin/sh
until [ "$(getprop sys.boot_completed)" = 1 ]; do sleep 2; done
for p in CAMERA RECORD_AUDIO ACCESS_FINE_LOCATION ACCESS_COARSE_LOCATION READ_EXTERNAL_STORAGE WRITE_EXTERNAL_STORAGE; do
 pm grant com.android.camera android.permission.$p 2>/dev/null
done
cmd appops set com.android.camera MANAGE_EXTERNAL_STORAGE allow

MODDIR=${0%/*}
su -mm -c "sh $MODDIR/ambilight-bind.sh"
