from pathlib import Path
import shutil
root=Path('work/module')
stock=Path('work/hyper14')
def copy(src,dst):
 p=root/dst;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,p)
def write(dst,s):
 p=root/dst;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s,encoding='utf-8',newline='\n')
copy(stock/'system_ext_a/framework/miui-framework.jar','system/framework/miuicam-deps.jar')
copy(stock/'product_a/etc/device_features/odin.xml','system/product/etc/device_features/odin.xml')
for n in ['libcamera_algoup_jni.xiaomi.so','libcamera_mianode_jni.xiaomi.so']:
 copy(stock/'system_ext_a/lib64'/n,'system/priv-app/MiuiCamera/lib/arm64/'+n)
copy(stock/'system_ext_a/lib64/libmicampostproc_client.so','system/lib64/libmicampostproc_client.so')
shutil.copytree('../previous-port-inputs/_work/module_b/META-INF',root/'META-INF',dirs_exist_ok=True)
perms=['SYSTEM_CAMERA','WRITE_MEDIA_STORAGE','WRITE_SECURE_SETTINGS','INTERACT_ACROSS_USERS','START_ACTIVITIES_FROM_BACKGROUND','LOG_COMPAT_CHANGE','READ_COMPAT_CHANGE_CONFIG']
write('system/etc/permissions/miui-camera-port.xml','<permissions><library name="miuicam-deps" file="/system/framework/miuicam-deps.jar"/><privapp-permissions package="com.android.camera">'+''.join('<permission name="android.permission.'+p+'"/>' for p in perms)+'</privapp-permissions></permissions>\n')
write('module.prop','id=odin_lineage_miuicamera\nname=MIX 4 MIUI Camera for LineageOS\nversion=0.1.0-test\nversionCode=1\nauthor=efface-yyy\ndescription=Odin HyperOS 1 camera 5.1.001130.2; Android 17 compatibility work in progress\n')
write('customize.sh','''#!/system/bin/sh
[ "$(getprop ro.product.device)" = odin ] || abort "This module requires Xiaomi MIX 4 (odin)."
ui_print "- MIX 4 MIUI Camera / LineageOS compatibility test"
set_perm_recursive "$MODPATH" 0 0 0755 0644
set_perm "$MODPATH/post-fs-data.sh" 0 0 0755
set_perm "$MODPATH/service.sh" 0 0 0755
''')
write('post-fs-data.sh','''#!/system/bin/sh
# Non-persistent properties: rollback on reboot with module disabled.
resetprop -n sys.camera.miui.apk 1
''')
write('service.sh','''#!/system/bin/sh
until [ "$(getprop sys.boot_completed)" = 1 ]; do sleep 2; done
for p in CAMERA RECORD_AUDIO ACCESS_FINE_LOCATION ACCESS_COARSE_LOCATION READ_EXTERNAL_STORAGE WRITE_EXTERNAL_STORAGE; do
 pm grant com.android.camera android.permission.$p 2>/dev/null
done
cmd appops set com.android.camera MANAGE_EXTERNAL_STORAGE allow
''')
manifest=Path('work/camera14-res/AndroidManifest.xml')
s=manifest.read_text(encoding='utf-8')
s=s.replace('<uses-library android:name="miuicam-deps" android:required="true"/>','')
s=s.replace('</application>','<uses-library android:name="miuicam-deps" android:required="true"/></application>')
manifest.write_text(s,encoding='utf-8')
print('initial module prepared')
