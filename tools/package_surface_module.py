from pathlib import Path
import shutil,hashlib,json,subprocess,sys
root=Path('work/module-surface')
shutil.copytree('work/module-custom-stream',root,dirs_exist_ok=True)
shutil.copy2('work/libcamera_algoup_jni-surface-compat.so',root/'system/priv-app/MiuiCamera/lib/arm64/libcamera_algoup_jni.xiaomi.so')
(root/'module.prop').write_text('id=odin_lineage_miuicamera\nname=MIX 4 MIUI Camera compatibility validation\nversion=0.4.0-surface-compat\nversionCode=4\nauthor=efface-yyy\ndescription=Exact 20260815 build; custom stream and Surface ABI fixes; full feature and quality validation incomplete\n',newline='\n')
p=root/'customize.sh';s=p.read_text()
s+='''
[ "$(sha256sum /system/lib64/libgui.so | cut -d ' ' -f 1)" = 232543cf7dd5b525dfd7ebe3eb9fa1816f8c69f2a73e4445beea22ae6a6b4366 ] || abort "Unsupported libgui ABI."
'''
p.write_text(s,newline='\n')
records={str(p.relative_to(root)).replace('\\','/'):hashlib.sha256(p.read_bytes()).hexdigest() for p in root.rglob('*') if p.is_file()}
Path('evidence/surface-module-manifest.json').write_text(json.dumps(records,indent=2))
subprocess.run([sys.executable,'tools/build_module.py',str(root),'modules/odin_lineage_miuicamera_0.4.0-surface-compat.zip'],check=True)
