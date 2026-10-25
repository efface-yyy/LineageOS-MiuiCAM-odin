#!/system/bin/sh
MODDIR=${0%/*}
sh "$MODDIR/first-start.sh"
RESULT=$?
cat "$MODDIR/first-start.log"
exit "$RESULT"
