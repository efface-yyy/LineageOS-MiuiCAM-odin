from pathlib import Path
import shutil, hashlib, json, zipfile

src=Path('work/module'); root=Path('work/module-trace')
shutil.copytree(src,root,dirs_exist_ok=True)
def copy(a,b):
    dst=root/b; dst.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(a,dst)
copy('work/signed-trace/camera14-trace-aligned-debugSigned.apk','system/priv-app/MiuiCamera/MiuiCamera.apk')
copy('work/miuicam-deps-trace.jar','system/framework/miuicam-deps.jar')
copy('work/lineage-cameraserver-compat','system/bin/cameraserver')
(root/'module.prop').write_text('id=odin_lineage_miuicamera\nname=MIX 4 MIUI Camera diagnostic trace\nversion=0.2.0-diagnostic\nversionCode=2\nauthor=efface-yyy\ndescription=Metadata trace; unfinished port; exact 20260815 cameraserver ABI adaptation\n',newline='\n')
(root/'post-fs-data.sh').write_text('''#!/system/bin/sh
MODDIR=${0%/*}
chcon u:object_r:cameraserver_exec:s0 "$MODDIR/system/bin/cameraserver"
chmod 0755 "$MODDIR/system/bin/cameraserver"
resetprop -n sys.camera.miui.apk 1
''',newline='\n')
p=root/'customize.sh'
s=p.read_text()+'''
BASELINE=4a3237bc7cc0e50c5e7b4d5cbba3843882e06809846a5e8862033057a5077ac2
CURRENT=$(sha256sum /system/bin/cameraserver)
[ "${CURRENT%% *}" = "$BASELINE" ] || abort "Unsupported cameraserver build; diagnostic is only for the saved 20260815 ROM."
set_perm "$MODPATH/system/bin/cameraserver" 0 0 0755
chcon u:object_r:cameraserver_exec:s0 "$MODPATH/system/bin/cameraserver"
'''
p.write_text(s,newline='\n')
records={str(p.relative_to(root)).replace('\\','/'):hashlib.sha256(p.read_bytes()).hexdigest() for p in root.rglob('*') if p.is_file()}
Path('evidence/trace-module-manifest.json').write_text(json.dumps(records,indent=2))
with zipfile.ZipFile('work/signed-compat/camera14-compat-aligned-debugSigned.apk') as a,zipfile.ZipFile(root/'system/priv-app/MiuiCamera/MiuiCamera.apk') as b:
    changed=[n for n in a.namelist() if n in b.namelist() and not n.startswith('META-INF/') and a.read(n)!=b.read(n)]
    assert changed==['classes.dex'],changed
print('Coherent trace module prepared. Only classes.dex differs from previous compat APK; guard and framework adaptations retained.')
