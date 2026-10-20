from pathlib import Path
import zipfile, shutil, hashlib, json

with zipfile.ZipFile('work/signed-compat/camera14-compat-aligned-debugSigned.apk') as src, zipfile.ZipFile('work/camera14-trace-unsigned.apk','w') as dst:
    for i in src.infolist():
        if i.filename.startswith('META-INF/') and i.filename.endswith(('.RSA','.SF','.MF')): continue
        dst.writestr(i,Path('work/camera14-classes1-trace.dex').read_bytes() if i.filename=='classes.dex' else src.read(i.filename))
with zipfile.ZipFile('work/hyper14/system_ext_a/framework/miui-framework.jar') as src, zipfile.ZipFile('work/miuicam-deps-trace.jar','w') as dst:
    for i in src.infolist(): dst.writestr(i,src.read(i.filename))
    dst.writestr('classes2.dex',Path('work/bridge-dex/classes.dex').read_bytes())
print('Trace APK and helper prepared; classes2/3 and native APK entries retained')
