#!/system/bin/sh
[ "$(getprop ro.product.device)" = odin ] || abort "This module requires Xiaomi MIX 4 (odin)."
ui_print "- MIX 4 MIUI Camera / LineageOS compatibility test"
set_perm_recursive "$MODPATH" 0 0 0755 0644
set_perm "$MODPATH/post-fs-data.sh" 0 0 0755
set_perm "$MODPATH/service.sh" 0 0 0755
set_perm "$MODPATH/first-start.sh" 0 0 0755
set_perm "$MODPATH/action.sh" 0 0 0755

BASELINE=4a3237bc7cc0e50c5e7b4d5cbba3843882e06809846a5e8862033057a5077ac2
CURRENT=$(sha256sum /system/bin/cameraserver)
case "${CURRENT%% *}" in
 "$BASELINE"|b40953304dee7654c498f7f85527dba1e03798c6f3b615fe6a879c59678890e9|599325278fd4721293a051d8852d5eeb54109778786c5ec2b619b57fe22c2df7) ;;
 *) abort "Unsupported cameraserver build." ;;
esac
case "$(sha256sum /vendor/lib64/hw/camera.qcom.so | cut -d ' ' -f 1)" in
 a2c7bbb1d54b154d95e14acb33d2f25a5e99707d787bd3119362ff95075c39d4|0b869f9ec111681f90100db0bbe47196a55f2f44ff22ef20039d90ec3a05ed0a|c3d262079c7c09efaa060b69a6c10eb90442e1cb1ddacc7641ca046ffc159d52) ;;
 *) abort "Unsupported camera HAL build." ;;
esac
[ "$(sha256sum /vendor/lib/modules/camera.ko | cut -d ' ' -f 1)" = 054b477e19cd0cb8a015f0ce28295db6c688e14a022fed90ad5919caa12ef51c ] || abort "Unsupported OIS driver. Use the matching build; disable this module before a ROM update."

set_perm "$MODPATH/system/bin/cameraserver" 0 0 0755
chcon u:object_r:cameraserver_exec:s0 "$MODPATH/system/bin/cameraserver"

[ "$(sha256sum /system/lib64/libgui.so | cut -d ' ' -f 1)" = 232543cf7dd5b525dfd7ebe3eb9fa1816f8c69f2a73e4445beea22ae6a6b4366 ] || abort "Unsupported libgui ABI."

case "$(sha256sum /system/lib/libstagefright.so | cut -d ' ' -f 1)" in
 850f0604ba48deefe6d88c7d39085334a127bf48a662a263ab98068b7b8ffb67|893a7e70d74933c185b2e215a3fcbd8e2eeaa6d651d1860c7f27b495ffd56769) ;;
 *) abort "Unsupported 32-bit FrameDecoder build." ;;
esac
[ "$(sha256sum /system/lib/libsfplugin_ccodec_utils.so | cut -d ' ' -f 1)" = 277e3b0b8574c8a062e0e5ec2b0bb0482c4d5f446e26ea39b1d04ef7f7f24554 ] || abort "Unsupported frame bridge ABI dependency."
[ "$(sha256sum /system/lib/libstagefright_foundation.so | cut -d ' ' -f 1)" = 4eb08a0015abe9c42411c513cbbcea79d2f751954cc0b72dfd991b8de775fe25 ] || abort "Unsupported frame bridge ABI dependency."
[ "$(sha256sum /system/lib/libutils.so | cut -d ' ' -f 1)" = 44c75a39655d0e5a27b7f8d7bf2fe0b37432efa9d05bdb5a3a1301210f66340f ] || abort "Unsupported frame bridge ABI dependency."

case "$(sha256sum /vendor/etc/media_codecs.xml | cut -d ' ' -f 1)" in
 83947422456cc6971fed634e4b889834a38ff16f6bd0bed06be26ba51c75ca57|27e5be030f46dfcb0486d458296413b095d2e86d7718af1b3c4884528217bbbd) ;;
 *) abort "Unsupported codec configuration build." ;;
esac

case "$(sha256sum /vendor/etc/media_codecs_lahaina.xml | cut -d ' ' -f 1)" in
 83947422456cc6971fed634e4b889834a38ff16f6bd0bed06be26ba51c75ca57|27e5be030f46dfcb0486d458296413b095d2e86d7718af1b3c4884528217bbbd) ;;
 *) abort "Unsupported codec configuration build." ;;
esac

case "$(sha256sum /vendor/lib/libtinycompress.so | cut -d ' ' -f 1)" in
 9a7215d1bfe46aeff0ea0c680dcd45aaf4b0fdd0e5eed1457793325cdd805cfe|f0edc60ab3e93aeab5e81d48e806d635485c0cb4724d3f85b5542ac61a164ab9) ;;
 *) abort "Unsupported 32-bit tinycompress build." ;;
esac
