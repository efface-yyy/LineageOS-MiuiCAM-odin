from pathlib import Path
import zipfile
with zipfile.ZipFile('work/signed14/camera14-aligned-debugSigned.apk') as src, zipfile.ZipFile('work/camera14-compat-unsigned.apk','w') as dst:
    for i in src.infolist():
        if i.filename.startswith('META-INF/') and i.filename.endswith(('.RSA','.SF','.MF')):
            continue
        data = Path('work/camera14-classes2-compat.dex').read_bytes() if i.filename == 'classes2.dex' else src.read(i.filename)
        dst.writestr(i, data)
with zipfile.ZipFile('work/hyper14/system_ext_a/framework/miui-framework.jar') as src, zipfile.ZipFile('work/miuicam-deps-compat.jar','w') as dst:
    for i in src.infolist():
        dst.writestr(i, src.read(i.filename))
    dst.writestr('classes2.dex', Path('work/bridge-dex/classes.dex').read_bytes())
Path('tools/accept_cta.sh').write_text('''#!/system/bin/sh
am force-stop com.android.camera
P=/data/user/0/com.android.camera/shared_prefs/camera_settings_global.xml
sed -i 's/name="pref_camera_recordcta_key" value="false"/name="pref_camera_recordcta_key" value="true"/' "$P"
''', newline='\n')
